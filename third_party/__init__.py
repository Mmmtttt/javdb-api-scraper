"""
第三方 API 适配器模块

提供统一的接口访问不同的视频平台 API

使用示例:
    >>> from third_party.external_api import search_videos, get_video_detail
    >>> 
    >>> # 搜索视频
    >>> videos = search_videos("SSIS", max_pages=2)
    >>> 
    >>> # 获取视频详情
    >>> detail = get_video_detail("YwG8Ve")
    >>> 
    >>> # 根据番号搜索
    >>> detail = get_video_by_code("MIDA-583")
    >>> 
    >>> # 搜索演员
    >>> actors = search_actor("井上もも")
    >>> 
    >>> # 获取演员作品
    >>> works = get_actor_works("0R1n3", max_pages=2)
"""

from .external_api import (
    search_videos,
    get_video_detail,
    get_video_by_code,
    search_actor,
    get_actor_works,
    get_tag_works,
    search_by_tags,
    download_video_images,
    convert_to_standard_format,
    get_stats,
    get_supported_platforms,
    set_default_platform,
    get_adapter,
)

from .adapter_factory import AdapterFactory
from .base_adapter import BaseAdapter
from .javdb_adapter import JavdbAdapter

__all__ = [
    # API 函数
    'search_videos',
    'get_video_detail',
    'get_video_by_code',
    'search_actor',
    'get_actor_works',
    'get_tag_works',
    'search_by_tags',
    'download_video_images',
    'convert_to_standard_format',
    'get_stats',
    'get_supported_platforms',
    'set_default_platform',
    'get_adapter',
    # 类
    'AdapterFactory',
    'BaseAdapter',
    'JavdbAdapter',
]
