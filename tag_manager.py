"""
标签管理模块
负责爬取、管理和查询 JAVDB 的标签分类体系

标签分类格式:
- c1: 基本 (如: 可播放、中字可播放等)
- c2: 年份 (如: 2026、2025等)
- c3: 主題 (如: 淫亂貪賓、出軌等)
- c4: 角色 (如: 高中女生、美少女等)
- c5: 服裝 (如: 水手服、泳裝等)
- c6: 體型 (如: 熟女、巨乳等)
- c7: 行為 (如: 乳交、中出等)

组合搜索示例:
- c1=23&c3=78: 第一类第23个标签 + 第三类第78个标签
"""

import json
import re
from typing import Dict, List, Optional
from pathlib import Path
from urllib.parse import urljoin

from curl_cffi import requests
from bs4 import BeautifulSoup

import config

# 导入加密工具
try:
    from crypto_utils import CryptoUtils, DEFAULT_KEY
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


# 尝试导入登录模块
try:
    from login import JavdbLogin
    HAS_LOGIN = True
except ImportError:
    HAS_LOGIN = False


class TagManager:
    """
    标签管理器
    
    功能:
    - 爬取标签分类数据
    - 保存/加载标签数据库
    - 查询标签信息
    - 构建标签搜索URL
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.tags_db: Dict = {}
        self.db_path = Path(config.OUTPUT_DIR['root']) / 'tags_database.enc'  # 使用加密文件
    
    def fetch_tags(self, force_update: bool = False, auto_login: bool = True) -> Dict:
        """
        爬取标签分类页面建立数据库
        
        Args:
            force_update: 是否强制更新，即使本地已有数据
            auto_login: 是否自动登录（如果未登录）
            
        Returns:
            标签数据库字典
            
            返回格式:
            {
                "categories": {
                    "c1": {
                        "name": "基本",
                        "tags": [
                            {"id": "all", "name": "全部", "value": ""},
                            {"id": 23, "name": "可播放", "value": "playable"},
                            ...
                        ]
                    },
                    "c2": {"name": "年份", "tags": [...]},
                    "c3": {"name": "主題", "tags": [...]},
                    ...
                },
                "updated_at": "2026-03-01 12:00:00"
            }
        """
        # 如果本地已有数据且不强制更新，直接返回
        if not force_update and self.db_path.exists():
            return self.load_tags()
        
        # 如果需要自动登录
        if auto_login and HAS_LOGIN:
            login_helper = JavdbLogin()
            if login_helper.ensure_login():
                # 使用登录后的 session
                self.session = login_helper.session
        
        # 爬取标签页面
        url = "https://javdb.com/tags"
        response = self.session.get(url, timeout=config.JAVDB['timeout'])
        soup = BeautifulSoup(response.text, 'lxml')
        
        tags_db = {
            "categories": {},
            "updated_at": ""
        }
        
        # 查找所有标签分类区域
        # 根据网页结构，标签分类通常有特定的 class 或结构
        category_sections = soup.select('.tag-category, .category-section, .tags-list')
        
        # 如果没有找到特定 class，尝试根据常见结构查找
        if not category_sections:
            # 查找包含标签链接的区域
            all_links = soup.select('a[href*="/tags?c"]')
            
            # 按类别分组
            category_map = {}
            for link in all_links:
                href = link.get('href', '')
                # 提取 cN=xxx 格式
                match = re.search(r'c(\d+)=(\d+)', href)
                if match:
                    cat_num = match.group(1)
                    tag_id = match.group(2)
                    tag_name = link.get_text(strip=True)
                    
                    cat_key = f"c{cat_num}"
                    if cat_key not in category_map:
                        category_map[cat_key] = []
                    
                    category_map[cat_key].append({
                        "id": int(tag_id) if tag_id.isdigit() else tag_id,
                        "name": tag_name,
                        "value": tag_id
                    })
            
            # 根据常见的分类名称映射
            category_names = {
                "c1": "基本",
                "c2": "年份",
                "c3": "主題",
                "c4": "角色",
                "c5": "服裝",
                "c6": "體型",
                "c7": "行為",
            }
            
            for cat_key, tags in category_map.items():
                tags_db["categories"][cat_key] = {
                    "name": category_names.get(cat_key, f"分类{cat_key}"),
                    "tags": sorted(tags, key=lambda x: x["id"] if isinstance(x["id"], int) else 0)
                }
        
        # 添加更新时间
        from datetime import datetime
        tags_db["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存到文件
        self.save_tags(tags_db)
        self.tags_db = tags_db
        
        return tags_db
    
    def save_tags(self, tags_db: Dict = None):
        """
        保存标签数据库到加密文件
        
        Args:
            tags_db: 标签数据库，如果为 None 使用当前缓存的数据
        """
        if tags_db is None:
            tags_db = self.tags_db
        
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        if HAS_CRYPTO:
            # 使用加密保存
            json_str = json.dumps(tags_db, indent=2, ensure_ascii=False)
            encrypted = CryptoUtils.xor_encrypt(json_str, DEFAULT_KEY)
            with open(self.db_path, 'w', encoding='utf-8') as f:
                f.write(encrypted)
        else:
            # 降级到明文保存
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(tags_db, f, indent=2, ensure_ascii=False)
    
    def load_tags(self) -> Dict:
        """
        从加密文件加载标签数据库
        
        Returns:
            标签数据库字典
        """
        if self.db_path.exists():
            try:
                if HAS_CRYPTO:
                    # 尝试解密加载
                    with open(self.db_path, 'r', encoding='utf-8') as f:
                        encrypted_content = f.read()
                    decrypted_str = CryptoUtils.xor_decrypt(encrypted_content, DEFAULT_KEY)
                    self.tags_db = json.loads(decrypted_str)
                else:
                    # 尝试明文加载
                    with open(self.db_path, 'r', encoding='utf-8') as f:
                        self.tags_db = json.load(f)
                return self.tags_db
            except Exception as e:
                # 如果解密失败，尝试明文加载（向后兼容）
                try:
                    with open(self.db_path, 'r', encoding='utf-8') as f:
                        self.tags_db = json.load(f)
                    return self.tags_db
                except:
                    return {}
        return {}
    
    def get_tag_info(self, category: str, tag_id) -> Optional[Dict]:
        """
        获取特定标签的信息
        
        Args:
            category: 分类代码 (如 "c3")
            tag_id: 标签ID (如 78)
            
        Returns:
            标签信息字典，未找到返回 None
            
            返回格式:
            {"id": 78, "name": "水手服", "value": "78"}
        """
        if not self.tags_db:
            self.load_tags()
        
        cat_data = self.tags_db.get("categories", {}).get(category)
        if not cat_data:
            return None
        
        for tag in cat_data.get("tags", []):
            if str(tag.get("id")) == str(tag_id):
                return tag
        
        return None
    
    def search_tag_by_name(self, name: str) -> List[Dict]:
        """
        根据标签名称搜索标签
        
        Args:
            name: 标签名称（支持部分匹配）
            
        Returns:
            匹配的标签列表
            
            返回格式:
            [
                {"category": "c5", "category_name": "服裝", "tag": {"id": 78, "name": "水手服", ...}},
                ...
            ]
        """
        if not self.tags_db:
            self.load_tags()
        
        results = []
        name_lower = name.lower()
        
        for cat_key, cat_data in self.tags_db.get("categories", {}).items():
            for tag in cat_data.get("tags", []):
                if name_lower in tag.get("name", "").lower():
                    results.append({
                        "category": cat_key,
                        "category_name": cat_data.get("name", ""),
                        "tag": tag
                    })
        
        return results
    
    def build_tag_url(self, **kwargs) -> str:
        """
        构建标签搜索 URL
        
        Args:
            **kwargs: 标签参数，如 c1=23, c3=78
            
        Returns:
            完整的搜索 URL
            
        示例:
            build_tag_url(c1=23, c3=78) 
            -> "https://javdb.com/tags?c1=23&c3=78"
        """
        params = []
        for key, value in kwargs.items():
            if key.startswith('c') and value is not None:
                params.append(f"{key}={value}")
        
        if params:
            return f"https://javdb.com/tags?{'&'.join(params)}"
        return "https://javdb.com/tags"
    
    def get_category_list(self) -> List[Dict]:
        """
        获取所有分类列表
        
        Returns:
            分类列表
            
            返回格式:
            [
                {"key": "c1", "name": "基本", "tag_count": 10},
                {"key": "c3", "name": "主題", "tag_count": 50},
                ...
            ]
        """
        if not self.tags_db:
            self.load_tags()
        
        categories = []
        for cat_key, cat_data in self.tags_db.get("categories", {}).items():
            categories.append({
                "key": cat_key,
                "name": cat_data.get("name", ""),
                "tag_count": len(cat_data.get("tags", []))
            })
        
        return sorted(categories, key=lambda x: x["key"])
    
    def print_tags_summary(self):
        """打印标签数据库摘要"""
        if not self.tags_db:
            self.load_tags()
        
        print("=" * 70)
        print("JAVDB 标签分类数据库")
        print("=" * 70)
        print(f"更新时间: {self.tags_db.get('updated_at', '未知')}")
        print()
        
        for cat_key, cat_data in sorted(self.tags_db.get("categories", {}).items()):
            print(f"\n【{cat_key}】{cat_data.get('name', '')} ({len(cat_data.get('tags', []))}个标签)")
            
            # 只显示前10个标签
            tags = cat_data.get("tags", [])[:10]
            for tag in tags:
                print(f"  - {tag['id']}: {tag['name']}")
            
            if len(cat_data.get("tags", [])) > 10:
                print(f"  ... 还有 {len(cat_data.get('tags', [])) - 10} 个标签")


# ==================== 便捷函数 ====================

def fetch_tags(force_update: bool = False, auto_login: bool = True) -> Dict:
    """
    爬取标签分类页面建立数据库
    
    Args:
        force_update: 是否强制更新
        auto_login: 是否自动登录（如果未登录）
        
    Returns:
        标签数据库字典
    """
    manager = TagManager()
    return manager.fetch_tags(force_update, auto_login)


def get_tag_info(category: str, tag_id) -> Optional[Dict]:
    """
    获取特定标签的信息
    
    Args:
        category: 分类代码 (如 "c3")
        tag_id: 标签ID (如 78)
        
    Returns:
        标签信息字典
    """
    manager = TagManager()
    return manager.get_tag_info(category, tag_id)


def search_tag_by_name(name: str) -> List[Dict]:
    """
    根据标签名称搜索标签
    
    Args:
        name: 标签名称
        
    Returns:
        匹配的标签列表
    """
    manager = TagManager()
    return manager.search_tag_by_name(name)


def build_tag_url(**kwargs) -> str:
    """
    构建标签搜索 URL
    
    Args:
        **kwargs: 标签参数，如 c1=23, c3=78
        
    Returns:
        完整的搜索 URL
    """
    manager = TagManager()
    return manager.build_tag_url(**kwargs)


def get_category_list() -> List[Dict]:
    """
    获取所有分类列表
    
    Returns:
        分类列表
    """
    manager = TagManager()
    return manager.get_category_list()
