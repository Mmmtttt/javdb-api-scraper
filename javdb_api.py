"""
JAVDB API 核心模块
提供视频、演员、Tag 搜索和数据抓取功能

对外暴露的主要接口:
- get_video_detail: 抓取作品页全量信息
- get_video_by_code: 根据code搜索并获取详情
- get_actor_works_by_page: 获取演员作品（分页，只返回code等基础信息）
- get_actor_works_full_by_page: 获取演员作品全量信息（分页）
- get_tag_works_by_page: 获取Tag作品（分页，只返回code等基础信息）
- get_tag_works_full_by_page: 获取Tag作品全量信息（分页）
- search_by_tags: 多类标签组合搜索（基础信息）
- search_by_tags_full: 多类标签组合搜索（全量信息）
- search_actor: 搜索演员
- scrape_actor_full: 全量抓取演员所有信息

标签管理模块 (tag_manager):
- fetch_tags: 爬取标签分类建立数据库
- get_tag_info: 获取特定标签信息
- search_tag_by_name: 根据名称搜索标签
- build_tag_url: 构建标签搜索URL
- get_category_list: 获取所有分类列表
"""

import re
import json
import time
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin, quote
from pathlib import Path
from datetime import datetime

from curl_cffi import requests
from bs4 import BeautifulSoup

import config
from utils import JSONExporter, ImageDownloader, MagnetExporter, DataProcessor


class JavdbAPI:
    """
    JAVDB API 客户端
    
    提供以下功能：
    - 视频详情抓取（番号、标题、磁力链接、Tags、缩略图等）
    - 演员搜索和作品抓取（支持分页）
    - Tag 搜索和作品抓取（支持分页）
    - 根据番号搜索获取详情
    - 缩略图下载（自动使用高清图）
    
    示例:
        >>> api = JavdbAPI()
        >>> detail = api.get_video_detail("YwG8Ve", download_images=True)
        >>> print(detail['code'])  # MIDA-583
    """
    
    def __init__(self, domain_index: int = 0):
        """
        初始化 API 客户端
        
        Args:
            domain_index: 域名索引，用于自动切换域名
        """
        self.domain_index = domain_index
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        
        self._load_cookies()
        
        self.request_count = 0
        self.success_count = 0
        
        self.image_downloader = ImageDownloader(self.session)
        self.json_exporter = JSONExporter()
        self.magnet_exporter = MagnetExporter()
    
    @property
    def base_url(self) -> str:
        """获取当前基础 URL"""
        return f"https://{config.JAVDB['domains'][self.domain_index]}"
    
    def _load_cookies(self):
        """从文件加载 cookies"""
        cookie_path = Path(config.COOKIE_FILE)
        if cookie_path.exists():
            try:
                with open(cookie_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                    self.session.cookies.update(cookies)
            except Exception as e:
                pass
    
    def _get_full_url(self, path: str) -> str:
        """获取完整 URL"""
        if path.startswith('http'):
            return path
        return urljoin(self.base_url, path)
    
    def _switch_domain(self):
        """切换到下一个域名"""
        self.domain_index = (self.domain_index + 1) % len(config.JAVDB['domains'])
    
    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        发送 HTTP 请求，支持自动重试和域名切换
        
        Args:
            method: 请求方法 (get/post)
            path: 请求路径
            **kwargs: 其他请求参数
            
        Returns:
            响应对象
        """
        url = self._get_full_url(path)
        kwargs.setdefault('timeout', config.JAVDB['timeout'])
        kwargs.setdefault('allow_redirects', True)
        
        last_exception = None
        
        for retry in range(config.JAVDB['retry_times']):
            try:
                self.request_count += 1
                
                if method.lower() == 'get':
                    response = self.session.get(url, **kwargs)
                else:
                    response = self.session.post(url, **kwargs)
                
                if response.status_code == 200:
                    self.success_count += 1
                    return response
                
                if response.status_code in [403, 503]:
                    self._switch_domain()
                    url = self._get_full_url(path)
                    continue
                
                response.raise_for_status()
                
            except Exception as e:
                last_exception = e
                time.sleep(2)
        
        raise Exception(f"请求失败: {last_exception}")
    
    def get(self, path: str, **kwargs) -> requests.Response:
        """发送 GET 请求"""
        return self.request('get', path, **kwargs)
    
    def get_stats(self) -> Dict:
        """获取请求统计"""
        return {
            'request_count': self.request_count,
            'success_count': self.success_count,
            'success_rate': f"{(self.success_count / self.request_count * 100):.1f}%" if self.request_count > 0 else "0%",
        }
    
    # ==================== 视频详情 ====================
    
    def get_video_detail(self, video_id: str, download_images: bool = False) -> Dict:
        """
        抓取作品页全量信息
        
        Args:
            video_id: 视频 ID (如 YwG8Ve)
            download_images: 是否下载缩略图（自动使用高清图）
            
        Returns:
            包含番号、标题、磁力链接、Tags、缩略图等信息的字典
            
            返回格式:
            {
                'video_id': 'YwG8Ve',
                'code': 'MIDA-583',
                'title': '作品标题',
                'tags': ['美少女電影', '單體作品', ...],
                'series': '系列名',
                'actors': ['井上もも'],
                'magnets': [
                    {'magnet': 'magnet:...', 'size_text': '5.27GB', 'size_mb': 5396.48}
                ],
                'thumbnail_images': [
                    'https://c0.jdbstatic.com/samples/yw/YwG8Ve_l_0.jpg',
                    ...
                ],
                'preview_video': '',
                'url': 'https://javdb.com/v/YwG8Ve'
            }
        """
        response = self.get(f'/v/{video_id}')
        soup = BeautifulSoup(response.text, 'lxml')
        
        title = self._extract_title(soup)
        code = self._extract_code(soup)
        tags = self._extract_tags(soup)
        series = self._extract_series(soup)
        actors = self._extract_actors(soup)
        magnets = self._extract_magnets(soup)
        thumbnail_images = DataProcessor.extract_hd_thumbnails(video_id, soup)
        preview_video = self._extract_preview_video(soup)
        
        result = {
            'video_id': video_id,
            'title': title,
            'code': code,
            'tags': tags,
            'series': series,
            'actors': actors,
            'magnets': magnets,
            'thumbnail_images': thumbnail_images,
            'preview_video': preview_video,
            'url': response.url,
        }
        
        if download_images and thumbnail_images and code:
            self.image_downloader.download_thumbnails(code, thumbnail_images)
        
        return result
    
    def get_video_by_code(self, code: str, download_images: bool = False) -> Optional[Dict]:
        """
        根据番号搜索并获取作品全量信息
        
        搜索code，模糊匹配到的第一个结果就是
        
        Args:
            code: 番号 (如 MIDA-583, SSIS-001)
            download_images: 是否下载缩略图
            
        Returns:
            视频详情字典，如果未找到返回 None
        """
        encoded_code = quote(code)
        url = f"/search?q={encoded_code}"
        
        response = self.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        items = soup.select('div.item a.box')
        if not items:
            return None
        
        first_item = items[0]
        work = self._parse_work_item(first_item)
        
        if not work:
            return None
        
        return self.get_video_detail(work['video_id'], download_images)
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        selectors = ['h1.title', '.video-title', 'h1', 'title']
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                title = re.sub(r'\|.*$', '', title)
                return title
        return ""
    
    def _extract_code(self, soup: BeautifulSoup) -> str:
        """提取番号（字母+数字+中划线）"""
        copy_btn = soup.select_one('.panel-block.first-block .copy-to-clipboard')
        if copy_btn:
            code = copy_btn.get('data-clipboard-text', '')
            if code and re.match(r'^[A-Z]+-?\d+$', code, re.I):
                return code.upper()
        
        title_elem = soup.select_one('h1.title, .video-title')
        if title_elem:
            text = title_elem.get_text(strip=True)
            match = re.search(r'([A-Z]{2,6}-?\d{2,5})', text, re.I)
            if match:
                return match.group(1).upper()
        
        return ""
    
    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """提取 Tags（類別）"""
        tags = []
        
        tag_sections = soup.select('.panel-block')
        for section in tag_sections:
            strong_elem = section.select_one('strong')
            if strong_elem and '類別' in strong_elem.get_text():
                tag_links = section.select('a')
                for tag_link in tag_links:
                    tag_name = tag_link.get_text(strip=True)
                    if tag_name:
                        tags.append(tag_name)
                break
        
        return tags
    
    def _extract_series(self, soup: BeautifulSoup) -> str:
        """提取系列"""
        tag_sections = soup.select('.panel-block')
        for section in tag_sections:
            strong_elem = section.select_one('strong')
            if strong_elem and '系列' in strong_elem.get_text():
                series_link = section.select_one('a')
                if series_link:
                    return series_link.get_text(strip=True)
        return ""
    
    def _extract_actors(self, soup: BeautifulSoup) -> List[str]:
        """提取演员列表"""
        actors = []
        
        tag_sections = soup.select('.panel-block')
        for section in tag_sections:
            strong_elem = section.select_one('strong')
            if strong_elem and '演員' in strong_elem.get_text():
                actor_links = section.select('a')
                for actor_link in actor_links:
                    actor_name = actor_link.get_text(strip=True)
                    if actor_name and actor_name not in ['♀', '♂']:
                        actors.append(actor_name)
                break
        
        return actors
    
    def _extract_magnets(self, soup: BeautifulSoup) -> List[Dict]:
        """提取磁力链接"""
        magnets = []
        container = soup.select_one('#magnets-content')
        if not container:
            return magnets
        
        items = container.select('.item')
        for item in items:
            try:
                copy_btn = item.select_one('.copy-to-clipboard')
                if not copy_btn:
                    continue
                
                magnet = copy_btn.get('data-clipboard-text', '')
                if not magnet or not magnet.startswith('magnet:'):
                    continue
                
                meta = item.select_one('.meta')
                size_text = meta.get_text(strip=True) if meta else "未知大小"
                size_mb = self._parse_size(size_text)
                
                magnets.append({
                    'magnet': magnet,
                    'size_text': size_text,
                    'size_mb': size_mb,
                })
            except:
                continue
        
        magnets.sort(key=lambda x: x['size_mb'], reverse=True)
        return magnets
    
    def _extract_preview_video(self, soup: BeautifulSoup) -> str:
        """提取预览视频链接"""
        video_elem = soup.select_one('video source, video')
        if video_elem:
            src = video_elem.get('src')
            if src:
                return src
        
        video_container = soup.select_one('.preview-video, .video-preview')
        if video_container:
            video = video_container.select_one('video')
            if video:
                src = video.get('src') or video.get('data-src')
                if src:
                    return src
        
        return ""
    
    def _parse_size(self, size_text: str) -> float:
        """解析文件大小为 MB"""
        match = re.search(r'([\d.]+)\s*(GB|MB)', size_text, re.I)
        if not match:
            return 0
        size = float(match[1])
        unit = match[2].upper()
        return size * 1024 if unit == 'GB' else size
    
    # ==================== 演员搜索 ====================
    
    def search_actor(self, actor_name: str) -> List[Dict]:
        """
        搜索演员
        
        Args:
            actor_name: 演员名字
            
        Returns:
            演员列表，每个演员包含 name, actor_id, url
        """
        encoded_name = quote(actor_name)
        url = f"/search?q={encoded_name}&f=actor"
        
        response = self.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        actors = []
        actor_items = soup.select('.actor-box, .actors .item')
        
        for item in actor_items:
            try:
                link_elem = item.select_one('a')
                if not link_elem:
                    continue
                
                href = link_elem.get('href', '')
                title = link_elem.get('title', '')
                
                if not href.startswith('/actors'):
                    continue
                
                actor_id_match = re.search(r'/actors/([a-zA-Z0-9_-]+)', href)
                if not actor_id_match:
                    continue
                
                actor_id = actor_id_match.group(1)
                
                names = [n.strip() for n in title.split(',')]
                matched_name = None
                
                for name in names:
                    if name == actor_name:
                        matched_name = name
                        break
                
                if not matched_name:
                    continue
                
                actors.append({
                    'name': matched_name,
                    'actor_id': actor_id,
                    'url': urljoin(self.base_url, href),
                })
            except:
                continue
        
        return actors
    
    # ==================== 演员作品（分页） ====================
    
    def get_actor_works_by_page(self, actor_id: str, page: int = 1) -> Dict:
        """
        获取演员作品的code等基础信息（单页）
        
        Args:
            actor_id: 演员 ID
            page: 页码（从1开始）
            
        Returns:
            {
                'page': 1,
                'has_next': True,
                'works': [
                    {
                        'video_id': 'YwG8Ve',
                        'code': 'MIDA-583',
                        'title': '作品标题',
                        'date': '2026-03-04',
                        'rating': '4.57分',
                        'url': 'https://javdb.com/v/YwG8Ve'
                    },
                    ...
                ]
            }
        """
        if page == 1:
            url = f"/actors/{actor_id}"
        else:
            url = f"/actors/{actor_id}?page={page}"
        
        response = self.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        works = []
        items = soup.select('div.item a.box')
        
        for item in items:
            try:
                work = self._parse_work_item(item)
                if work:
                    works.append(work)
            except:
                continue
        
        next_btn = soup.select_one('nav.pagination a[rel="next"]')
        has_next = next_btn is not None
        
        return {
            'page': page,
            'has_next': has_next,
            'works': works,
        }
    
    def get_actor_works_full_by_page(self, actor_id: str, page: int = 1, 
                                      download_images: bool = False) -> Dict:
        """
        获取演员作品的全量信息（单页）
        
        Args:
            actor_id: 演员 ID
            page: 页码（从1开始）
            download_images: 是否下载缩略图
            
        Returns:
            {
                'page': 1,
                'has_next': True,
                'works': [
                    {
                        'video_id': 'YwG8Ve',
                        'code': 'MIDA-583',
                        'title': '作品标题',
                        'tags': [...],
                        'actors': [...],
                        'magnets': [...],
                        'thumbnail_images': [...],
                        ...
                    },
                    ...
                ]
            }
        """
        result = self.get_actor_works_by_page(actor_id, page)
        
        full_works = []
        for work in result['works']:
            try:
                detail = self.get_video_detail(work['video_id'], download_images)
                full_work = DataProcessor.merge_video_detail(work, detail)
                full_works.append(full_work)
            except:
                full_works.append(work)
            time.sleep(config.JAVDB['sleep_time'])
        
        result['works'] = full_works
        return result
    
    def get_actor_works(self, actor_id: str, max_pages: int = 10, 
                        get_details: bool = False, download_images: bool = False) -> List[Dict]:
        """
        获取演员的所有作品（多页）
        
        Args:
            actor_id: 演员 ID
            max_pages: 最大爬取页数
            get_details: 是否获取详情
            download_images: 是否下载缩略图
            
        Returns:
            作品列表
        """
        works = []
        page = 1
        has_next = True
        
        while has_next and page <= max_pages:
            if get_details:
                result = self.get_actor_works_full_by_page(actor_id, page, download_images)
            else:
                result = self.get_actor_works_by_page(actor_id, page)
            
            works.extend(result['works'])
            has_next = result['has_next']
            
            if has_next:
                page += 1
                time.sleep(config.JAVDB['sleep_time'])
        
        for i, work in enumerate(works, 1):
            work['rank'] = i
        
        return works
    
    def _parse_work_item(self, item) -> Optional[Dict]:
        """解析作品项"""
        try:
            title = item.get('title', '')
            href = item.get('href', '')
            
            match = re.search(r'/v/([a-zA-Z0-9]+)', href)
            if not match:
                return None
            
            video_id = match.group(1)
            
            code = ""
            code_elem = item.select_one('.video-title')
            if code_elem:
                code_text = code_elem.get_text(strip=True)
                code_match = re.search(r'([A-Z]{2,6}-?\d{2,5})', code_text, re.I)
                if code_match:
                    code = code_match.group(1).upper()
            
            date = ""
            meta_elem = item.select_one('.meta')
            if meta_elem:
                meta_text = meta_elem.get_text(strip=True)
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', meta_text)
                if date_match:
                    date = date_match.group(1)
            
            rating = ""
            rating_elem = item.select_one('.score, .rating')
            if rating_elem:
                rating = rating_elem.get_text(strip=True)
            
            return {
                'video_id': video_id,
                'code': code,
                'title': title,
                'date': date,
                'rating': rating,
                'url': urljoin(self.base_url, href),
            }
        except:
            return None
    
    # ==================== Tag 作品（分页） ====================
    
    def get_tag_works_by_page(self, tag_id: str, page: int = 1) -> Dict:
        """
        获取Tag搜索结果的code等基础信息（单页）
        
        Args:
            tag_id: Tag ID
            page: 页码（从1开始）
            
        Returns:
            {
                'page': 1,
                'has_next': True,
                'works': [
                    {
                        'video_id': 'YwG8Ve',
                        'code': 'MIDA-583',
                        'title': '作品标题',
                        'date': '2026-03-04',
                        'rating': '4.57分',
                        'url': 'https://javdb.com/v/YwG8Ve'
                    },
                    ...
                ]
            }
        """
        if page == 1:
            url = f"/tags?c1={tag_id}"
        else:
            url = f"/tags?c1={tag_id}&page={page}"
        
        response = self.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        works = []
        items = soup.select('div.item a.box')
        
        for item in items:
            try:
                work = self._parse_work_item(item)
                if work:
                    works.append(work)
            except:
                continue
        
        next_btn = soup.select_one('nav.pagination a[rel="next"]')
        has_next = next_btn is not None
        
        return {
            'page': page,
            'has_next': has_next,
            'works': works,
        }
    
    def get_tag_works_full_by_page(self, tag_id: str, page: int = 1,
                                    download_images: bool = False) -> Dict:
        """
        获取Tag搜索结果的全量信息（单页）
        
        Args:
            tag_id: Tag ID
            page: 页码（从1开始）
            download_images: 是否下载缩略图
            
        Returns:
            {
                'page': 1,
                'has_next': True,
                'works': [
                    {
                        'video_id': 'YwG8Ve',
                        'code': 'MIDA-583',
                        'title': '作品标题',
                        'tags': [...],
                        'actors': [...],
                        'magnets': [...],
                        'thumbnail_images': [...],
                        ...
                    },
                    ...
                ]
            }
        """
        result = self.get_tag_works_by_page(tag_id, page)
        
        full_works = []
        for work in result['works']:
            try:
                detail = self.get_video_detail(work['video_id'], download_images)
                full_work = DataProcessor.merge_video_detail(work, detail)
                full_works.append(full_work)
            except:
                full_works.append(work)
            time.sleep(config.JAVDB['sleep_time'])
        
        result['works'] = full_works
        return result
    
    def get_tag_works(self, tag_id: str, max_pages: int = 10, 
                      get_details: bool = False, download_images: bool = False) -> List[Dict]:
        """
        获取某个 Tag 下的所有作品（多页）
        
        Args:
            tag_id: Tag ID
            max_pages: 最大爬取页数
            get_details: 是否获取详情
            download_images: 是否下载缩略图
            
        Returns:
            作品列表
        """
        works = []
        page = 1
        has_next = True
        
        while has_next and page <= max_pages:
            if get_details:
                result = self.get_tag_works_full_by_page(tag_id, page, download_images)
            else:
                result = self.get_tag_works_by_page(tag_id, page)
            
            works.extend(result['works'])
            has_next = result['has_next']
            
            if has_next:
                page += 1
                time.sleep(config.JAVDB['sleep_time'])
        
        for i, work in enumerate(works, 1):
            work['rank'] = i
        
        return works
    
    # ==================== 多类标签组合搜索 ====================
    
    def search_by_tags(self, page: int = 1, **tag_params) -> Dict:
        """
        多类标签组合搜索（基础信息）
        
        支持多类标签组合，如 c1=23&c3=78
        
        Args:
            page: 页码
            **tag_params: 标签参数，如 c1=23, c3=78, c5=100
            
        Returns:
            {
                'page': 1,
                'has_next': True,
                'tag_params': {'c1': 23, 'c3': 78},
                'works': [
                    {
                        'video_id': 'YwG8Ve',
                        'code': 'MIDA-583',
                        'title': '作品标题',
                        'date': '2026-03-04',
                        'rating': '4.57分',
                        'url': 'https://javdb.com/v/YwG8Ve'
                    },
                    ...
                ]
            }
            
        示例:
            # 搜索第一类第23个标签 + 第三类第78个标签
            result = api.search_by_tags(page=1, c1=23, c3=78)
            
            # 只搜索第五类（服裝）的水手服
            result = api.search_by_tags(page=1, c5=78)
        """
        # 构建 URL 参数
        params = []
        for key, value in tag_params.items():
            if key.startswith('c') and value is not None:
                params.append(f"{key}={value}")
        
        if not params:
            raise ValueError("至少需要提供一个标签参数（如 c1=23）")
        
        query_string = "&".join(params)
        
        if page == 1:
            url = f"/tags?{query_string}"
        else:
            url = f"/tags?{query_string}&page={page}"
        
        response = self.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        works = []
        items = soup.select('div.item a.box')
        
        for item in items:
            try:
                work = self._parse_work_item(item)
                if work:
                    works.append(work)
            except:
                continue
        
        next_btn = soup.select_one('nav.pagination a[rel="next"]')
        has_next = next_btn is not None
        
        return {
            'page': page,
            'has_next': has_next,
            'tag_params': tag_params,
            'works': works,
        }
    
    def search_by_tags_full(self, page: int = 1, download_images: bool = False, 
                            **tag_params) -> Dict:
        """
        多类标签组合搜索（全量信息）
        
        支持多类标签组合，获取作品全量信息
        
        Args:
            page: 页码
            download_images: 是否下载缩略图
            **tag_params: 标签参数，如 c1=23, c3=78
            
        Returns:
            {
                'page': 1,
                'has_next': True,
                'tag_params': {'c1': 23, 'c3': 78},
                'works': [
                    {
                        'video_id': 'YwG8Ve',
                        'code': 'MIDA-583',
                        'title': '作品标题',
                        'tags': [...],
                        'actors': [...],
                        'magnets': [...],
                        ...
                    },
                    ...
                ]
            }
        """
        result = self.search_by_tags(page, **tag_params)
        
        full_works = []
        for work in result['works']:
            try:
                detail = self.get_video_detail(work['video_id'], download_images)
                full_work = DataProcessor.merge_video_detail(work, detail)
                full_works.append(full_work)
            except:
                full_works.append(work)
            time.sleep(config.JAVDB['sleep_time'])
        
        result['works'] = full_works
        return result
    
    # ==================== 搜索功能 ====================
    
    def search_videos(self, keyword: str, page: int = 1) -> List[Dict]:
        """
        搜索视频
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            视频列表
        """
        encoded_keyword = quote(keyword)
        url = f"/search?q={encoded_keyword}&page={page}"
        
        response = self.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        videos = []
        items = soup.select('div.item a.box')
        
        for item in items:
            try:
                work = self._parse_work_item(item)
                if work:
                    videos.append(work)
            except:
                continue
        
        return videos
    
    # ==================== 批量保存功能 ====================
    
    def save_actor_works(self, actor_name: str, max_pages: int = 10, 
                         download_images: bool = True) -> Dict:
        """
        抓取并保存演员所有作品（完整流程）
        
        Args:
            actor_name: 演员名字
            max_pages: 最大页数
            download_images: 是否下载缩略图
            
        Returns:
            完整数据字典
        """
        actors = self.search_actor(actor_name)
        if not actors:
            raise Exception(f"未找到演员: {actor_name}")
        
        actor = actors[0]
        
        works = self.get_actor_works(
            actor['actor_id'],
            max_pages=max_pages,
            get_details=True,
            download_images=download_images
        )
        
        export_data = self.json_exporter.save_actor_works(
            actor_name=actor['name'],
            actor_id=actor['actor_id'],
            works=works,
            actor_url=actor['url']
        )
        
        self.magnet_exporter.save_magnets(works, f"{actor_name}_magnets.txt")
        
        return export_data


# ==================== 便捷函数 ====================

def get_video_detail(video_id: str, download_images: bool = False) -> Dict:
    """
    抓取作品页全量信息
    
    Args:
        video_id: 视频 ID
        download_images: 是否下载缩略图
        
    Returns:
        视频详情字典
    """
    api = JavdbAPI()
    return api.get_video_detail(video_id, download_images)


def get_video_by_code(code: str, download_images: bool = False) -> Optional[Dict]:
    """
    根据番号搜索并获取作品全量信息
    
    Args:
        code: 番号 (如 MIDA-583)
        download_images: 是否下载缩略图
        
    Returns:
        视频详情字典，未找到返回 None
    """
    api = JavdbAPI()
    return api.get_video_by_code(code, download_images)


def search_actor(actor_name: str) -> List[Dict]:
    """
    搜索演员
    
    Args:
        actor_name: 演员名字
        
    Returns:
        演员列表
    """
    api = JavdbAPI()
    return api.search_actor(actor_name)


def get_actor_works_by_page(actor_id: str, page: int = 1) -> Dict:
    """
    获取演员作品的code等基础信息（单页）
    
    Args:
        actor_id: 演员 ID
        page: 页码
        
    Returns:
        包含 page, has_next, works 的字典
    """
    api = JavdbAPI()
    return api.get_actor_works_by_page(actor_id, page)


def get_actor_works_full_by_page(actor_id: str, page: int = 1, 
                                  download_images: bool = False) -> Dict:
    """
    获取演员作品的全量信息（单页）
    
    Args:
        actor_id: 演员 ID
        page: 页码
        download_images: 是否下载缩略图
        
    Returns:
        包含 page, has_next, works 的字典
    """
    api = JavdbAPI()
    return api.get_actor_works_full_by_page(actor_id, page, download_images)


def get_actor_works(actor_name: str, max_pages: int = 10, 
                    get_details: bool = False, download_images: bool = False) -> List[Dict]:
    """
    获取演员作品（多页）
    
    Args:
        actor_name: 演员名字
        max_pages: 最大页数
        get_details: 是否获取详情
        download_images: 是否下载缩略图
        
    Returns:
        作品列表
    """
    api = JavdbAPI()
    
    actors = api.search_actor(actor_name)
    if not actors:
        return []
    
    return api.get_actor_works(
        actors[0]['actor_id'],
        max_pages,
        get_details,
        download_images
    )


def get_tag_works_by_page(tag_id: str, page: int = 1) -> Dict:
    """
    获取Tag搜索结果的code等基础信息（单页）
    
    Args:
        tag_id: Tag ID
        page: 页码
        
    Returns:
        包含 page, has_next, works 的字典
    """
    api = JavdbAPI()
    return api.get_tag_works_by_page(tag_id, page)


def get_tag_works_full_by_page(tag_id: str, page: int = 1,
                                download_images: bool = False) -> Dict:
    """
    获取Tag搜索结果的全量信息（单页）
    
    Args:
        tag_id: Tag ID
        page: 页码
        download_images: 是否下载缩略图
        
    Returns:
        包含 page, has_next, works 的字典
    """
    api = JavdbAPI()
    return api.get_tag_works_full_by_page(tag_id, page, download_images)


def get_tag_works(tag_id: str, max_pages: int = 10, 
                  get_details: bool = False, download_images: bool = False) -> List[Dict]:
    """
    获取 Tag 下的作品（多页）
    
    Args:
        tag_id: Tag ID
        max_pages: 最大页数
        get_details: 是否获取详情
        download_images: 是否下载缩略图
        
    Returns:
        作品列表
    """
    api = JavdbAPI()
    return api.get_tag_works(tag_id, max_pages, get_details, download_images)


def scrape_actor_full(actor_name: str, max_pages: int = 10, 
                      download_images: bool = True) -> Dict:
    """
    全量抓取演员所有信息并保存
    
    Args:
        actor_name: 演员名字
        max_pages: 最大页数
        download_images: 是否下载缩略图
        
    Returns:
        完整数据字典
    """
    api = JavdbAPI()
    return api.save_actor_works(actor_name, max_pages, download_images)


def search_by_tags(page: int = 1, **tag_params) -> Dict:
    """
    多类标签组合搜索（基础信息）
    
    支持多类标签组合，如 c1=23&c3=78
    
    Args:
        page: 页码
        **tag_params: 标签参数，如 c1=23, c3=78, c5=100
        
    Returns:
        {
            'page': 1,
            'has_next': True,
            'tag_params': {'c1': 23, 'c3': 78},
            'works': [...]
        }
        
    示例:
        # 搜索第一类第23个标签 + 第三类第78个标签
        result = search_by_tags(page=1, c1=23, c3=78)
        
        # 只搜索第五类（服裝）的水手服
        result = search_by_tags(page=1, c5=78)
    """
    api = JavdbAPI()
    return api.search_by_tags(page, **tag_params)


def search_by_tags_full(page: int = 1, download_images: bool = False, 
                        **tag_params) -> Dict:
    """
    多类标签组合搜索（全量信息）
    
    支持多类标签组合，获取作品全量信息
    
    Args:
        page: 页码
        download_images: 是否下载缩略图
        **tag_params: 标签参数，如 c1=23, c3=78
        
    Returns:
        {
            'page': 1,
            'has_next': True,
            'tag_params': {'c1': 23, 'c3': 78},
            'works': [...]
        }
    """
    api = JavdbAPI()
    return api.search_by_tags_full(page, download_images, **tag_params)
