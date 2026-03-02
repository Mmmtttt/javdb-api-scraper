"""
JAVDB API 测试运行器
支持配置化测试、结果保存和详细日志

使用方法:
    python test_runner.py              # 运行所有启用的测试
    python test_runner.py --list        # 列出所有测试项
    python test_runner.py --video       # 只运行视频相关测试
    python test_runner.py --actor       # 只运行演员相关测试
    python test_runner.py --tag         # 只运行标签相关测试

配置文件: test_config.py
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入配置
from test_config import (
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
    # 测试函数
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
    
    # ============================================================================
    # 运行测试
    # ============================================================================
    
    def run_all(self, test_filter: str = None):
        """
        运行所有测试
        
        Args:
            test_filter: 测试过滤器 (video, actor, tag, magnet, image)
        """
        print("=" * 70)
        print("🚀 JAVDB API 测试运行器")
        print("=" * 70)
        
        # 打印测试摘要
        summary = get_test_summary()
        total = sum(summary.values())
        print(f"\n📋 启用的测试项总数: {total}\n")
        
        # 初始化 API
        if not self.init_api():
            return
        
        # 运行测试
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
        
        # 保存结果
        self.save_results()
        
        # 打印摘要
        self.print_summary()
    
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
        if not RESULT_CONFIG["save_results"]:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存 JSON 格式
        if RESULT_CONFIG["save_json"]:
            json_file = self.output_dir / f"test_results_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "total_tests": len(self.results),
                    "passed_tests": sum(1 for r in self.results if r.success),
                    "failed_tests": sum(1 for r in self.results if not r.success),
                    "results": [r.to_dict() for r in self.results]
                }, f, indent=2, ensure_ascii=False)
            print(f"\n📁 JSON 结果已保存: {json_file}")
        
        # 保存文本格式
        if RESULT_CONFIG["save_text"]:
            text_file = self.output_dir / f"test_results_{timestamp}.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("JAVDB API 测试结果\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总测试数: {len(self.results)}\n")
                f.write(f"通过: {sum(1 for r in self.results if r.success)}\n")
                f.write(f"失败: {sum(1 for r in self.results if not r.success)}\n\n")
                
                for result in self.results:
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
            
            print(f"📁 文本结果已保存: {text_file}")
    
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
    parser.add_argument("--list", action="store_true", help="列出所有测试项")
    parser.add_argument("--video", action="store_true", help="只运行视频相关测试")
    parser.add_argument("--actor", action="store_true", help="只运行演员相关测试")
    parser.add_argument("--tag", action="store_true", help="只运行标签相关测试")
    parser.add_argument("--magnet", action="store_true", help="只运行磁力链接测试")
    parser.add_argument("--image", action="store_true", help="只运行图片下载测试")
    
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
    if args.video:
        test_filter = "video"
    elif args.actor:
        test_filter = "actor"
    elif args.tag:
        test_filter = "tag"
    elif args.magnet:
        test_filter = "magnet"
    elif args.image:
        test_filter = "image"
    
    runner.run_all(test_filter)


if __name__ == "__main__":
    main()
