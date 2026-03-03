"""
测试配置文件
在文件开头配置所有测试参数，方便快速修改和测试

================================================================================
=========================== 7个核心功能测试配置 =================================
================================================================================
"""

# ============================================================================
# 7个核心功能测试配置
# ============================================================================

# 核心功能1: 搜索演员的作品ID列表（支持起始/结束个数，平台选择）
CORE_API_SEARCH_ACTOR_WORKS_TESTS = [
    {
        "name": "【核心功能1】搜索演员作品 - 永野一夏前20个",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "start": 0,
        "end": 20,
        "platform": None,  # None=默认javdb, "javdb" 或 "javbus"
        "enabled": True,
    },
    {
        "name": "【核心功能1】搜索演员作品 - 永野一夏第21-40个",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "start": 20,
        "end": 40,
        "platform": None,
        "enabled": False,  # 默认关闭
    },
    {
        "name": "【核心功能1】搜索演员作品 - JavBus平台",
        "actor_id": "star_id_here",  # 需要替换为实际的JavBus演员ID
        "actor_name": "演员名字",
        "start": 0,
        "end": 20,
        "platform": "javbus",
        "enabled": False,  # 默认关闭
    },
]

# 核心功能2: 通过作品ID获取作品详细信息（平台选择）
CORE_API_VIDEO_DETAIL_TESTS = [
    {
        "name": "【核心功能2】获取作品详情 - JAVDB",
        "video_id": "YwG8Ve",
        "platform": None,  # None=默认javdb
        "enabled": True,
    },
    {
        "name": "【核心功能2】获取作品详情 - JavBus",
        "video_id": "SSIS-865",
        "platform": "javbus",
        "enabled": True,
    },
]

# 核心功能3: 通过作品ID获取并下载高清预览图和封面（平台选择）
CORE_API_DOWNLOAD_IMAGES_TESTS = [
    {
        "name": "【核心功能3】下载作品图片 - JAVDB",
        "video_id": "YwG8Ve",
        "output_dir": "test/测试3/images",
        "platform": None,
        "enabled": True,
    },
    {
        "name": "【核心功能3】下载作品图片 - JavBus",
        "video_id": "SSIS-865",
        "output_dir": "test/测试3/images",
        "platform": "javbus",
        "enabled": False,  # 默认关闭
    },
]

# 核心功能4: 通过标签内容搜索作品ID列表（多标签，起始/结束个数，平台选择）
CORE_API_TAG_SEARCH_TESTS = [
    {
        "name": "【核心功能4】标签搜索 - 单标签",
        "tag_names": ["美少女"],
        "start": 0,
        "end": 20,
        "platform": None,
        "enabled": True,
    },
    {
        "name": "【核心功能4】标签搜索 - 多标签组合",
        "tag_names": ["美少女", "水手服"],
        "start": 0,
        "end": 20,
        "platform": None,
        "enabled": False,  # 默认关闭
    },
    {
        "name": "【核心功能4】标签搜索 - 第21-40个结果",
        "tag_names": ["美少女"],
        "start": 20,
        "end": 40,
        "platform": None,
        "enabled": False,  # 默认关闭
    },
]

# 核心功能5: 搜索已登录用户的所有清单名称（仅javdb）
CORE_API_USER_LISTS_TESTS = [
    {
        "name": "【核心功能5】获取用户清单列表",
        "enabled": True,
    },
]

# 核心功能6: 在某清单中搜索所有作品ID列表（起始/结束个数，仅javdb）
CORE_API_LIST_WORKS_TESTS = [
    {
        "name": "【核心功能6】获取清单作品 - 前20个",
        "list_id": "0W97k",  # 需要替换为实际的清单ID
        "start": 0,
        "end": 20,
        "enabled": False,  # 默认关闭，需要实际的清单ID
    },
    {
        "name": "【核心功能6】获取清单作品 - 第21-40个",
        "list_id": "0W97k",
        "start": 20,
        "end": 40,
        "enabled": False,
    },
]

# 核心功能7: 支持登录（仅javdb）
CORE_API_LOGIN_TESTS = [
    {
        "name": "【核心功能7】登录测试",
        "enabled": False,  # 默认关闭，需要手动开启
    },
]


# ================================================================================
# ============================= 其他测试配置 ======================================
# ================================================================================

# 登录配置
LOGIN_CONFIG = {
    "enabled": True,  # 是否需要登录
    "auto_login": False,  # 是否使用自动登录（打开浏览器）
    "use_existing_cookies": True,  # 是否使用已有的 cookies.json
}

# 视频详情测试
VIDEO_DETAIL_TESTS = [
    {
        "name": "测试视频详情 - 永野一夏作品",
        "video_id": "YwG8Ve",
        "download_images": True,
        "enabled": True,
    },
]

# 番号搜索测试
CODE_SEARCH_TESTS = [
    {
        "name": "测试番号搜索 - MIDA-583",
        "code": "MIDA-583",
        "enabled": True,
    },
]

# 视频搜索测试
VIDEO_SEARCH_TESTS = [
    {
        "name": "测试视频搜索 - SSIS",
        "keyword": "SSIS",
        "max_pages": 1,
        "enabled": True,
    },
]

# 演员搜索测试
ACTOR_SEARCH_TESTS = [
    {
        "name": "测试演员搜索 - 井上もも",
        "actor_name": "井上もも",
        "enabled": True,
    },
    {
        "name": "测试演员搜索 - 永野一夏",
        "actor_name": "永野一夏",
        "enabled": True,
    },
]

# 演员作品测试
ACTOR_WORKS_TESTS = [
    {
        "name": "测试演员作品 - 永野一夏第一页",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "max_pages": 1,
        "get_details": False,
        "download_images": False,
        "enabled": True,
    },
    {
        "name": "测试演员作品 - 永野一夏全量抓取（第一页详情+图片）",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "max_pages": 1,
        "get_details": True,
        "download_images": True,
        "enabled": False,  # 默认关闭，需要时开启
    },
]

# 标签筛选测试
TAG_FILTER_TESTS = [
    {
        "name": "测试标签筛选 - 永野一夏的'美少女'标签作品",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "tag_names": ["美少女"],
        "max_pages": 1,
        "get_details": True,
        "download_images": False,
        "save_temp": True,
        "enabled": True,
    },
    {
        "name": "测试标签筛选 - 永野一夏的多标签组合",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "tag_names": ["美少女", "單體作品"],
        "max_pages": 1,
        "get_details": True,
        "download_images": False,
        "save_temp": True,
        "enabled": False,  # 默认关闭，需要时开启
    },
]

# 标签搜索测试
TAG_SEARCH_TESTS = [
    {
        "name": "测试标签搜索 - 美少女",
        "tag_id": "c1=23",
        "max_pages": 1,
        "enabled": True,
    },
]

# 磁力链接测试
MAGNET_TESTS = [
    {
        "name": "测试磁力链接获取",
        "video_id": "YwG8Ve",
        "enabled": True,
    },
]

# 图片下载测试
IMAGE_DOWNLOAD_TESTS = [
    {
        "name": "测试图片下载 - 永野一夏作品",
        "video_id": "YwG8Ve",
        "download_dir": "test/images/javdb",  # 下载到 test 目录
        "enabled": True,
    },
    {
        "name": "测试图片下载 - 多图片作品 SSIS-001",
        "video_id": "SSIS-001",
        "download_dir": "test/images/javdb",
        "enabled": False,  # 默认关闭，需要时开启
    },
]

# 通用图片下载测试（使用 download_video_images API）
GENERAL_IMAGE_DOWNLOAD_TESTS = [
    {
        "name": "测试通用图片下载 API",
        "video_id": "Test-Video",
        "image_urls": [
            {"url": "https://www.javbus.com/pics/cover/475i_b.jpg", "filename": "cover.jpg"},
            {"url": "https://www.javbus.com/pics/sample/9wuo_1.jpg", "filename": "sample_01.jpg"},
        ],
        "headers": {
            "Referer": "https://www.javbus.com/"
        },
        "download_dir": "test/images/general",
        "enabled": False,  # 默认关闭，需要有效的图片 URL
    },
]

# JavBus 测试配置
JAVBUS_CONFIG = {
    "enabled": True,  # 是否启用 JavBus 测试
    "base_url": "https://www.javbus.com",
    "proxy": None,  # 代理设置，如 "http://127.0.0.1:7890"
}

# JavBus 搜索测试
JAVBUS_SEARCH_TESTS = [
    {
        "name": "JavBus 搜索 - 有码影片 SSIS-865",
        "keyword": "SSIS-865",
        "movie_type": "normal",  # normal=有码, uncensored=无码
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "JavBus 搜索 - 无码影片",
        "keyword": "ABP",
        "movie_type": "uncensored",
        "max_pages": 1,
        "enabled": False,  # 默认关闭
    },
]

# JavBus 详情测试
JAVBUS_DETAIL_TESTS = [
    {
        "name": "JavBus 详情 - ABP-123",
        "video_id": "ABP-123",
        "movie_type": "normal",
        "enabled": True,
    },
]

# JavBus 磁力链接测试
JAVBUS_MAGNET_TESTS = [
    {
        "name": "JavBus 磁力链接 - ABP-123",
        "video_id": "ABP-123",
        "movie_type": "normal",
        "enabled": True,
    },
]

# JavBus 图片下载测试
JAVBUS_IMAGE_TESTS = [
    {
        "name": "JavBus 图片下载 - 封面和样品图",
        "video_id": "ABP-123",
        "movie_type": "normal",
        "download_dir": "test/images/javbus",
        "enabled": True,
    },
]

# JavBus 演员作品测试
JAVBUS_ACTOR_TESTS = [
    {
        "name": "JavBus 演员作品 - 获取演员作品列表",
        "actor_id": "star_id_here",  # 需要替换为实际的演员ID
        "max_pages": 1,
        "enabled": False,  # 默认关闭，需要实际的演员ID
    },
]


# ================================================================================
# ============================= 结果和日志配置 ====================================
# ================================================================================

# 结果保存配置
RESULT_CONFIG = {
    "save_to_file": True,  # 是否保存结果到文件
    "output_dir": "test_results",  # 结果输出目录
    "output_format": "json",  # 输出格式: json, txt
    "verbose": True,  # 是否打印详细信息
    "test_output_dirs": {
        "core_search_actor_works": "test/测试1/results",
        "core_video_detail": "test/测试2/results",
        "core_download_images": "test/测试3/results",
        "core_tag_search": "test/测试4/results",
        "core_user_lists": "test/测试5/results",
        "core_list_works": "test/测试6/results",
        "core_login": "test/测试7/results",
        "video_detail": "test/其他测试/results",
        "code_search": "test/其他测试/results",
        "video_search": "test/其他测试/results",
        "actor_search": "test/其他测试/results",
        "actor_works": "test/其他测试/results",
        "tag_filter": "test/其他测试/results",
        "tag_search": "test/其他测试/results",
        "magnet": "test/其他测试/results",
        "image_download": "test/其他测试/results",
        "general_image_download": "test/其他测试/results",
        "javbus_search": "test/javbus/results",
        "javbus_detail": "test/javbus/results",
        "javbus_magnet": "test/javbus/results",
        "javbus_image": "test/javbus/results",
        "javbus_actor": "test/javbus/results",
    }
}

# 超时配置
TIMEOUT_CONFIG = {
    "request_timeout": 30,  # 请求超时时间（秒）
    "retry_times": 3,  # 重试次数
    "retry_delay": 2,  # 重试延迟（秒）
}

# 重试配置
RETRY_CONFIG = {
    "max_retries": 3,
    "retry_delay": 2,
    "retry_exceptions": ["ConnectionError", "TimeoutError"],
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",  # 日志级别: DEBUG, INFO, WARNING, ERROR
    "save_to_file": True,
    "log_dir": "logs",
    "log_file": "test.log",
}


# ================================================================================
# ============================= 辅助函数 ==========================================
# ================================================================================

def get_enabled_tests(test_list: list) -> list:
    """获取启用的测试列表"""
    return [t for t in test_list if t.get("enabled", True)]


def get_test_summary() -> dict:
    """获取测试摘要"""
    
    # 7个核心功能测试
    core_tests = {
        "search_actor_works": len(get_enabled_tests(CORE_API_SEARCH_ACTOR_WORKS_TESTS)),
        "video_detail": len(get_enabled_tests(CORE_API_VIDEO_DETAIL_TESTS)),
        "download_images": len(get_enabled_tests(CORE_API_DOWNLOAD_IMAGES_TESTS)),
        "tag_search": len(get_enabled_tests(CORE_API_TAG_SEARCH_TESTS)),
        "user_lists": len(get_enabled_tests(CORE_API_USER_LISTS_TESTS)),
        "list_works": len(get_enabled_tests(CORE_API_LIST_WORKS_TESTS)),
        "login": len(get_enabled_tests(CORE_API_LOGIN_TESTS)),
    }
    
    # 其他测试
    other_tests = {
        "video_detail": len(get_enabled_tests(VIDEO_DETAIL_TESTS)),
        "code_search": len(get_enabled_tests(CODE_SEARCH_TESTS)),
        "video_search": len(get_enabled_tests(VIDEO_SEARCH_TESTS)),
        "actor_search": len(get_enabled_tests(ACTOR_SEARCH_TESTS)),
        "actor_works": len(get_enabled_tests(ACTOR_WORKS_TESTS)),
        "tag_filter": len(get_enabled_tests(TAG_FILTER_TESTS)),
        "tag_search": len(get_enabled_tests(TAG_SEARCH_TESTS)),
        "magnet": len(get_enabled_tests(MAGNET_TESTS)),
        "image_download": len(get_enabled_tests(IMAGE_DOWNLOAD_TESTS)),
        "general_image_download": len(get_enabled_tests(GENERAL_IMAGE_DOWNLOAD_TESTS)),
    }
    
    # JavBus 测试
    javbus_tests = {
        "search": len(get_enabled_tests(JAVBUS_SEARCH_TESTS)),
        "detail": len(get_enabled_tests(JAVBUS_DETAIL_TESTS)),
        "magnet": len(get_enabled_tests(JAVBUS_MAGNET_TESTS)),
        "image": len(get_enabled_tests(JAVBUS_IMAGE_TESTS)),
        "actor": len(get_enabled_tests(JAVBUS_ACTOR_TESTS)),
    }
    
    return {
        "core_api_tests": core_tests,
        "other_tests": other_tests,
        "javbus_tests": javbus_tests,
        "total_core": sum(core_tests.values()),
        "total_other": sum(other_tests.values()),
        "total_javbus": sum(javbus_tests.values()),
        "total": sum(core_tests.values()) + sum(other_tests.values()) + sum(javbus_tests.values()),
    }


if __name__ == "__main__":
    # 打印测试摘要
    summary = get_test_summary()
    print("=" * 60)
    print("测试配置摘要")
    print("=" * 60)
    print(f"\n【7个核心功能测试】")
    for name, count in summary["core_api_tests"].items():
        print(f"  {name}: {count} 个")
    print(f"  小计: {summary['total_core']} 个")
    
    print(f"\n【其他测试】")
    for name, count in summary["other_tests"].items():
        print(f"  {name}: {count} 个")
    print(f"  小计: {summary['total_other']} 个")
    
    print(f"\n【JavBus 测试】")
    for name, count in summary["javbus_tests"].items():
        print(f"  {name}: {count} 个")
    print(f"  小计: {summary['total_javbus']} 个")
    
    print(f"\n{'=' * 60}")
    print(f"总计: {summary['total']} 个测试")
    print("=" * 60)
