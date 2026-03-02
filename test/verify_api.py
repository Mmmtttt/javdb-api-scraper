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

TEST_DATA = {
    "video_id": "YwG8Ve",
    "code": "MIDA-583",
    "actor_name": "井上もも",
    "actor_id": "0R1n3",
    "tag_c3": 78,
    "tag_name": "水手服",
}

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
    
    try:
        actors = search_actor(TEST_DATA["actor_name"])
        
        if not actors:
            log_test("search_actor", False, "返回空列表")
            return None
        
        if not isinstance(actors, list):
            log_test("search_actor", False, "返回不是列表")
            return None
        
        first_actor = actors[0]
        required = ["actor_id", "actor_name", "actor_url"]
        missing = [f for f in required if f not in first_actor]
        
        if missing:
            log_test("search_actor", False, f"缺少字段: {missing}")
            return None
        
        log_test("search_actor", True,
                f"找到 {len(actors)} 个演员: {first_actor.get('actor_name')} (ID: {first_actor.get('actor_id')})",
                first_actor)
        return first_actor
    except Exception as e:
        log_test("search_actor", False, f"异常: {str(e)}")
    
    return None


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
    
    test_1_get_video_detail()
    time.sleep(1)
    
    test_2_get_video_by_code()
    time.sleep(1)
    
    test_3_search_actor()
    time.sleep(1)
    
    test_4_get_actor_works_by_page()
    time.sleep(1)
    
    test_5_get_actor_works_full_by_page()
    time.sleep(1)
    
    test_6_search_by_tags()
    time.sleep(1)
    
    test_7_search_by_tags_full()
    time.sleep(1)
    
    # test_8_tag_manager()  # 标签管理功能已移至 lib
    time.sleep(1)
    
    test_9_image_download()
    
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


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
