"""
JAVDB API 测试运行器
支持配置化测试、结果保存和详细日志

================================================================================
================================ 7个核心功能测试 ================================
================================================================================

1. search_actor_works    - 搜索演员的作品ID列表
2. get_video_detail      - 获取作品详细信息
3. download_video_images - 下载作品图片
4. search_videos_by_tags - 标签搜索
5. get_user_lists        - 获取用户清单
6. get_list_works        - 获取清单作品
7. login                 - 登录

使用方法:
    python test_runner.py              # 运行所有启用的测试（首先运行7个核心功能）
    python test_runner.py --core        # 只运行7个核心功能测试
    python test_runner.py --list        # 列出所有测试项
    python test_runner.py --video       # 只运行视频相关测试
    python test_runner.py --actor       # 只运行演员相关测试
    python test_runner.py --tag         # 只运行标签相关测试
    python test_runner.py --javbus      # 只运行 JavBus 测试

配置文件: test_config.py
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入配置
from test_config import (
    # 7个核心功能测试配置
    CORE_API_SEARCH_ACTOR_WORKS_TESTS,
    CORE_API_VIDEO_DETAIL_TESTS,
    CORE_API_DOWNLOAD_IMAGES_TESTS,
    CORE_API_TAG_SEARCH_TESTS,
    CORE_API_USER_LISTS_TESTS,
    CORE_API_LIST_WORKS_TESTS,
    CORE_API_LOGIN_TESTS,
    # 其他测试配置
    LOGIN_CONFIG,
    VIDEO_DETAIL_TESTS,
    CODE_SEARCH_TESTS,
    VIDEO_SEARCH_TESTS,
    ACTOR_SEARCH_TESTS,
    ACTOR_WORKS_TESTS,
    TAG_FILTER_TESTS,
    TAG_SEARCH_TESTS,
    MAGNET_TESTS,
    IMAGE_DOWNLOAD_TESTS,
    GENERAL_IMAGE_DOWNLOAD_TESTS,
    JAVBUS_CONFIG,
    JAVBUS_SEARCH_TESTS,
    JAVBUS_DETAIL_TESTS,
    JAVBUS_MAGNET_TESTS,
    JAVBUS_IMAGE_TESTS,
    JAVBUS_ACTOR_TESTS,
    RESULT_CONFIG,
    TIMEOUT_CONFIG,
    RETRY_CONFIG,
    LOG_CONFIG,
    get_enabled_tests,
    get_test_summary,
)


# ============================================================================
# 测试结果类
# ============================================================================

class TestResult:
    """测试结果类"""
    
    def __init__(self, test_name: str, test_type: str):
        self.test_name = test_name
        self.test_type = test_type
        self.success = False
        self.error = None
        self.start_time = None
        self.end_time = None
        self.duration = 0
        self.data = {}
        self.message = ""
    
    def start(self):
        """开始测试"""
        self.start_time = time.time()
    
    def end(self, success: bool, message: str = "", data: Dict = None, error: str = None):
        """结束测试"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.success = success
        self.message = message
        self.error = error
        if data:
            self.data = data
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "test_name": self.test_name,
            "test_type": self.test_type,
            "success": self.success,
            "error": self.error,
            "duration": round(self.duration, 2),
            "message": self.message,
            "data": self.data,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
        }


class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.api = None
        self.output_dir = Path(RESULT_CONFIG["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def init_api(self):
        """初始化 API"""
        try:
            from javdb_api import JavdbAPI
            self.api = JavdbAPI()
            return True
        except Exception as e:
            print(f"❌ 初始化 API 失败: {e}")
            return False
    
    def run_test(self, test_func, test_config: Dict, test_type: str) -> TestResult:
        """
        运行单个测试
        
        Args:
            test_func: 测试函数
            test_config: 测试配置
            test_type: 测试类型
            
        Returns:
            测试结果
        """
        result = TestResult(test_config["name"], test_type)
        result.start()
        
        print(f"\n{'=' * 70}")
        print(f"🧪 {test_config['name']}")
        print(f"{'=' * 70}")
        
        try:
            data = test_func(self.api, test_config)
            result.end(True, "测试成功", data)
            print(f"✅ 测试成功: {test_config['name']}")
            if RESULT_CONFIG["verbose"] and data:
                print(f"📊 结果: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}...")
        except Exception as e:
            result.end(False, "", error=str(e))
            print(f"❌ 测试失败: {test_config['name']}")
            print(f"   错误: {e}")
        
        self.results.append(result)
        return result
    
    # ============================================================================
    # 7个核心功能测试函数
    # ============================================================================

    def test_core_search_actor_works(self, api, config: Dict) -> Dict:
        """【核心功能1】测试搜索演员作品"""
        from lib import search_actor_works

        works = search_actor_works(
            actor_id=config["actor_id"],
            start=config.get("start", 0),
            end=config.get("end", 20),
            platform=config.get("platform")
        )
        return {
            "actor_id": config["actor_id"],
            "actor_name": config.get("actor_name"),
            "platform": config.get("platform") or "javdb",
            "start": config.get("start", 0),
            "end": config.get("end", 20),
            "total_works": len(works),
            "first_code": works[0].get("code") if works else None,
            "first_title": works[0].get("title", "")[:50] if works else None,
        }

    def test_core_video_detail(self, api, config: Dict) -> Dict:
        """【核心功能2】测试获取作品详情"""
        from lib import get_video_detail

        detail = get_video_detail(
            video_id=config["video_id"],
            platform=config.get("platform")
        )
        return {
            "video_id": config["video_id"],
            "platform": config.get("platform") or "javdb",
            "code": detail.get("code") if detail else None,
            "title": detail.get("title", "")[:50] if detail else None,
            "tags_count": len(detail.get("tags", [])) if detail else 0,
            "actors_count": len(detail.get("actors", [])) if detail else 0,
            "magnets_count": len(detail.get("magnets", [])) if detail else 0,
            "has_cover": bool(detail.get("cover_url")) if detail else False,
            "thumbnails_count": len(detail.get("thumbnail_images", [])) if detail else 0,
        }

    def test_core_download_images(self, api, config: Dict) -> Dict:
        """【核心功能3】测试下载作品图片"""
        from lib import download_video_images

        result = download_video_images(
            video_id=config["video_id"],
            output_dir=config.get("output_dir", "output/images"),
            platform=config.get("platform")
        )
        return {
            "video_id": config["video_id"],
            "platform": config.get("platform") or "javdb",
            "downloaded": result.get("downloaded", 0),
            "total": result.get("total", 0),
            "success_rate": result.get("success_rate", 0),
            "download_dir": result.get("download_dir", ""),
        }

    def test_core_tag_search(self, api, config: Dict) -> Dict:
        """【核心功能4】测试标签搜索"""
        from lib import search_videos_by_tags

        works = search_videos_by_tags(
            tag_names=config["tag_names"],
            start=config.get("start", 0),
            end=config.get("end", 20),
            platform=config.get("platform")
        )
        return {
            "tag_names": config["tag_names"],
            "platform": config.get("platform") or "javdb",
            "start": config.get("start", 0),
            "end": config.get("end", 20),
            "total_works": len(works),
            "first_code": works[0].get("code") if works else None,
            "first_title": works[0].get("title", "")[:50] if works else None,
        }

    def test_core_user_lists(self, api, config: Dict) -> Dict:
        """【核心功能5】测试获取用户清单"""
        from lib import get_user_lists

        lists = get_user_lists()
        return {
            "total_lists": len(lists),
            "lists": [{"id": lst.get("list_id"), "name": lst.get("list_name")} for lst in lists[:5]],
        }

    def test_core_list_works(self, api, config: Dict) -> Dict:
        """【核心功能6】测试获取清单作品"""
        from lib import get_list_works

        works = get_list_works(
            list_id=config["list_id"],
            start=config.get("start", 0),
            end=config.get("end", 20)
        )
        return {
            "list_id": config["list_id"],
            "start": config.get("start", 0),
            "end": config.get("end", 20),
            "total_works": len(works),
            "first_code": works[0].get("code") if works else None,
            "first_title": works[0].get("title", "")[:50] if works else None,
        }

    def test_core_login(self, api, config: Dict) -> Dict:
        """【核心功能7】测试登录"""
        from lib import login

        success = login()
        return {
            "login_success": success,
        }

    # ============================================================================
    # 其他测试函数
    # ============================================================================

    def test_video_detail(self, api, config: Dict) -> Dict:
        """测试视频详情"""
        detail = api.get_video_detail(
            config["video_id"],
            download_images=config.get("download_images", False)
        )
        return {
            "video_id": detail.get("video_id"),
            "code": detail.get("code"),
            "title": detail.get("title", "")[:50],
            "date": detail.get("date"),
            "tags_count": len(detail.get("tags", [])),
            "magnets_count": len(detail.get("magnets", [])),
        }
    
    def test_code_search(self, api, config: Dict) -> Dict:
        """测试番号搜索"""
        detail = api.get_video_by_code(config["code"])
        return {
            "code": detail.get("code"),
            "title": detail.get("title", "")[:50],
            "found": bool(detail),
        }
    
    def test_video_search(self, api, config: Dict) -> Dict:
        """测试视频搜索"""
        videos = api.search_videos(
            config["keyword"],
            max_pages=config.get("max_pages", 1)
        )
        return {
            "keyword": config["keyword"],
            "count": len(videos),
            "first_code": videos[0].get("code") if videos else None,
        }
    
    def test_actor_search(self, api, config: Dict) -> Dict:
        """测试演员搜索"""
        actors = api.search_actor(config["actor_name"])
        return {
            "actor_name": config["actor_name"],
            "count": len(actors),
            "first_actor_id": actors[0].get("actor_id") if actors else None,
        }
    
    def test_actor_works(self, api, config: Dict) -> Dict:
        """测试演员作品"""
        result = api.get_actor_works(
            config["actor_id"],
            max_pages=config.get("max_pages", 1),
            get_details=config.get("get_details", False),
            download_images=config.get("download_images", False)
        )
        works = result.get("works", [])
        return {
            "actor_id": config["actor_id"],
            "actor_name": config.get("actor_name"),
            "total_works": len(works),
            "first_code": works[0].get("code") if works else None,
        }
    
    def test_tag_filter(self, api, config: Dict) -> Dict:
        """测试标签筛选"""
        result = api.get_actor_works_with_tags(
            actor_id=config["actor_id"],
            tag_names=config.get("tag_names"),
            max_pages=config.get("max_pages", 1),
            get_details=config.get("get_details", False),
            download_images=config.get("download_images", False),
            save_temp=config.get("save_temp", True)
        )
        return {
            "actor_id": config["actor_id"],
            "actor_name": config.get("actor_name"),
            "tags": config.get("tag_names"),
            "total_works": result["total_works"],
            "filtered_works": result["filtered_works"],
            "filter_rate": round(result["filtered_works"] / result["total_works"] * 100, 1) if result["total_works"] > 0 else 0,
        }
    
    def test_tag_search(self, api, config: Dict) -> Dict:
        """测试标签搜索"""
        result = api.get_tag_works(
            config["tag_id"],
            max_pages=config.get("max_pages", 1)
        )
        works = result.get("works", [])
        return {
            "tag_id": config["tag_id"],
            "count": len(works),
            "first_code": works[0].get("code") if works else None,
        }
    
    def test_magnet(self, api, config: Dict) -> Dict:
        """测试磁力链接"""
        detail = api.get_video_detail(config["video_id"])
        magnets = detail.get("magnets", [])
        return {
            "video_id": config["video_id"],
            "magnets_count": len(magnets),
            "has_magnet": len(magnets) > 0,
        }
    
    def test_image_download(self, api, config: Dict) -> Dict:
        """测试图片下载"""
        success_count, total_count = api.download_video_images(
            config["video_id"],
            download_dir=config.get("download_dir")
        )
        return {
            "video_id": config["video_id"],
            "total_images": total_count,
            "downloaded_images": success_count,
            "success_rate": round(success_count / total_count * 100, 1) if total_count > 0 else 0,
        }
    
    def test_general_image_download(self, api, config: Dict) -> Dict:
        """测试通用图片下载 API"""
        from javdb_api import download_video_images
        
        result = download_video_images(
            video_id=config["video_id"],
            image_urls=config["image_urls"],
            output_dir=config.get("download_dir", "test/images/general"),
            headers=config.get("headers")
        )
        return result
    
    # ============================================================================
    # JavBus 测试函数
    # ============================================================================
    
    def init_javbus_adapter(self):
        """初始化 JavBus 适配器"""
        try:
            from lib.javbus_adapter import JavbusAdapter
            proxy = JAVBUS_CONFIG.get("proxy")
            self.javbus_adapter = JavbusAdapter(proxy=proxy)
            return True
        except Exception as e:
            print(f"❌ 初始化 JavBus 适配器失败: {e}")
            return False
    
    def test_javbus_search(self, adapter, config: Dict) -> Dict:
        """测试 JavBus 搜索"""
        from lib import search_videos
        
        videos = search_videos(
            config["keyword"],
            max_pages=config.get("max_pages", 1),
            platform="javbus",
            movie_type=config.get("movie_type", "normal")
        )
        return {
            "keyword": config["keyword"],
            "movie_type": config.get("movie_type", "normal"),
            "count": len(videos),
            "first_code": videos[0].get("code") if videos else None,
            "first_title": videos[0].get("title", "")[:50] if videos else None,
        }
    
    def test_javbus_detail(self, adapter, config: Dict) -> Dict:
        """测试 JavBus 详情"""
        from lib import get_video_detail
        
        detail = get_video_detail(
            config["video_id"],
            platform="javbus",
            movie_type=config.get("movie_type", "normal")
        )
        return {
            "video_id": config["video_id"],
            "code": detail.get("code"),
            "title": detail.get("title", "")[:50],
            "date": detail.get("date"),
            "actors": detail.get("actors", []),
            "tags": detail.get("tags", []),
            "has_gid": bool(detail.get("gid")),
            "has_uc": bool(detail.get("uc")),
        }
    
    def test_javbus_magnet(self, adapter, config: Dict) -> Dict:
        """测试 JavBus 磁力链接"""
        from lib import get_video_detail, get_movie_magnets
        
        # 先获取详情获取 gid 和 uc
        detail = get_video_detail(
            config["video_id"],
            platform="javbus",
            movie_type=config.get("movie_type", "normal")
        )
        
        if not detail or not detail.get("gid") or not detail.get("uc"):
            return {
                "video_id": config["video_id"],
                "magnets_count": 0,
                "error": "无法获取 gid 或 uc 参数",
            }
        
        magnets = get_movie_magnets(
            config["video_id"],
            platform="javbus",
            gid=detail["gid"],
            uc=detail["uc"],
            sort_by="size",
            sort_order="desc"
        )
        
        return {
            "video_id": config["video_id"],
            "magnets_count": len(magnets),
            "first_magnet_size": magnets[0].get("size") if magnets else None,
            "first_magnet_hd": magnets[0].get("is_hd") if magnets else None,
        }
    
    def test_javbus_actor(self, adapter, config: Dict) -> Dict:
        """测试 JavBus 演员作品"""
        result = adapter.get_actor_works(
            config["actor_id"],
            max_pages=config.get("max_pages", 1)
        )
        works = result.get("works", [])
        return {
            "actor_id": config["actor_id"],
            "total_works": len(works),
            "first_code": works[0].get("code") if works else None,
        }
    
    def test_javbus_image(self, adapter, config: Dict) -> Dict:
        """测试 JavBus 图片下载"""
        import os
        from pathlib import Path
        
        # 获取详情
        detail = adapter.get_video_detail(
            config["video_id"],
            movie_type=config.get("movie_type", "normal")
        )
        
        if not detail:
            return {
                "video_id": config["video_id"],
                "error": "无法获取详情",
                "downloaded": 0,
                "total": 0,
            }
        
        # 创建下载目录
        download_dir = config.get("download_dir", "./images/javbus")
        video_dir = Path(download_dir) / config["video_id"]
        video_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = 0
        total = 0
        
        # 下载封面
        if config.get("download_cover", True) and detail.get("cover_url"):
            total += 1
            cover_url = detail["cover_url"]
            ext = cover_url.split(".")[-1].split("?")[0]
            if not ext or len(ext) > 5:
                ext = "jpg"
            
            cover_path = video_dir / f"cover.{ext}"
            try:
                # 使用带 Referer 的请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': f"{adapter.BASE_URL}/{config['video_id']}",
                }
                response = adapter.session.get(cover_url, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(cover_path, "wb") as f:
                        f.write(response.content)
                    downloaded += 1
                    print(f"  ✅ 封面下载成功: {cover_path}")
                else:
                    print(f"  ⚠️ 封面下载返回 {response.status_code}")
            except Exception as e:
                print(f"  ❌ 封面下载失败: {e}")
        
        # 下载样品图
        if config.get("download_samples", True) and detail.get("samples"):
            samples = detail["samples"]
            for i, sample in enumerate(samples[:10]):  # 最多下载10张
                total += 1
                img_url = sample.get("full_image") or sample.get("thumbnail")
                if not img_url:
                    continue
                
                ext = img_url.split(".")[-1].split("?")[0]
                if not ext or len(ext) > 5:
                    ext = "jpg"
                
                sample_path = video_dir / f"sample_{i+1:02d}.{ext}"
                try:
                    # 使用带 Referer 的请求头
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Referer': f"{adapter.BASE_URL}/{config['video_id']}",
                    }
                    response = adapter.session.get(img_url, headers=headers, timeout=30)
                    if response.status_code == 200:
                        with open(sample_path, "wb") as f:
                            f.write(response.content)
                        downloaded += 1
                        print(f"  ✅ 样品图 {i+1} 下载成功: {sample_path}")
                    else:
                        print(f"  ⚠️ 样品图 {i+1} 返回 {response.status_code}")
                except Exception as e:
                    print(f"  ❌ 样品图 {i+1} 下载失败: {e}")
        
        # 下载搜索列表缩略图（如果有）
        thumbnail_downloaded = 0
        if config.get("download_thumbnails", False):
            # 搜索该作品获取缩略图
            try:
                search_results = adapter.search_videos(
                    config["video_id"],
                    max_pages=1,
                    movie_type=config.get("movie_type", "normal")
                )
                for result in search_results:
                    if result.get("code") == config["video_id"] and result.get("cover_url"):
                        total += 1
                        thumb_url = result["cover_url"]
                        ext = thumb_url.split(".")[-1].split("?")[0]
                        if not ext or len(ext) > 5:
                            ext = "jpg"
                        
                        thumb_path = video_dir / f"thumbnail.{ext}"
                        try:
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                'Referer': f"{adapter.BASE_URL}/search/{config['video_id']}",
                            }
                            response = adapter.session.get(thumb_url, headers=headers, timeout=30)
                            if response.status_code == 200:
                                with open(thumb_path, "wb") as f:
                                    f.write(response.content)
                                downloaded += 1
                                thumbnail_downloaded += 1
                                print(f"  ✅ 缩略图下载成功: {thumb_path}")
                            else:
                                print(f"  ⚠️ 缩略图下载返回 {response.status_code}")
                        except Exception as e:
                            print(f"  ❌ 缩略图下载失败: {e}")
                        break
            except Exception as e:
                print(f"  ⚠️ 搜索缩略图失败: {e}")
        
        return {
            "video_id": config["video_id"],
            "download_dir": str(video_dir),
            "downloaded": downloaded,
            "total": total,
            "success_rate": round(downloaded / total * 100, 1) if total > 0 else 0,
            "cover_url": detail.get("cover_url"),
            "cover_hd": detail.get("cover_hd"),
            "sample_count": detail.get("sample_count", 0),
            "thumbnail_downloaded": thumbnail_downloaded,
            "tags": detail.get("tags", []),
            "tags_count": detail.get("tags_count", 0),
            "actors": detail.get("actors", []),
            "actors_detail": detail.get("actors_detail", []),
        }
    
    # ============================================================================
    # 运行测试
    # ============================================================================
    
    def run_all(self, test_filter: str = None):
        """
        运行所有测试
        
        Args:
            test_filter: 测试过滤器 (core, video, actor, tag, magnet, image, javbus)
        """
        print("=" * 70)
        print("🚀 JAVDB API 测试运行器")
        print("=" * 70)

        # 打印测试摘要
        summary = get_test_summary()
        total = summary.get("total", 0)
        print(f"\n📋 启用的测试项总数: {total}\n")

        # 初始化 API
        if not self.init_api():
            return

        # 首先运行7个核心功能测试
        if not test_filter or test_filter == "core":
            self._run_core_api_tests()

        # 运行其他测试
        if not test_filter or test_filter == "video":
            self._run_tests(VIDEO_DETAIL_TESTS, self.test_video_detail, "video_detail")
            self._run_tests(CODE_SEARCH_TESTS, self.test_code_search, "code_search")
            self._run_tests(VIDEO_SEARCH_TESTS, self.test_video_search, "video_search")

        if not test_filter or test_filter == "actor":
            self._run_tests(ACTOR_SEARCH_TESTS, self.test_actor_search, "actor_search")
            self._run_tests(ACTOR_WORKS_TESTS, self.test_actor_works, "actor_works")

        if not test_filter or test_filter == "tag":
            self._run_tests(TAG_FILTER_TESTS, self.test_tag_filter, "tag_filter")
            self._run_tests(TAG_SEARCH_TESTS, self.test_tag_search, "tag_search")

        if not test_filter or test_filter == "magnet":
            self._run_tests(MAGNET_TESTS, self.test_magnet, "magnet")

        if not test_filter or test_filter == "image":
            self._run_tests(IMAGE_DOWNLOAD_TESTS, self.test_image_download, "image_download")
            self._run_tests(GENERAL_IMAGE_DOWNLOAD_TESTS, self.test_general_image_download, "general_image_download")

        # 运行 JavBus 测试
        if not test_filter or test_filter == "javbus":
            self._run_javbus_tests()

        # 保存结果
        self.save_results()

        # 打印摘要
        self.print_summary()

    def _run_core_api_tests(self):
        """运行7个核心功能测试"""
        print("\n" + "=" * 70)
        print("🎯 7个核心功能测试")
        print("=" * 70)

        # 核心功能1: 搜索演员作品
        self._run_tests(CORE_API_SEARCH_ACTOR_WORKS_TESTS, self.test_core_search_actor_works, "core_search_actor_works")

        # 核心功能2: 获取作品详情
        self._run_tests(CORE_API_VIDEO_DETAIL_TESTS, self.test_core_video_detail, "core_video_detail")

        # 核心功能3: 下载作品图片
        self._run_tests(CORE_API_DOWNLOAD_IMAGES_TESTS, self.test_core_download_images, "core_download_images")

        # 核心功能4: 标签搜索
        self._run_tests(CORE_API_TAG_SEARCH_TESTS, self.test_core_tag_search, "core_tag_search")

        # 核心功能5: 获取用户清单
        self._run_tests(CORE_API_USER_LISTS_TESTS, self.test_core_user_lists, "core_user_lists")

        # 核心功能6: 获取清单作品
        self._run_tests(CORE_API_LIST_WORKS_TESTS, self.test_core_list_works, "core_list_works")

        # 核心功能7: 登录
        self._run_tests(CORE_API_LOGIN_TESTS, self.test_core_login, "core_login")
    
    def _run_javbus_tests(self):
        """运行 JavBus 测试"""
        if not JAVBUS_CONFIG.get("enabled", False):
            print("\n⚠️ JavBus 测试已禁用，跳过")
            return
        
        print("\n" + "=" * 70)
        print("🌐 JavBus 测试")
        print("=" * 70)
        
        # 初始化 JavBus 适配器
        if not self.init_javbus_adapter():
            return
        
        # 运行搜索测试
        enabled_tests = get_enabled_tests(JAVBUS_SEARCH_TESTS)
        for test_config in enabled_tests:
            result = TestResult(test_config["name"], "javbus_search")
            result.start()
            
            print(f"\n{'=' * 70}")
            print(f"🧪 {test_config['name']}")
            print(f"{'=' * 70}")
            
            try:
                data = self.test_javbus_search(self.javbus_adapter, test_config)
                result.end(True, "测试成功", data)
                print(f"✅ 测试成功: {test_config['name']}")
                if RESULT_CONFIG["verbose"] and data:
                    print(f"📊 结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
            except Exception as e:
                result.end(False, "", error=str(e))
                print(f"❌ 测试失败: {test_config['name']}")
                print(f"   错误: {e}")
            
            self.results.append(result)
        
        # 运行详情测试
        enabled_tests = get_enabled_tests(JAVBUS_DETAIL_TESTS)
        for test_config in enabled_tests:
            result = TestResult(test_config["name"], "javbus_detail")
            result.start()
            
            print(f"\n{'=' * 70}")
            print(f"🧪 {test_config['name']}")
            print(f"{'=' * 70}")
            
            try:
                data = self.test_javbus_detail(self.javbus_adapter, test_config)
                result.end(True, "测试成功", data)
                print(f"✅ 测试成功: {test_config['name']}")
                if RESULT_CONFIG["verbose"] and data:
                    print(f"📊 结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
            except Exception as e:
                result.end(False, "", error=str(e))
                print(f"❌ 测试失败: {test_config['name']}")
                print(f"   错误: {e}")
            
            self.results.append(result)
        
        # 运行磁力链接测试
        enabled_tests = get_enabled_tests(JAVBUS_MAGNET_TESTS)
        for test_config in enabled_tests:
            result = TestResult(test_config["name"], "javbus_magnet")
            result.start()
            
            print(f"\n{'=' * 70}")
            print(f"🧪 {test_config['name']}")
            print(f"{'=' * 70}")
            
            try:
                data = self.test_javbus_magnet(self.javbus_adapter, test_config)
                result.end(True, "测试成功", data)
                print(f"✅ 测试成功: {test_config['name']}")
                if RESULT_CONFIG["verbose"] and data:
                    print(f"📊 结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
            except Exception as e:
                result.end(False, "", error=str(e))
                print(f"❌ 测试失败: {test_config['name']}")
                print(f"   错误: {e}")
            
            self.results.append(result)
        
        # 运行图片下载测试
        enabled_tests = get_enabled_tests(JAVBUS_IMAGE_TESTS)
        for test_config in enabled_tests:
            result = TestResult(test_config["name"], "javbus_image")
            result.start()
            
            print(f"\n{'=' * 70}")
            print(f"🧪 {test_config['name']}")
            print(f"{'=' * 70}")
            
            try:
                data = self.test_javbus_image(self.javbus_adapter, test_config)
                result.end(True, "测试成功", data)
                print(f"✅ 测试成功: {test_config['name']}")
                print(f"📊 下载: {data['downloaded']}/{data['total']} ({data['success_rate']}%)")
                print(f"📊 样品图数: {data['sample_count']}, 缩略图: {data.get('thumbnail_downloaded', 0)}")
                print(f"📊 保存目录: {data['download_dir']}")
                if RESULT_CONFIG["verbose"]:
                    print(f"📊 标签数: {data['tags_count']}, 标签: {', '.join(data['tags'][:10])}")
                    print(f"📊 演员: {', '.join(data['actors'])}")
            except Exception as e:
                result.end(False, "", error=str(e))
                print(f"❌ 测试失败: {test_config['name']}")
                print(f"   错误: {e}")
            
            self.results.append(result)
        
        # 运行演员作品测试
        enabled_tests = get_enabled_tests(JAVBUS_ACTOR_TESTS)
        for test_config in enabled_tests:
            result = TestResult(test_config["name"], "javbus_actor")
            result.start()
            
            print(f"\n{'=' * 70}")
            print(f"🧪 {test_config['name']}")
            print(f"{'=' * 70}")
            
            try:
                data = self.test_javbus_actor(self.javbus_adapter, test_config)
                result.end(True, "测试成功", data)
                print(f"✅ 测试成功: {test_config['name']}")
                if RESULT_CONFIG["verbose"] and data:
                    print(f"📊 结果: {json.dumps(data, ensure_ascii=False, indent=2)}")
            except Exception as e:
                result.end(False, "", error=str(e))
                print(f"❌ 测试失败: {test_config['name']}")
                print(f"   错误: {e}")
            
            self.results.append(result)
    
    def _run_tests(self, test_list: List[Dict], test_func, test_type: str):
        """运行测试列表"""
        enabled_tests = get_enabled_tests(test_list)
        for test_config in enabled_tests:
            self.run_test(test_func, test_config, test_type)
    
    # ============================================================================
    # 结果保存
    # ============================================================================
    
    def save_results(self):
        """保存测试结果"""
        if not RESULT_CONFIG["save_to_file"]:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_output_dirs = RESULT_CONFIG.get("test_output_dirs", {})

        # 按测试类型分组结果
        results_by_type = {}
        for result in self.results:
            test_type = result.test_type
            if test_type not in results_by_type:
                results_by_type[test_type] = []
            results_by_type[test_type].append(result)

        # 为每个测试类型保存独立的结果文件
        for test_type, type_results in results_by_type.items():
            # 获取该测试类型的输出目录
            output_dir_name = test_output_dirs.get(test_type, "test_results")
            output_dir = Path(output_dir_name)
            output_dir.mkdir(parents=True, exist_ok=True)

            # 保存 JSON 格式
            if RESULT_CONFIG["output_format"] in ["json", "both"]:
                json_file = output_dir / f"{test_type}_{timestamp}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "test_type": test_type,
                        "total_tests": len(type_results),
                        "passed_tests": sum(1 for r in type_results if r.success),
                        "failed_tests": sum(1 for r in type_results if not r.success),
                        "results": [r.to_dict() for r in type_results]
                    }, f, indent=2, ensure_ascii=False)
                print(f"\n📁 [{test_type}] JSON 结果已保存: {json_file}")

            # 保存文本格式
            if RESULT_CONFIG["output_format"] in ["txt", "both"]:
                text_file = output_dir / f"{test_type}_{timestamp}.txt"
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write("=" * 70 + "\n")
                    f.write(f"JAVDB API 测试结果 - {test_type}\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"总测试数: {len(type_results)}\n")
                    f.write(f"通过: {sum(1 for r in type_results if r.success)}\n")
                    f.write(f"失败: {sum(1 for r in type_results if not r.success)}\n\n")

                    for result in type_results:
                        f.write("-" * 70 + "\n")
                        f.write(f"测试: {result.test_name}\n")
                        f.write(f"类型: {result.test_type}\n")
                        f.write(f"状态: {'✅ 通过' if result.success else '❌ 失败'}\n")
                        f.write(f"耗时: {result.duration:.2f}秒\n")
                        if result.error:
                            f.write(f"错误: {result.error}\n")
                        if result.data:
                            f.write(f"数据: {json.dumps(result.data, ensure_ascii=False)}\n")
                        f.write("\n")

                print(f"📁 [{test_type}] 文本结果已保存: {text_file}")

        # 同时保存一个汇总结果到主目录
        summary_file = self.output_dir / f"test_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(self.results),
                "passed_tests": sum(1 for r in self.results if r.success),
                "failed_tests": sum(1 for r in self.results if not r.success),
                "results_by_type": {k: len(v) for k, v in results_by_type.items()},
                "all_results": [r.to_dict() for r in self.results]
            }, f, indent=2, ensure_ascii=False)
        print(f"\n📊 测试汇总已保存: {summary_file}")
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 70)
        print("📊 测试摘要")
        print("=" * 70)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success)
        total_duration = sum(r.duration for r in self.results)
        
        print(f"\n总测试数: {total}")
        print(f"通过: {passed} ({passed/total*100:.1f}%)" if total > 0 else "通过: 0")
        print(f"失败: {failed} ({failed/total*100:.1f}%)" if total > 0 else "失败: 0")
        print(f"总耗时: {total_duration:.2f}秒")
        
        if failed > 0:
            print(f"\n❌ 失败的测试:")
            for result in self.results:
                if not result.success:
                    print(f"   - {result.test_name}: {result.error}")
        
        print("\n" + "=" * 70)


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="JAVDB API 测试运行器")
    parser.add_argument("--core", action="store_true", help="只运行7个核心功能测试")
    parser.add_argument("--list", action="store_true", help="列出所有测试项")
    parser.add_argument("--video", action="store_true", help="只运行视频相关测试")
    parser.add_argument("--actor", action="store_true", help="只运行演员相关测试")
    parser.add_argument("--tag", action="store_true", help="只运行标签相关测试")
    parser.add_argument("--magnet", action="store_true", help="只运行磁力链接测试")
    parser.add_argument("--image", action="store_true", help="只运行图片下载测试")
    parser.add_argument("--javbus", action="store_true", help="只运行 JavBus 测试")

    args = parser.parse_args()

    # 列出测试项
    if args.list:
        print("=" * 70)
        print("📋 所有测试项")
        print("=" * 70)

        summary = get_test_summary()
        for test_type, count in summary.items():
            print(f"\n{test_type}: {count}")

        print("\n" + "=" * 70)
        print("💡 提示: 修改 test_config.py 中的 enabled 字段来启用/禁用测试")
        print("=" * 70)
        return

    # 运行测试
    runner = TestRunner()

    test_filter = None
    if args.core:
        test_filter = "core"
    elif args.video:
        test_filter = "video"
    elif args.actor:
        test_filter = "actor"
    elif args.tag:
        test_filter = "tag"
    elif args.magnet:
        test_filter = "magnet"
    elif args.image:
        test_filter = "image"
    elif args.javbus:
        test_filter = "javbus"

    runner.run_all(test_filter)


if __name__ == "__main__":
    main()
