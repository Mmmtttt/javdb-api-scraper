"""
测试配置文件
在文件开头配置所有测试参数，方便快速修改和测试
"""

# ============================================================================
# 测试配置表
# ============================================================================

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
        "download_images": False,
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
        "download_dir": None,  # None 表示使用默认目录
        "enabled": True,
    },
]

# ============================================================================
# 测试结果保存配置
# ============================================================================

RESULT_CONFIG = {
    "save_results": True,  # 是否保存测试结果
    "output_dir": "test/output",  # 结果输出目录
    "save_json": True,  # 是否保存 JSON 格式结果
    "save_text": True,  # 是否保存文本格式结果
    "include_timestamp": True,  # 文件名是否包含时间戳
    "verbose": True,  # 是否输出详细信息
}

# ============================================================================
# 其他配置
# ============================================================================

# 测试超时设置
TIMEOUT_CONFIG = {
    "request_timeout": 30,  # 单个请求超时时间（秒）
    "test_timeout": 300,  # 整个测试超时时间（秒）
}

# 重试配置
RETRY_CONFIG = {
    "max_retries": 3,  # 最大重试次数
    "retry_delay": 2,  # 重试延迟（秒）
}

# 日志配置
LOG_CONFIG = {
    "log_level": "INFO",  # 日志级别: DEBUG, INFO, WARNING, ERROR
    "log_to_file": True,  # 是否记录到文件
    "log_file": "test/test.log",  # 日志文件路径
}

# ============================================================================
# 辅助函数
# ============================================================================

def get_enabled_tests(test_list):
    """
    获取启用的测试项
    
    Args:
        test_list: 测试列表
        
    Returns:
        启用的测试项列表
    """
    return [test for test in test_list if test.get("enabled", False)]


def get_test_summary():
    """
    获取测试摘要
    
    Returns:
        测试摘要字典
    """
    return {
        "video_detail": len(get_enabled_tests(VIDEO_DETAIL_TESTS)),
        "code_search": len(get_enabled_tests(CODE_SEARCH_TESTS)),
        "video_search": len(get_enabled_tests(VIDEO_SEARCH_TESTS)),
        "actor_search": len(get_enabled_tests(ACTOR_SEARCH_TESTS)),
        "actor_works": len(get_enabled_tests(ACTOR_WORKS_TESTS)),
        "tag_filter": len(get_enabled_tests(TAG_FILTER_TESTS)),
        "tag_search": len(get_enabled_tests(TAG_SEARCH_TESTS)),
        "magnet": len(get_enabled_tests(MAGNET_TESTS)),
        "image_download": len(get_enabled_tests(IMAGE_DOWNLOAD_TESTS)),
    }


if __name__ == "__main__":
    # 打印测试摘要
    print("=" * 70)
    print("📋 测试配置摘要")
    print("=" * 70)
    
    summary = get_test_summary()
    total = sum(summary.values())
    
    print(f"\n启用的测试项总数: {total}\n")
    
    for test_type, count in summary.items():
        print(f"  {test_type}: {count}")
    
    print("\n" + "=" * 70)
