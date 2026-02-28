"""
工具函数模块
处理 JSON 导出、图片下载等辅助功能
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import config


class JSONExporter:
    """JSON 导出工具"""
    
    @staticmethod
    def to_json(data: Any, filename: str = None) -> str:
        """
        导出数据为 JSON 字符串
        
        Args:
            data: 要导出的数据
            filename: 可选，保存到文件
            
        Returns:
            JSON 字符串
        """
        json_str = json.dumps(
            data,
            indent=config.JSON_INDENT,
            ensure_ascii=config.JSON_ENSURE_ASCII
        )
        
        if filename:
            output_path = Path(config.OUTPUT_DIR['json']) / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    @staticmethod
    def save_actor_works(actor_name: str, actor_id: str, works: List[Dict], 
                         actor_url: str = "") -> Dict:
        """
        保存演员作品为 JSON
        
        Args:
            actor_name: 演员名字
            actor_id: 演员 ID
            works: 作品列表
            actor_url: 演员页面 URL
            
        Returns:
            导出数据结构
        """
        export_data = {
            'collection_name': f'{actor_name} 作品全集',
            'actor': actor_name,
            'actor_id': actor_id,
            'actor_url': actor_url,
            'total_works': len(works),
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'albums': works,
        }
        
        # 保存完整版
        full_filename = f"{actor_name}_full_works.json"
        JSONExporter.to_json(export_data, full_filename)
        
        # 保存简化版（不含磁力链接）
        simple_works = []
        for work in works:
            simple_work = {
                'rank': work.get('rank', 0),
                'video_id': work.get('video_id', ''),
                'code': work.get('code', ''),
                'title': work.get('title', ''),
                'date': work.get('date', ''),
                'rating': work.get('rating', ''),
                'tags': work.get('tags', []),
                'series': work.get('series', ''),
                'actors': work.get('actors', []),
                'thumbnail_count': len(work.get('thumbnail_images', [])),
                'magnet_count': len(work.get('magnets', [])),
                'work_url': work.get('work_url', ''),
            }
            simple_works.append(simple_work)
        
        simple_data = {
            'collection_name': f'{actor_name} 作品列表',
            'actor': actor_name,
            'total_works': len(simple_works),
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'albums': simple_works,
        }
        
        simple_filename = f"{actor_name}_works_list.json"
        JSONExporter.to_json(simple_data, simple_filename)
        
        return export_data
    
    @staticmethod
    def save_video_detail(video_detail: Dict, filename: str = None) -> str:
        """
        保存单个视频详情为 JSON
        
        Args:
            video_detail: 视频详情字典
            filename: 可选，指定文件名
            
        Returns:
            保存的文件路径
        """
        if not filename:
            code = video_detail.get('code', video_detail.get('video_id', 'unknown'))
            filename = f"{code}_detail.json"
        
        JSONExporter.to_json(video_detail, filename)
        return str(Path(config.OUTPUT_DIR['json']) / filename)


class ImageDownloader:
    """图片下载工具"""
    
    def __init__(self, session):
        """
        初始化下载器
        
        Args:
            session: requests session 对象
        """
        self.session = session
    
    def download_thumbnails(self, code: str, image_urls: List[str]) -> List[str]:
        """
        下载缩略图
        
        Args:
            code: 影片番号（用于创建目录）
            image_urls: 图片 URL 列表
            
        Returns:
            成功下载的文件路径列表
        """
        # 清理 code 中的非法字符
        safe_code = self._sanitize_filename(code)
        
        # 创建目录: output/images/{code}/
        image_dir = Path(config.OUTPUT_DIR['images']) / safe_code
        image_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = []
        
        for i, url in enumerate(image_urls):
            try:
                # 转换高清图 URL (s -> l)
                hd_url = self._convert_to_hd_url(url)
                
                response = self.session.get(hd_url, timeout=10)
                
                # 检查是否有效图片（至少 10KB）
                if response.status_code == 200 and len(response.content) > 10000:
                    # 保存为 00001.jpg, 00002.jpg, ...
                    filename = f"{i+1:05d}.jpg"
                    filepath = image_dir / filename
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded.append(str(filepath))
                    
                time.sleep(0.3)  # 避免请求过快
                
            except Exception as e:
                continue
        
        return downloaded
    
    @staticmethod
    def _convert_to_hd_url(url: str) -> str:
        """
        将缩略图 URL 转换为高清图 URL
        
        Args:
            url: 原始 URL (包含 _s_)
            
        Returns:
            高清图 URL (包含 _l_)
        """
        # 将 _s_ 替换为 _l_
        if '_s_' in url:
            return url.replace('_s_', '_l_')
        return url
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """清理文件名中的非法字符"""
        import re
        # 移除或替换非法字符
        return re.sub(r'[\\/*?:"<>|]', "_", filename)


class MagnetExporter:
    """磁力链接导出工具"""
    
    @staticmethod
    def save_magnets(works: List[Dict], filename: str) -> str:
        """
        保存磁力链接到文本文件
        
        Args:
            works: 作品列表
            filename: 文件名
            
        Returns:
            保存的文件路径
        """
        output_path = Path(config.OUTPUT_DIR['magnets']) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for work in works:
                code = work.get('code', work.get('video_id', 'unknown'))
                magnets = work.get('magnets', [])
                
                for magnet in magnets:
                    size_text = magnet.get('size_text', '未知大小')
                    magnet_link = magnet.get('magnet', '')
                    if magnet_link:
                        f.write(f"{code}\t{size_text}\t{magnet_link}\n")
        
        return str(output_path)
    
    @staticmethod
    def save_magnet_list(magnets: List[str], filename: str) -> str:
        """
        保存纯磁力链接列表
        
        Args:
            magnets: 磁力链接列表
            filename: 文件名
            
        Returns:
            保存的文件路径
        """
        output_path = Path(config.OUTPUT_DIR['magnets']) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for magnet in magnets:
                f.write(f"{magnet}\n")
        
        return str(output_path)


class DataProcessor:
    """数据处理工具"""
    
    @staticmethod
    def merge_video_detail(basic_info: Dict, detail: Dict) -> Dict:
        """
        合并基础信息和详细信息
        
        Args:
            basic_info: 基础信息（来自列表页）
            detail: 详细信息（来自详情页）
            
        Returns:
            合并后的完整信息
        """
        return {
            'video_id': basic_info.get('video_id', detail.get('video_id', '')),
            'code': detail.get('code', basic_info.get('code', '')),
            'title': detail.get('title', basic_info.get('title', '')),
            'date': basic_info.get('date', ''),
            'rating': basic_info.get('rating', ''),
            'tags': detail.get('tags', []),
            'series': detail.get('series', ''),
            'actors': detail.get('actors', []),
            'magnets': detail.get('magnets', []),
            'thumbnail_images': detail.get('thumbnail_images', []),
            'preview_video': detail.get('preview_video', ''),
            'work_url': detail.get('url', basic_info.get('url', '')),
        }
    
    @staticmethod
    def extract_hd_thumbnails(video_id: str, soup) -> List[str]:
        """
        提取高清缩略图 URL
        
        Args:
            video_id: 视频 ID
            soup: BeautifulSoup 对象
            
        Returns:
            高清缩略图 URL 列表
        """
        images = []
        
        # 查找预览图区域
        preview_container = soup.select_one('.preview-images, .video-images, .tile-images')
        if preview_container:
            img_links = preview_container.select('img, a.tile-item')
            for img in img_links:
                src = img.get('src') or img.get('data-src')
                if src:
                    # 转换为高清图 URL
                    hd_url = src.replace('_s_', '_l_')
                    images.append(hd_url)
        
        # 如果页面没有直接显示，构建标准高清 URL
        if not images:
            prefix = video_id[:2].lower()
            for i in range(10):  # 最多尝试10张
                # 使用 _l_ 获取高清图
                url = f"https://c0.jdbstatic.com/samples/{prefix}/{video_id}_l_{i}.jpg"
                images.append(url)
        
        return images
