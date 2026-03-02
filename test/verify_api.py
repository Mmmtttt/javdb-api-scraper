"""
API 验证测试脚本
验证所有 API 接口是否正确调用并返回预期格式

测试内容:
1. 视频详情抓取 - get_video_detail
2. 根据番号搜索 - get_video_by_code
3. 演员搜索 - search_actor
4. 演员作品抓取（分页）- get_actor_works_by_page
5. 演员作品全量抓取（分页）- get_actor_works_full_by_page
6. 标签搜索 - search_by_tags
7. 标签搜索全量 - search_by_tags_full
8. 标签管理 - get_tag_info, search_tag_by_name
9. 演员作品标签筛选 - get_actor_works_with_tags
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from javdb_api import (
    JavdbAPI,
    get_video_detail,
    get_video_by_code,
    search_actor,
    get_actor_works_by_page,
    get_actor_works_full_by_page,
    search_by_tags,
    search_by_tags_full,
    get_tag_by_name,
    get_tag_by_id,
    search_tags_by_keyword,
    convert_to_traditional,
    get_want_watch_videos,
    get_watched_videos,
    get_user_lists,
    get_list_detail,
    get_want_watch_videos_all,
    get_watched_videos_all,
    get_list_detail_all,
    get_user_lists_all,
)
# from tag_manager import (  # 标签管理功能已移至 lib
#     get_tag_info,
#     search_tag_by_name,
#     get_category_list,
# )

TEST_OUTPUT_DIR = Path(__file__).parent / "output"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEST_IMAGES_DIR = TEST_OUTPUT_DIR / "images"
TEST_JSON_DIR = TEST_OUTPUT_DIR / "json"
TEST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
TEST_JSON_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 测试配置表 - 在这里配置要测试的内容
# ============================================================================

# 视频详情测试配置
VIDEO_DETAIL_TESTS = [
    {
        "name": "测试视频详情1",
        "video_id": "YwG8Ve",
        "download_images": False,
        "enabled": True,
    },
    {
        "name": "测试视频详情2",
        "video_id": "RqGjB2",
        "download_images": False,
        "enabled": False,
    },
]

# 番号搜索测试配置
CODE_SEARCH_TESTS = [
    {
        "name": "测试番号搜索1",
        "code": "MIDA-583",
        "enabled": True,
    },
    {
        "name": "测试番号搜索2",
        "code": "SSIS-001",
        "enabled": False,
    },
]

# 演员搜索测试配置
ACTOR_SEARCH_TESTS = [
    {
        "name": "测试演员搜索1",
        "actor_name": "井上もも",
        "enabled": True,
    },
    {
        "name": "测试演员搜索2",
        "actor_name": "永野一夏",
        "enabled": True,
    },
]

# 演员作品测试配置
ACTOR_WORKS_TESTS = [
    {
        "name": "测试演员作品1 - 井上もも第一页",
        "actor_id": "0R1n3",
        "actor_name": "井上もも",
        "page": 1,
        "enabled": True,
    },
    {
        "name": "测试演员作品2 - 永野一夏第一页",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "page": 1,
        "enabled": True,
    },
]

# 演员作品全量测试配置
ACTOR_WORKS_FULL_TESTS = [
    {
        "name": "测试演员全量作品1 - 井上もも",
        "actor_id": "0R1n3",
        "actor_name": "井上もも",
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试演员全量作品2 - 永野一夏",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "max_pages": 1,
        "enabled": True,
    },
]

# 演员作品标签筛选测试配置
ACTOR_TAG_FILTER_TESTS = [
    {
        "name": "测试标签筛选1 - 永野一夏的美少女作品",
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
        "name": "测试标签筛选2 - 永野一夏的多标签组合",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "tag_names": ["美少女", "單體作品"],
        "max_pages": 1,
        "get_details": True,
        "download_images": False,
        "save_temp": True,
        "enabled": False,
    },
]

# 标签搜索测试配置
TAG_SEARCH_TESTS = [
    {
        "name": "测试标签搜索1 - 最简单方式（直接标签名）",
        "tag_params": {"淫亂真實": ""},
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试标签搜索2 - 使用tags列表",
        "tag_params": {"tags": ["淫亂真實", "水手服"]},
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试标签搜索3 - 简体自动转繁体",
        "tag_params": {"淫乱真实": ""},
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试标签搜索4 - 带分类前缀",
        "tag_params": {"tag_主題": "淫亂真實"},
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试标签搜索5 - 传统ID模式",
        "tag_params": {"c1": 23},
        "max_pages": 1,
        "enabled": True,
    },
]

# 标签全量搜索测试配置
TAG_SEARCH_FULL_TESTS = [
    {
        "name": "测试标签全量搜索1 - 最简单方式",
        "tag_params": {"淫亂真實": ""},
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试标签全量搜索2 - 使用tags列表",
        "tag_params": {"tags": ["美少女", "水手服"]},
        "max_pages": 1,
        "enabled": True,
    },
]

# 演员作品全量抓取+图片下载测试配置
ACTOR_WORKS_FULL_IMAGE_TESTS = [
    {
        "name": "测试全量抓取+图片 - 永野一夏第一页",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "page": 1,
        "enabled": False,
    },
]

# 高清预览图下载测试配置
HD_PREVIEW_DOWNLOAD_TESTS = [
    {
        "name": "测试高清预览图下载",
        "video_id": "YwG8Ve",
        "code": "MIDA-583",
        "enabled": True,
    },
]

# 登录测试配置
LOGIN_TESTS = [
    {
        "name": "测试登录状态检查",
        "enabled": True,
    },
    {
        "name": "测试自动登录",
        "auto_login": True,  # 改为 True
        "enabled": True,  # 改为 True
    },
]

# 标签管理测试配置
TAG_MANAGER_TESTS = [
    {
        "name": "测试标签名称查询 - 美少女",
        "tag_name": "美少女",
        "expected_id": "c1=23",
        "enabled": True,
    },
    {
        "name": "测试标签名称查询 - 简体转繁体",
        "tag_name": "淫乱真实",  # 简体
        "expected_id": "c1=23",
        "enabled": True,
    },
    {
        "name": "测试标签ID查询",
        "tag_id": "c1=23",
        "expected_name": "淫亂真實",
        "enabled": True,
    },
    {
        "name": "测试标签关键词搜索",
        "keyword": "女",
        "enabled": True,
    },
]

# 用户清单测试配置
USER_LIST_TESTS = [
    {
        "name": "测试获取想看清单",
        "test_type": "want_watch",
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试获取看过清单（全部作品ID）",
        "test_type": "watched_all",
        "max_pages": 5,
        "enabled": True,
    },
    {
        "name": "测试获取用户清单列表（全部）",
        "test_type": "user_lists_all",
        "max_pages": 5,
        "enabled": True,
    },
    {
        "name": "测试获取清单详细内容",
        "test_type": "list_detail",
        "list_id": "0W97k",
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试获取清单全部作品ID",
        "test_type": "list_detail_all",
        "list_id": "0W97k",
        "max_pages": 5,
        "enabled": True,
    },
]

# ============================================================================
# 旧版配置（保留兼容性）
# ============================================================================

TEST_DATA = {
    "video_id": "YwG8Ve",
    "code": "MIDA-583",
    "actor_name": "井上もも",
    "actor_id": "0R1n3",
    "tag_c3": 78,
    "tag_name": "水手服",
}

# 额外的演员测试数据
EXTRA_ACTORS = [
    {"name": "井上もも", "id": "0R1n3"},
    {"name": "永野一夏", "id": "NeOr"},
]

test_results = []


def log_test(name: str, passed: bool, message: str = "", data: any = None):
    """记录测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    result = {
        "test": name,
        "passed": passed,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    test_results.append(result)
    
    print(f"\n{status} | {name}")
    if message:
        print(f"     {message}")
    if data and passed:
        if isinstance(data, dict):
            for key, value in list(data.items())[:5]:
                if isinstance(value, list):
                    print(f"     - {key}: {value[:3]}{'...' if len(value) > 3 else ''}")
                elif isinstance(value, str) and len(value) > 50:
                    print(f"     - {key}: {value[:50]}...")
                else:
                    print(f"     - {key}: {value}")


def validate_video_detail(detail: dict, test_name: str) -> bool:
    """验证视频详情格式"""
    required_fields = ["video_id", "code", "title", "date", "actors", "tags", "magnets"]
    missing = [f for f in required_fields if f not in detail]
    
    if missing:
        log_test(test_name, False, f"缺少字段: {missing}")
        return False
    
    if not detail.get("code"):
        log_test(test_name, False, "code 为空")
        return False
    
    if not detail.get("title"):
        log_test(test_name, False, "title 为空")
        return False
    
    if not isinstance(detail.get("actors"), list):
        log_test(test_name, False, "actors 不是列表")
        return False
    
    if not isinstance(detail.get("tags"), list):
        log_test(test_name, False, "tags 不是列表")
        return False
    
    if not isinstance(detail.get("magnets"), list):
        log_test(test_name, False, "magnets 不是列表")
        return False
    
    return True


def test_1_get_video_detail():
    """测试1: 抓取作品页全量信息"""
    print("\n" + "=" * 70)
    print("测试1: get_video_detail - 抓取作品页全量信息")
    print("=" * 70)
    
    try:
        detail = get_video_detail(TEST_DATA["video_id"], download_images=False)
        
        if not detail:
            log_test("get_video_detail", False, "返回 None")
            return None
        
        if validate_video_detail(detail, "get_video_detail"):
            log_test("get_video_detail", True, 
                    f"成功获取: {detail.get('code')} - {detail.get('title')[:30]}...", 
                    detail)
            return detail
    except Exception as e:
        log_test("get_video_detail", False, f"异常: {str(e)}")
    
    return None


def test_2_get_video_by_code():
    """测试2: 根据番号搜索并获取详情"""
    print("\n" + "=" * 70)
    print("测试2: get_video_by_code - 根据番号搜索")
    print("=" * 70)
    
    try:
        detail = get_video_by_code(TEST_DATA["code"])
        
        if not detail:
            log_test("get_video_by_code", False, "返回 None")
            return None
        
        if validate_video_detail(detail, "get_video_by_code"):
            log_test("get_video_by_code", True,
                    f"成功搜索: {detail.get('code')} - {detail.get('title')[:30]}...",
                    detail)
            return detail
    except Exception as e:
        log_test("get_video_by_code", False, f"异常: {str(e)}")
    
    return None


def test_3_search_actor():
    """测试3: 搜索演员"""
    print("\n" + "=" * 70)
    print("测试3: search_actor - 搜索演员")
    print("=" * 70)
    
    all_passed = True
    results = []
    
    for actor in EXTRA_ACTORS:
        try:
            actors = search_actor(actor["name"])
            
            if not actors:
                log_test(f"search_actor ({actor['name']})", False, "返回空列表")
                all_passed = False
                continue
            
            if not isinstance(actors, list):
                log_test(f"search_actor ({actor['name']})", False, "返回不是列表")
                all_passed = False
                continue
            
            first_actor = actors[0]
            required = ["actor_id", "actor_name", "actor_url"]
            missing = [f for f in required if f not in first_actor]
            
            if missing:
                log_test(f"search_actor ({actor['name']})", False, f"缺少字段: {missing}")
                all_passed = False
                continue
            
            log_test(f"search_actor ({actor['name']})", True,
                    f"找到 {len(actors)} 个演员: {first_actor.get('actor_name')} (ID: {first_actor.get('actor_id')})",
                    first_actor)
            results.append(first_actor)
        except Exception as e:
            log_test(f"search_actor ({actor['name']})", False, f"异常: {str(e)}")
            all_passed = False
    
    return results if results else None


def test_4_get_actor_works_by_page():
    """测试4: 获取演员作品（分页，基础信息）"""
    print("\n" + "=" * 70)
    print("测试4: get_actor_works_by_page - 演员作品（分页）")
    print("=" * 70)
    
    try:
        result = get_actor_works_by_page(TEST_DATA["actor_id"], page=1)
        
        if not result:
            log_test("get_actor_works_by_page", False, "返回 None")
            return None
        
        required = ["page", "has_next", "works"]
        missing = [f for f in required if f not in result]
        
        if missing:
            log_test("get_actor_works_by_page", False, f"缺少字段: {missing}")
            return None
        
        works = result.get("works", [])
        if not works:
            log_test("get_actor_works_by_page", False, "works 为空")
            return None
        
        first_work = works[0]
        work_fields = ["video_id", "code", "title"]
        missing_work = [f for f in work_fields if f not in first_work]
        
        if missing_work:
            log_test("get_actor_works_by_page", False, f"作品缺少字段: {missing_work}")
            return None
        
        log_test("get_actor_works_by_page", True,
                f"第 {result.get('page')} 页，共 {len(works)} 个作品，有下一页: {result.get('has_next')}",
                {"page": result.get("page"), "works_count": len(works), "has_next": result.get("has_next")})
        return result
    except Exception as e:
        log_test("get_actor_works_by_page", False, f"异常: {str(e)}")
    
    return None


def test_5_get_actor_works_full_by_page():
    """测试5: 获取演员作品全量信息（分页）"""
    print("\n" + "=" * 70)
    print("测试5: get_actor_works_full_by_page - 演员作品全量（分页）")
    print("=" * 70)
    
    try:
        result = get_actor_works_full_by_page(TEST_DATA["actor_id"], page=1, download_images=False)
        
        if not result:
            log_test("get_actor_works_full_by_page", False, "返回 None")
            return None
        
        required = ["page", "has_next", "works"]
        missing = [f for f in required if f not in result]
        
        if missing:
            log_test("get_actor_works_full_by_page", False, f"缺少字段: {missing}")
            return None
        
        works = result.get("works", [])
        if not works:
            log_test("get_actor_works_full_by_page", False, "works 为空")
            return None
        
        first_work = works[0]
        if not validate_video_detail(first_work, "get_actor_works_full_by_page"):
            return None
        
        log_test("get_actor_works_full_by_page", True,
                f"第 {result.get('page')} 页，共 {len(works)} 个作品（全量信息）",
                {"page": result.get("page"), "works_count": len(works), "first_code": first_work.get("code")})
        return result
    except Exception as e:
        log_test("get_actor_works_full_by_page", False, f"异常: {str(e)}")
    
    return None


def test_6_search_by_tags():
    """测试6: 多类标签组合搜索（基础信息）"""
    print("\n" + "=" * 70)
    print("测试6: search_by_tags - 标签搜索")
    print("=" * 70)
    
    try:
        result = search_by_tags(page=1, c3=TEST_DATA["tag_c3"])
        
        if not result:
            log_test("search_by_tags", False, "返回 None")
            return None
        
        required = ["page", "has_next", "works"]
        missing = [f for f in required if f not in result]
        
        if missing:
            log_test("search_by_tags", False, f"缺少字段: {missing}")
            return None
        
        log_test("search_by_tags", True,
                f"搜索 c3={TEST_DATA['tag_c3']} ({TEST_DATA['tag_name']})，"
                f"第 {result.get('page')} 页，共 {len(result.get('works', []))} 个作品",
                {"page": result.get("page"), "works_count": len(result.get("works", [])), "has_next": result.get("has_next")})
        return result
    except Exception as e:
        log_test("search_by_tags", False, f"异常: {str(e)}")
    
    return None


def test_7_search_by_tags_full():
    """测试7: 多类标签组合搜索（全量信息）"""
    print("\n" + "=" * 70)
    print("测试7: search_by_tags_full - 标签搜索全量")
    print("=" * 70)
    
    try:
        result = search_by_tags_full(page=1, c3=TEST_DATA["tag_c3"], download_images=False)
        
        if not result:
            log_test("search_by_tags_full", False, "返回 None")
            return None
        
        required = ["page", "has_next", "works"]
        missing = [f for f in required if f not in result]
        
        if missing:
            log_test("search_by_tags_full", False, f"缺少字段: {missing}")
            return None
        
        works = result.get("works", [])
        if works:
            first_work = works[0]
            if not validate_video_detail(first_work, "search_by_tags_full"):
                return None
        
        log_test("search_by_tags_full", True,
                f"搜索 c3={TEST_DATA['tag_c3']} ({TEST_DATA['tag_name']})，"
                f"第 {result.get('page')} 页，共 {len(works)} 个作品（全量）",
                {"page": result.get("page"), "works_count": len(works), "has_next": result.get("has_next")})
        return result
    except Exception as e:
        log_test("search_by_tags_full", False, f"异常: {str(e)}")
    
    return None


def test_8_tag_manager():
    """测试8: 标签管理"""
    print("\n" + "=" * 70)
    print("测试8: tag_manager - 标签管理")
    print("=" * 70)
    
    all_passed = True
    
    try:
        tag = get_tag_info("c3", TEST_DATA["tag_c3"])
        if tag and tag.get("name") == TEST_DATA["tag_name"]:
            log_test("get_tag_info", True, f"c3={TEST_DATA['tag_c3']} -> {tag.get('name')}")
        else:
            log_test("get_tag_info", False, f"预期: {TEST_DATA['tag_name']}, 实际: {tag}")
            all_passed = False
    except Exception as e:
        log_test("get_tag_info", False, f"异常: {str(e)}")
        all_passed = False
    
    try:
        results = search_tag_by_name(TEST_DATA["tag_name"])
        if results and len(results) > 0:
            log_test("search_tag_by_name", True, f"搜索 '{TEST_DATA['tag_name']}' 找到 {len(results)} 个结果")
        else:
            log_test("search_tag_by_name", False, "未找到结果")
            all_passed = False
    except Exception as e:
        log_test("search_tag_by_name", False, f"异常: {str(e)}")
        all_passed = False
    
    try:
        categories = get_category_list()
        if categories and len(categories) > 0:
            log_test("get_category_list", True, f"获取 {len(categories)} 个分类")
        else:
            log_test("get_category_list", False, "分类为空")
            all_passed = False
    except Exception as e:
        log_test("get_category_list", False, f"异常: {str(e)}")
        all_passed = False
    
    return all_passed


def test_9_image_download():
    """测试9: 图片下载功能"""
    print("\n" + "=" * 70)
    print("测试9: 图片下载功能")
    print("=" * 70)
    
    try:
        detail = get_video_detail(TEST_DATA["video_id"], download_images=True)
        
        if not detail:
            log_test("image_download", False, "无法获取视频详情")
            return False
        
        images = detail.get("thumbnail_images", [])
        if not images:
            log_test("image_download", False, "没有缩略图")
            return False
        
        log_test("image_download", True, f"获取 {len(images)} 张缩略图链接")
        
        from utils import ImageDownloader
        from curl_cffi import requests
        
        session = requests.Session()
        session.headers.update(config.HEADERS)
        downloader = ImageDownloader(session)
        
        code = detail.get("code", "unknown")
        save_dir = TEST_IMAGES_DIR / code
        save_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = downloader.download_thumbnails(code, images)
        
        if downloaded and len(downloaded) > 0:
            log_test("image_download_save", True, f"成功下载 {len(downloaded)} 张图片到 {save_dir}")
            return True
        else:
            log_test("image_download_save", False, "下载失败")
            return False
    except Exception as e:
        log_test("image_download", False, f"异常: {str(e)}")
        return False


def test_10_nagano_ichika_full():
    """测试10: 抓取永野一夏第一页所有作品详细信息并下载图片"""
    print("\n" + "=" * 70)
    print("测试10: 永野一夏第一页作品全量抓取+图片下载")
    print("=" * 70)
    
    actor_name = "永野一夏"
    actor_id = "NeOr"
    
    try:
        # 1. 获取第一页作品（基础信息）
        print(f"\n1. 获取 {actor_name} 的第一页作品...")
        result = get_actor_works_by_page(actor_id, page=1)
        
        if not result or not result.get("works"):
            log_test("nagano_ichika_full", False, "未找到作品")
            return False
        
        works = result["works"]
        total_works = len(works)
        print(f"   找到 {total_works} 个作品")
        
        # 2. 获取每个作品的详细信息
        print(f"\n2. 获取 {total_works} 个作品的详细信息...")
        full_works = []
        
        for i, work in enumerate(works, 1):
            video_id = work.get("video_id")
            code = work.get("code", "unknown")
            print(f"   [{i}/{total_works}] 获取 {code} (ID: {video_id})...", end=" ")
            
            try:
                detail = get_video_detail(video_id, download_images=True)
                if detail:
                    full_works.append(detail)
                    print("✅")
                else:
                    print("❌")
            except Exception as e:
                print(f"❌ ({e})")
            
            time.sleep(1)  # 避免请求过快
        
        print(f"\n   成功获取 {len(full_works)}/{total_works} 个作品的详细信息")
        
        # 3. 统计图片下载情况
        print(f"\n3. 统计图片下载情况...")
        total_images = 0
        downloaded_images = 0
        
        for work in full_works:
            images = work.get("thumbnail_images", [])
            total_images += len(images)
        
        print(f"   总图片数: {total_images}")
        
        # 4. 保存结果到 JSON
        output_data = {
            "actor_name": actor_name,
            "actor_id": actor_id,
            "page": 1,
            "total_works": total_works,
            "successful_works": len(full_works),
            "total_images": total_images,
            "works": full_works,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        output_file = TEST_JSON_DIR / f"{actor_name}_works_full.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n   结果已保存到: {output_file}")
        
        # 5. 输出作品列表
        print(f"\n   作品列表:")
        for i, work in enumerate(full_works[:5], 1):  # 只显示前5个
            code = work.get("code", "N/A")
            title = work.get("title", "")[:40]
            img_count = len(work.get("thumbnail_images", []))
            print(f"     {i}. [{code}] {title}... ({img_count} 张图片)")
        
        if len(full_works) > 5:
            print(f"     ... 还有 {len(full_works) - 5} 个作品")
        
        log_test("nagano_ichika_full", True, 
                f"成功抓取 {actor_name} 的 {len(full_works)} 个作品，"
                f"共 {total_images} 张图片，结果保存到 {output_file}",
                {"actor": actor_name, "works_count": len(full_works), "images_count": total_images})
        
        return True
        
    except Exception as e:
        log_test("nagano_ichika_full", False, f"异常: {str(e)}")
        return False


def save_test_results():
    """保存测试结果"""
    results_file = TEST_JSON_DIR / "test_results.json"
    
    summary = {
        "total": len(test_results),
        "passed": sum(1 for r in test_results if r["passed"]),
        "failed": sum(1 for r in test_results if not r["passed"]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tests": test_results
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 测试结果已保存到: {results_file}")
    return summary


def main():
    """运行所有测试"""
    print("=" * 70)
    print("🧪 JAVDB API 验证测试")
    print("=" * 70)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"输出目录: {TEST_OUTPUT_DIR}")
    print("=" * 70)
    
    # 收集所有启用的测试用例
    all_tests = []
    
    # 视频详情测试
    for test in VIDEO_DETAIL_TESTS:
        if test.get("enabled", False):
            all_tests.append(("视频详情", test, run_video_detail_test))
    
    # 番号搜索测试
    for test in CODE_SEARCH_TESTS:
        if test.get("enabled", False):
            all_tests.append(("番号搜索", test, run_code_search_test))
    
    # 演员搜索测试
    for test in ACTOR_SEARCH_TESTS:
        if test.get("enabled", False):
            all_tests.append(("演员搜索", test, run_actor_search_test))
    
    # 演员作品测试
    for test in ACTOR_WORKS_TESTS:
        if test.get("enabled", False):
            all_tests.append(("演员作品", test, run_actor_works_test))
    
    # 演员作品全量测试
    for test in ACTOR_WORKS_FULL_TESTS:
        if test.get("enabled", False):
            all_tests.append(("演员全量作品", test, run_actor_works_full_test))
    
    # 标签筛选测试
    for test in ACTOR_TAG_FILTER_TESTS:
        if test.get("enabled", False):
            all_tests.append(("标签筛选", test, run_tag_filter_test))
    
    # 标签搜索测试
    for test in TAG_SEARCH_TESTS:
        if test.get("enabled", False):
            all_tests.append(("标签搜索", test, run_tag_search_test))
    
    # 标签全量搜索测试
    for test in TAG_SEARCH_FULL_TESTS:
        if test.get("enabled", False):
            all_tests.append(("标签全量搜索", test, run_tag_search_full_test))
    
    # 演员作品全量+图片测试
    for test in ACTOR_WORKS_FULL_IMAGE_TESTS:
        if test.get("enabled", False):
            all_tests.append(("演员作品+图片", test, run_actor_works_full_image_test))
    
    # 高清预览图下载测试
    for test in HD_PREVIEW_DOWNLOAD_TESTS:
        if test.get("enabled", False):
            all_tests.append(("高清预览图", test, run_hd_preview_download_test))
    
    # 登录测试
    for test in LOGIN_TESTS:
        if test.get("enabled", False):
            all_tests.append(("登录测试", test, run_login_test))
    
    # 标签管理测试
    for test in TAG_MANAGER_TESTS:
        if test.get("enabled", False):
            all_tests.append(("标签管理", test, run_tag_manager_test))
    
    # 用户清单测试
    for test in USER_LIST_TESTS:
        if test.get("enabled", False):
            all_tests.append(("用户清单", test, run_user_list_test))
    
    print(f"启用的测试项: {len(all_tests)} 个")
    print("=" * 70)
    
    # 显示测试列表
    print("\n📋 测试用例列表:")
    print("=" * 70)
    print("0. 运行所有测试")
    
    for i, (category, test, _) in enumerate(all_tests, 1):
        print(f"{i}. {category}: {test['name']}")
    
    print("=" * 70)
    
    # 获取用户选择
    while True:
        try:
            choice = input("请输入测试编号 (0-全量测试): ")
            choice = int(choice)
            
            if choice == 0:
                # 运行所有测试
                print("\n🚀 开始全量测试...")
                for category, test, run_func in all_tests:
                    run_func(test)
                    time.sleep(1)
                break
            elif 1 <= choice <= len(all_tests):
                # 运行指定测试
                print("\n🚀 开始测试...")
                category, test, run_func = all_tests[choice - 1]
                run_func(test)
                break
            else:
                print(f"请输入 0 到 {len(all_tests)} 之间的数字")
        except ValueError:
            print("请输入有效的数字")
    
    summary = save_test_results()
    
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print(f"总计: {summary['total']} 个测试")
    print(f"通过: {summary['passed']} 个 ✅")
    print(f"失败: {summary['failed']} 个 ❌")
    print(f"成功率: {summary['passed']/summary['total']*100:.1f}%")
    print("=" * 70)
    
    return summary['failed'] == 0


# ============================================================================
# 配置化测试运行函数
# ============================================================================

def run_video_detail_test(config: dict):
    """运行视频详情测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        detail = get_video_detail(config["video_id"], download_images=config.get("download_images", False))
        
        if validate_video_detail(detail, config["name"]):
            data = {
                "video_id": detail.get("video_id"),
                "code": detail.get("code"),
                "title": detail.get("title", "")[:50],
                "date": detail.get("date"),
                "tags_count": len(detail.get("tags", [])),
                "magnets_count": len(detail.get("magnets", [])),
            }
            log_test(config["name"], True, f"视频ID: {config['video_id']}", data)
        else:
            log_test(config["name"], False, "验证失败")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_code_search_test(config: dict):
    """运行番号搜索测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        detail = get_video_by_code(config["code"])
        
        if detail and detail.get("code"):
            data = {
                "code": detail.get("code"),
                "title": detail.get("title", "")[:50],
                "found": True,
            }
            log_test(config["name"], True, f"找到番号: {config['code']}", data)
        else:
            log_test(config["name"], False, f"未找到番号: {config['code']}")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_actor_search_test(config: dict):
    """运行演员搜索测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        actors = search_actor(config["actor_name"])
        
        if actors:
            data = {
                "actor_name": config["actor_name"],
                "count": len(actors),
                "first_actor_id": actors[0].get("actor_id"),
            }
            log_test(config["name"], True, f"找到 {len(actors)} 个演员", data)
        else:
            log_test(config["name"], False, f"未找到演员: {config['actor_name']}")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_actor_works_test(config: dict):
    """运行演员作品测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        result = get_actor_works_by_page(config["actor_id"], page=config.get("page", 1))
        
        if result and result.get("works"):
            works = result["works"]
            data = {
                "actor_id": config["actor_id"],
                "actor_name": config.get("actor_name"),
                "page": config.get("page", 1),
                "total_works": len(works),
                "first_code": works[0].get("code") if works else None,
            }
            log_test(config["name"], True, f"找到 {len(works)} 个作品", data)
        else:
            log_test(config["name"], False, f"未找到作品")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_actor_works_full_test(config: dict):
    """运行演员作品全量测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        api = JavdbAPI()
        works = api.get_actor_works(
            config["actor_id"],
            max_pages=config.get("max_pages", 1),
            get_details=False,
            download_images=False
        )
        
        if works:
            data = {
                "actor_id": config["actor_id"],
                "actor_name": config.get("actor_name"),
                "total_works": len(works),
                "first_code": works[0].get("code") if works else None,
            }
            log_test(config["name"], True, f"找到 {len(works)} 个作品", data)
        else:
            log_test(config["name"], False, f"未找到作品")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_tag_filter_test(config: dict):
    """运行标签筛选测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        api = JavdbAPI()
        result = api.get_actor_works_with_tags(
            actor_id=config["actor_id"],
            tag_names=config.get("tag_names"),
            max_pages=config.get("max_pages", 1),
            get_details=config.get("get_details", False),
            download_images=config.get("download_images", False),
            save_temp=config.get("save_temp", True)
        )
        
        data = {
            "actor_id": config["actor_id"],
            "actor_name": config.get("actor_name"),
            "tags": config.get("tag_names"),
            "total_works": result["total_works"],
            "filtered_works": result["filtered_works"],
            "filter_rate": round(result["filtered_works"] / result["total_works"] * 100, 1) if result["total_works"] > 0 else 0,
        }
        log_test(config["name"], True, f"筛选结果: {result['filtered_works']}/{result['total_works']}", data)
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_tag_search_test(config: dict):
    """运行标签搜索测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        result = search_by_tags(
            page=1,
            max_pages=config.get("max_pages", 1),
            **config.get("tag_params", {})
        )
        
        if result and result.get("works"):
            works = result["works"]
            data = {
                "tag_params": config.get("tag_params"),
                "count": len(works),
                "first_code": works[0].get("code") if works else None,
            }
            log_test(config["name"], True, f"找到 {len(works)} 个作品", data)
        else:
            log_test(config["name"], False, f"未找到作品")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_tag_search_full_test(config: dict):
    """运行标签全量搜索测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        result = search_by_tags_full(
            page=1,
            max_pages=config.get("max_pages", 1),
            **config.get("tag_params", {})
        )
        
        if result and result.get("works"):
            works = result["works"]
            data = {
                "tag_params": config.get("tag_params"),
                "count": len(works),
                "first_code": works[0].get("code") if works else None,
            }
            log_test(config["name"], True, f"找到 {len(works)} 个作品", data)
        else:
            log_test(config["name"], False, f"未找到作品")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_actor_works_full_image_test(config: dict):
    """运行演员作品全量+图片测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        result = get_actor_works_full_by_page(
            config["actor_id"],
            max_pages=1,
            page=config.get("page", 1)
        )
        
        if result and result.get("works"):
            works = result["works"]
            total_images = 0
            
            for work in works:
                video_id = work.get("video_id")
                if video_id:
                    success, total = download_video_images(video_id, TEST_IMAGES_DIR)
                    total_images += total
            
            data = {
                "actor_id": config["actor_id"],
                "actor_name": config.get("actor_name"),
                "total_works": len(works),
                "total_images": total_images,
            }
            log_test(config["name"], True, f"下载 {total_images} 张图片", data)
        else:
            log_test(config["name"], False, f"未找到作品")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_hd_preview_download_test(config: dict):
    """运行高清预览图下载测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        detail = get_video_detail(config["video_id"], download_images=True)
        
        if detail:
            images = detail.get("thumbnail_images", [])
            data = {
                "video_id": config["video_id"],
                "code": config.get("code"),
                "title": detail.get("title", "")[:50],
                "images_count": len(images),
                "downloaded": True,
            }
            log_test(config["name"], True, f"下载 {len(images)} 张高清预览图", data)
        else:
            log_test(config["name"], False, f"未找到视频")
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_login_test(config: dict):
    """运行登录测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        from lib import JavdbLogin
        
        login = JavdbLogin()
        
        if config.get("auto_login", False):
            # 自动登录（打开浏览器）
            print("启动自动登录助手...")
            from lib import auto_login
            success = auto_login(timeout=300)
            
            if success:
                data = {
                    "method": "auto_login",
                    "success": True,
                }
                log_test(config["name"], True, "自动登录成功", data)
            else:
                log_test(config["name"], False, "自动登录失败或超时")
        else:
            # 检查登录状态
            if login.load_cookies():
                if login.check_login_status():
                    data = {
                        "method": "check_status",
                        "success": True,
                        "logged_in": True,
                    }
                    log_test(config["name"], True, "登录状态有效", data)
                else:
                    data = {
                        "method": "check_status",
                        "success": False,
                        "logged_in": False,
                    }
                    log_test(config["name"], False, "登录状态无效，需要重新登录", data)
            else:
                data = {
                    "method": "check_status",
                    "success": False,
                    "logged_in": False,
                    "error": "未找到 cookies 文件",
                }
                log_test(config["name"], False, "未找到 cookies 文件", data)
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_tag_manager_test(config: dict):
    """运行标签管理测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        # 测试1: 通过名称查询标签
        if "tag_name" in config:
            tag = get_tag_by_name(config["tag_name"])
            
            if tag:
                expected_id = config.get("expected_id")
                if expected_id and tag.get("id") != expected_id:
                    log_test(config["name"], False, 
                            f"标签ID不匹配: 预期 {expected_id}, 实际 {tag.get('id')}")
                    return
                
                data = {
                    "tag_name": config["tag_name"],
                    "tag_id": tag.get("id"),
                    "tag_category": tag.get("category"),
                    "tag_value": tag.get("value"),
                }
                log_test(config["name"], True, 
                        f"找到标签: {tag.get('name')} ({tag.get('id')})", data)
            else:
                log_test(config["name"], False, 
                        f"未找到标签: {config['tag_name']}")
        
        # 测试2: 通过ID查询标签
        elif "tag_id" in config:
            tag = get_tag_by_id(config["tag_id"])
            
            if tag:
                expected_name = config.get("expected_name")
                if expected_name and tag.get("name") != expected_name:
                    log_test(config["name"], False, 
                            f"标签名称不匹配: 预期 {expected_name}, 实际 {tag.get('name')}")
                    return
                
                data = {
                    "tag_id": config["tag_id"],
                    "tag_name": tag.get("name"),
                    "tag_category": tag.get("category"),
                    "tag_value": tag.get("value"),
                }
                log_test(config["name"], True, 
                        f"找到标签: {tag.get('name')} ({tag.get('id')})", data)
            else:
                log_test(config["name"], False, 
                        f"未找到标签ID: {config['tag_id']}")
        
        # 测试3: 关键词搜索
        elif "keyword" in config:
            tags = search_tags_by_keyword(config["keyword"])
            
            if tags:
                data = {
                    "keyword": config["keyword"],
                    "found_count": len(tags),
                    "tags": [{"name": t.get("name"), "id": t.get("id")} for t in tags[:5]],
                }
                log_test(config["name"], True, 
                        f"找到 {len(tags)} 个匹配标签", data)
            else:
                log_test(config["name"], False, 
                        f"未找到匹配关键词的标签: {config['keyword']}")
        else:
            log_test(config["name"], False, "未知的测试类型")
            
    except Exception as e:
        log_test(config["name"], False, f"异常: {str(e)}")


def run_user_list_test(config: dict):
    """运行用户清单测试"""
    print(f"\n{'=' * 70}")
    print(f"🧪 {config['name']}")
    print(f"{'=' * 70}")
    
    try:
        test_type = config.get("test_type")
        
        # 测试1: 获取想看清单
        if test_type == "want_watch":
            result = get_want_watch_videos(page=1)
            
            codes = [work['code'] for work in result['works'] if work['code']]
            data = {
                "page": result['page'],
                "has_next": result['has_next'],
                "total_works": len(result['works']),
                "codes": codes[:10],
                "all_codes_count": len(codes),
            }
            log_test(config["name"], True, 
                    f"获取到 {len(result['works'])} 个作品，{len(codes)} 个有番号", data)
        
        # 测试2: 获取看过清单（全部）
        elif test_type == "watched_all":
            max_pages = config.get("max_pages", 5)
            works = get_watched_videos_all(max_pages=max_pages)
            
            codes = [work['code'] for work in works if work['code']]
            video_ids = [work['video_id'] for work in works]
            
            data = {
                "max_pages": max_pages,
                "total_works": len(works),
                "codes_count": len(codes),
                "video_ids_count": len(video_ids),
                "sample_codes": codes[:20],
                "sample_video_ids": video_ids[:20],
            }
            log_test(config["name"], True, 
                    f"获取到 {len(works)} 个作品，{len(codes)} 个有番号", data)
        
        # 测试3: 获取用户清单列表（全部）
        elif test_type == "user_lists_all":
            max_pages = config.get("max_pages", 5)
            lists = get_user_lists_all(max_pages=max_pages)
            
            data = {
                "max_pages": max_pages,
                "total_lists": len(lists),
                "lists": [
                    {
                        "list_name": lst['list_name'],
                        "list_id": lst['list_id'],
                        "video_count": lst['video_count'],
                    }
                    for lst in lists
                ],
            }
            log_test(config["name"], True, 
                    f"获取到 {len(lists)} 个清单", data)
        
        # 测试4: 获取清单详细内容（单页）
        elif test_type == "list_detail":
            list_id = config.get("list_id", "0W97k")
            result = get_list_detail(list_id, page=1)
            
            codes = [work['code'] for work in result['works'] if work['code']]
            data = {
                "list_id": list_id,
                "list_name": result.get('list_name', ''),
                "page": result['page'],
                "has_next": result['has_next'],
                "total_works": len(result['works']),
                "codes": codes[:10],
            }
            log_test(config["name"], True, 
                    f"清单 '{result.get('list_name')}' 获取到 {len(result['works'])} 个作品", data)
        
        # 测试5: 获取清单全部作品ID
        elif test_type == "list_detail_all":
            list_id = config.get("list_id", "0W97k")
            max_pages = config.get("max_pages", 5)
            result = get_list_detail_all(list_id, max_pages=max_pages)
            
            codes = [work['code'] for work in result['works'] if work['code']]
            video_ids = [work['video_id'] for work in result['works']]
            
            data = {
                "list_id": list_id,
                "list_name": result.get('list_name', ''),
                "max_pages": max_pages,
                "total_works": len(result['works']),
                "codes_count": len(codes),
                "video_ids_count": len(video_ids),
                "sample_codes": codes[:20],
                "sample_video_ids": video_ids[:20],
            }
            log_test(config["name"], True, 
                    f"清单 '{result.get('list_name')}' 获取到 {len(result['works'])} 个作品，{len(codes)} 个有番号", data)
        
        else:
            log_test(config["name"], False, f"未知的测试类型: {test_type}")
            
    except Exception as e:
        import traceback
        log_test(config["name"], False, f"异常: {str(e)}\n{traceback.format_exc()}")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
