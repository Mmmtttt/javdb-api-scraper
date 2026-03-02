"""
测试 JAVDB API 功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from javdb_api import JavdbAPI


def test_video_detail():
    """测试视频详情获取"""
    print("=" * 70)
    print("测试1: 获取视频详情")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        detail = api.get_video_detail("YwG8Ve", download_images=False)
        
        print(f"\n✅ 成功获取视频详情:")
        print(f"   video_id: {detail.get('video_id')}")
        print(f"   code: {detail.get('code')}")
        print(f"   title: {detail.get('title', '')[:50]}...")
        print(f"   date: {detail.get('date')}")
        print(f"   tags: {detail.get('tags', [])}")
        print(f"   actors: {detail.get('actors', [])}")
        print(f"   series: {detail.get('series')}")
        print(f"   magnets: {len(detail.get('magnets', []))}个")
        print(f"   thumbnail_images: {len(detail.get('thumbnail_images', []))}张")
        print(f"   url: {detail.get('url')}")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_by_code():
    """测试根据番号搜索"""
    print("\n" + "=" * 70)
    print("测试2: 根据番号搜索")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        detail = api.get_video_by_code("MIDA-583", download_images=False)
        
        if detail:
            print(f"\n✅ 成功找到番号 MIDA-583:")
            print(f"   code: {detail.get('code')}")
            print(f"   title: {detail.get('title', '')[:50]}...")
            print(f"   tags: {detail.get('tags', [])}")
            print(f"   actors: {detail.get('actors', [])}")
            return True
        else:
            print(f"\n❌ 未找到番号 MIDA-583")
            return False
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_actor():
    """测试搜索演员"""
    print("\n" + "=" * 70)
    print("测试3: 搜索演员")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        actors = api.search_actor("井上もも")
        
        print(f"\n✅ 找到 {len(actors)} 个演员:")
        for actor in actors:
            print(f"   - {actor.get('actor_name')} (ID: {actor.get('actor_id')})")
            print(f"     URL: {actor.get('actor_url')}")
        
        return len(actors) > 0
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_actor_works():
    """测试获取演员作品"""
    print("\n" + "=" * 70)
    print("测试4: 获取演员作品")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        actors = api.search_actor("井上もも")
        if not actors:
            print(f"\n❌ 未找到演员")
            return False
        
        actor_id = actors[0]['actor_id']
        
        result = api.get_actor_works_by_page(actor_id, page=1)
        
        print(f"\n✅ 成功获取演员作品:")
        print(f"   actor_id: {actor_id}")
        print(f"   page: {result.get('page')}")
        print(f"   has_next: {result.get('has_next')}")
        print(f"   works: {len(result.get('works', []))}个")
        
        for work in result.get('works', [])[:5]:
            print(f"   - {work.get('code')}: {work.get('title', '')[:30]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_by_tags():
    """测试标签搜索"""
    print("\n" + "=" * 70)
    print("测试5: 标签搜索")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        result = api.search_by_tags(page=1, c1=23)
        
        print(f"\n✅ 成功搜索标签:")
        print(f"   tag_params: {result.get('tag_params')}")
        print(f"   page: {result.get('page')}")
        print(f"   has_next: {result.get('has_next')}")
        print(f"   works: {len(result.get('works', []))}个")
        
        for work in result.get('works', [])[:5]:
            print(f"   - {work.get('code')}: {work.get('title', '')[:30]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_tag_works():
    """测试获取标签作品"""
    print("\n" + "=" * 70)
    print("测试6: 获取标签作品")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        result = api.get_tag_works_by_page("173", page=1)
        
        print(f"\n✅ 成功获取标签作品:")
        print(f"   tag_id: 173")
        print(f"   page: {result.get('page')}")
        print(f"   has_next: {result.get('has_next')}")
        print(f"   works: {len(result.get('works', []))}个")
        
        for work in result.get('works', [])[:5]:
            print(f"   - {work.get('code')}: {work.get('title', '')[:30]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_videos():
    """测试视频搜索"""
    print("\n" + "=" * 70)
    print("测试7: 视频搜索")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        videos = api.search_videos("SSIS", page=1)
        
        print(f"\n✅ 成功搜索视频:")
        print(f"   keyword: SSIS")
        print(f"   results: {len(videos)}个")
        
        for video in videos[:5]:
            print(f"   - {video.get('code')}: {video.get('title', '')[:30]}...")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🧪 JAVDB API 功能测试")
    print("=" * 70)
    
    tests = [
        ("获取视频详情", test_video_detail),
        ("根据番号搜索", test_search_by_code),
        ("搜索演员", test_search_actor),
        ("获取演员作品", test_get_actor_works),
        ("标签搜索", test_search_by_tags),
        ("获取标签作品", test_get_tag_works),
        ("视频搜索", test_search_videos),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ {name} 失败: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 70)
    
    # 显示请求统计
    api = JavdbAPI()
    print(f"\n请求统计:")
    print(f"   总请求数: {api.request_count}")
    print(f"   成功请求数: {api.success_count}")
    print(f"   成功率: {(api.success_count / api.request_count * 100):.1f}%" if api.request_count > 0 else "0%")


if __name__ == '__main__':
    main()
