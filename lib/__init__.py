"""
JAVDB API 库
提供统一的接口访问 JAVDB 平台

使用示例:
    >>> from javdb_api import JavdbAPI
    >>> 
    >>> # 创建 API 实例
    >>> api = JavdbAPI()
    >>> 
    >>> # 获取视频详情
    >>> detail = api.get_video_detail("YwG8Ve")
    >>> 
    >>> # 搜索视频
    >>> videos = api.search_videos("SSIS", max_pages=2)
    >>> 
    >>> # 根据番号搜索
    >>> detail = api.get_video_by_code("MIDA-583")
    >>> 
    >>> # 搜索演员
    >>> actors = api.search_actor("井上もも")
    >>> 
    >>> # 获取演员作品
    >>> works = api.get_actor_works("0R1n3", max_pages=2)
"""

# 核心类
from javdb_api import JavdbAPI

# 适配器
from .adapter_factory import AdapterFactory
from .base_adapter import BaseAdapter
from .javdb_adapter import JavdbAdapter

# 统一 API 接口
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

# 工具类
from .crypto_utils import CryptoUtils, DEFAULT_KEY
from .login import JavdbLogin, login, ensure_login
from .auto_login import AutoLogin, auto_login

# 平台
from .platform import Platform, add_platform_prefix, get_platform_by_name, remove_platform_prefix

__all__ = [
    # 核心类
    'JavdbAPI',
    # 适配器
    'AdapterFactory',
    'BaseAdapter',
    'JavdbAdapter',
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
    # 工具类
    'CryptoUtils',
    'DEFAULT_KEY',
    'JavdbLogin',
    'login',
    'ensure_login',
    'AutoLogin',
    'auto_login',
    # 平台
    'Platform',
    'add_platform_prefix',
    'get_platform_by_name',
    'remove_platform_prefix',
]
