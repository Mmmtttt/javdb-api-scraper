"""
统一的外部 API 接口
提供简洁的 API 调用接口，自动选择默认适配器
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from core.platform import Platform
from third_party.adapter_factory import AdapterFactory
from third_party.base_adapter import BaseAdapter


# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "third_party_config.json"

# 默认平台
DEFAULT_PLATFORM = Platform.JAVDB


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "default_adapter": "javdb",
        "adapters": {
            "javdb": {
                "enabled": True,
                "domain_index": 0
            }
        }
    }


def save_config(config: Dict[str, Any]):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_adapter(platform_name: str = None) -> BaseAdapter:
    """
    获取指定平台的适配器
    
    Args:
        platform_name: 平台名称，如果为None则使用默认平台
        
    Returns:
        适配器实例
    """
    if platform_name is None:
        config = load_config()
        platform_name = config.get("default_adapter", "javdb")
    
    return AdapterFactory.get_adapter_by_name(platform_name)


# ==================== 视频相关 API ====================

def search_videos(keyword: str, max_pages: int = 1, platform: str = None) -> List[Dict[str, Any]]:
    """
    搜索视频
    
    Args:
        keyword: 搜索关键词
        max_pages: 最大搜索页数
        platform: 平台名称，默认使用配置中的默认平台
        
    Returns:
        视频列表
        
    Example:
        >>> videos = search_videos("SSIS", max_pages=2)
        >>> for video in videos:
        ...     print(f"{video['code']}: {video['title']}")
    """
    adapter = get_adapter(platform)
    return adapter.search_videos(keyword, max_pages)


def get_video_detail(video_id: str, platform: str = None) -> Optional[Dict[str, Any]]:
    """
    获取视频详情
    
    Args:
        video_id: 视频ID
        platform: 平台名称
        
    Returns:
        视频详情字典，失败返回None
        
    Example:
        >>> detail = get_video_detail("YwG8Ve")
        >>> print(detail['title'])
        >>> print(detail['magnets'])
    """
    adapter = get_adapter(platform)
    return adapter.get_video_detail(video_id)


def get_video_by_code(code: str, platform: str = None) -> Optional[Dict[str, Any]]:
    """
    根据番号获取视频详情
    
    Args:
        code: 番号（如 MIDA-583）
        platform: 平台名称
        
    Returns:
        视频详情字典，失败返回None
        
    Example:
        >>> detail = get_video_by_code("MIDA-583")
        >>> print(detail['title'])
    """
    adapter = get_adapter(platform)
    
    # JAVDB 适配器有特殊方法
    if hasattr(adapter, 'get_video_by_code'):
        return adapter.get_video_by_code(code)
    
    return None


# ==================== 演员相关 API ====================

def search_actor(actor_name: str, platform: str = None) -> List[Dict[str, Any]]:
    """
    搜索演员
    
    Args:
        actor_name: 演员名字
        platform: 平台名称
        
    Returns:
        演员列表
        
    Example:
        >>> actors = search_actor("井上もも")
        >>> for actor in actors:
        ...     print(f"{actor['actor_name']}: {actor['actor_id']}")
    """
    adapter = get_adapter(platform)
    return adapter.search_actor(actor_name)


def get_actor_works(actor_id: str, page: int = 1, max_pages: int = 1, 
                    full_detail: bool = False, platform: str = None) -> Dict[str, Any]:
    """
    获取演员作品
    
    Args:
        actor_id: 演员ID
        page: 起始页码
        max_pages: 最大页数
        full_detail: 是否获取完整详情
        platform: 平台名称
        
    Returns:
        作品列表和分页信息
        
    Example:
        >>> result = get_actor_works("0R1n3", max_pages=2)
        >>> for work in result['works']:
        ...     print(f"{work['code']}: {work['title']}")
    """
    adapter = get_adapter(platform)
    
    # JAVDB 适配器有特殊方法
    if full_detail and hasattr(adapter, 'get_actor_works_full'):
        return adapter.get_actor_works_full(actor_id, page, max_pages)
    
    return adapter.get_actor_works(actor_id, page, max_pages)


# ==================== 标签相关 API ====================

def get_tag_works(tag_id: str, page: int = 1, max_pages: int = 1, 
                  platform: str = None) -> Dict[str, Any]:
    """
    获取标签作品
    
    Args:
        tag_id: 标签ID
        page: 起始页码
        max_pages: 最大页数
        platform: 平台名称
        
    Returns:
        作品列表和分页信息
    """
    adapter = get_adapter(platform)
    return adapter.get_tag_works(tag_id, page, max_pages)


def search_by_tags(page: int = 1, max_pages: int = 1, platform: str = None, 
                   **tag_params) -> Dict[str, Any]:
    """
    多标签组合搜索
    
    Args:
        page: 起始页码
        max_pages: 最大页数
        platform: 平台名称
        **tag_params: 标签参数，如 c1=23, c3=78
        
    Returns:
        作品列表和分页信息
        
    Example:
        >>> result = search_by_tags(c1=23, c3=78)
        >>> for work in result['works']:
        ...     print(f"{work['code']}: {work['title']}")
    """
    adapter = get_adapter(platform)
    
    # JAVDB 适配器有特殊方法
    if hasattr(adapter, 'search_by_tags'):
        return adapter.search_by_tags(page, max_pages, **tag_params)
    
    return {"page": page, "has_next": False, "works": []}


# ==================== 下载相关 API ====================

def download_video_images(video_id: str, download_dir: str = None, 
                          platform: str = None) -> tuple:
    """
    下载视频缩略图
    
    Args:
        video_id: 视频ID
        download_dir: 下载目录，默认使用配置中的目录
        platform: 平台名称
        
    Returns:
        (成功下载数, 总数)
        
    Example:
        >>> success, total = download_video_images("YwG8Ve", "./images")
        >>> print(f"下载完成: {success}/{total}")
    """
    if download_dir is None:
        download_dir = "./images"
    
    adapter = get_adapter(platform)
    return adapter.download_video_images(video_id, download_dir)


# ==================== 数据转换 API ====================

def convert_to_standard_format(videos: List[Dict[str, Any]], 
                                platform: str = None) -> Dict[str, List[Dict]]:
    """
    将平台数据转换为系统标准格式
    
    Args:
        videos: 视频数据列表
        platform: 平台名称
        
    Returns:
        标准格式的视频和标签数据
        
    Example:
        >>> videos = search_videos("SSIS")
        >>> data = convert_to_standard_format(videos)
        >>> print(f"视频数: {len(data['videos'])}")
        >>> print(f"标签数: {len(data['tags'])}")
    """
    adapter = get_adapter(platform)
    return adapter.convert_to_standard_format(videos)


# ==================== 统计信息 API ====================

def get_stats(platform: str = None) -> Dict[str, Any]:
    """
    获取请求统计
    
    Args:
        platform: 平台名称
        
    Returns:
        请求统计信息
    """
    adapter = get_adapter(platform)
    
    if hasattr(adapter, 'get_stats'):
        return adapter.get_stats()
    
    return {}


# ==================== 便捷函数 ====================

def get_supported_platforms() -> List[str]:
    """
    获取支持的平台列表
    
    Returns:
        平台名称列表
    """
    platforms = AdapterFactory.get_supported_platforms()
    return [p.value for p in platforms]


def set_default_platform(platform_name: str):
    """
    设置默认平台
    
    Args:
        platform_name: 平台名称
    """
    config = load_config()
    config["default_adapter"] = platform_name
    save_config(config)
