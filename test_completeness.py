"""
验证数据抓取的完整性
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from javdb_api import JavdbAPI


def test_video_detail_completeness():
    """测试视频详情数据的完整性"""
    print("=" * 70)
    print("测试1: 视频详情数据完整性")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        detail = api.get_video_detail("YwG8Ve", download_images=False)
        
        print(f"\n✅ 视频详情字段检查:")
        print(f"   video_id: {'✓' if detail.get('video_id') else '✗'}")
        print(f"   code: {'✓' if detail.get('code') else '✗'}")
        print(f"   title: {'✓' if detail.get('title') else '✗'}")
        print(f"   date: {'✓' if detail.get('date') else '✗'}")
        print(f"   tags: {'✓' if detail.get('tags') else '✗'} ({len(detail.get('tags', []))}个)")
        print(f"   actors: {'✓' if detail.get('actors') else '✗'} ({len(detail.get('actors', []))}个)")
        print(f"   series: {'✓' if detail.get('series') else '✗'}")
        print(f"   magnets: {'✓' if detail.get('magnets') else '✗'} ({len(detail.get('magnets', []))}个)")
        print(f"   thumbnail_images: {'✓' if detail.get('thumbnail_images') else '✗'} ({len(detail.get('thumbnail_images', []))}张)")
        print(f"   preview_video: {'✓' if detail.get('preview_video') else '✗'}")
        print(f"   url: {'✓' if detail.get('url') else '✗'}")
        
        # 详细显示磁力链接信息
        print(f"\n磁力链接详情:")
        for i, magnet in enumerate(detail.get('magnets', []), 1):
            print(f"   {i}. {magnet.get('size_text')} ({magnet.get('size_mb', 0):.2f}MB)")
            print(f"      {magnet.get('magnet', '')[:60]}...")
        
        # 详细显示标签
        print(f"\n标签列表:")
        for tag in detail.get('tags', []):
            print(f"   - {tag}")
        
        # 详细显示演员
        print(f"\n演员列表:")
        for actor in detail.get('actors', []):
            print(f"   - {actor}")
        
        # 详细显示缩略图
        print(f"\n缩略图列表 (前5张):")
        for img in detail.get('thumbnail_images', [])[:5]:
            print(f"   - {img}")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_actor_works_completeness():
    """测试演员作品数据的完整性"""
    print("\n" + "=" * 70)
    print("测试2: 演员作品数据完整性")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        actors = api.search_actor("井上もも")
        if not actors:
            print(f"\n❌ 未找到演员")
            return False
        
        actor_id = actors[0]['actor_id']
        
        result = api.get_actor_works_by_page(actor_id, page=1)
        
        print(f"\n✅ 演员作品字段检查:")
        print(f"   page: {'✓' if result.get('page') else '✗'}")
        print(f"   has_next: {'✓' if result.get('has_next') is not None else '✗'}")
        print(f"   works: {'✓' if result.get('works') else '✗'} ({len(result.get('works', []))}个)")
        
        # 检查每个作品字段的完整性
        if result.get('works'):
            print(f"\n第一个作品字段检查:")
            work = result['works'][0]
            print(f"   video_id: {'✓' if work.get('video_id') else '✗'}")
            print(f"   code: {'✓' if work.get('code') else '✗'}")
            print(f"   title: {'✓' if work.get('title') else '✗'}")
            print(f"   date: {'✓' if work.get('date') else '✗'}")
            print(f"   rating: {'✓' if work.get('rating') else '✗'}")
            print(f"   url: {'✓' if work.get('url') else '✗'}")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_video_detail():
    """测试获取完整视频详情"""
    print("\n" + "=" * 70)
    print("测试3: 获取完整视频详情")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        actors = api.search_actor("井上もも")
        if not actors:
            print(f"\n❌ 未找到演员")
            return False
        
        actor_id = actors[0]['actor_id']
        
        # 获取演员作品
        result = api.get_actor_works_by_page(actor_id, page=1)
        
        if not result.get('works'):
            print(f"\n❌ 未找到作品")
            return False
        
        # 获取第一个作品的完整详情
        first_work = result['works'][0]
        detail = api.get_video_detail(first_work['video_id'], download_images=False)
        
        print(f"\n✅ 完整视频详情:")
        print(f"   code: {detail.get('code')}")
        print(f"   title: {detail.get('title')}")
        print(f"   date: {detail.get('date')}")
        print(f"   tags: {detail.get('tags')}")
        print(f"   actors: {detail.get('actors')}")
        print(f"   series: {detail.get('series')}")
        print(f"   magnets: {len(detail.get('magnets', []))}个")
        print(f"   thumbnail_images: {len(detail.get('thumbnail_images', []))}张")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_results():
    """测试搜索结果的完整性"""
    print("\n" + "=" * 70)
    print("测试4: 搜索结果完整性")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        videos = api.search_videos("SSIS", page=1)
        
        print(f"\n✅ 搜索结果字段检查:")
        print(f"   结果数: {len(videos)}")
        
        if videos:
            print(f"\n第一个结果字段检查:")
            video = videos[0]
            print(f"   video_id: {'✓' if video.get('video_id') else '✗'}")
            print(f"   code: {'✓' if video.get('code') else '✗'}")
            print(f"   title: {'✓' if video.get('title') else '✗'}")
            print(f"   date: {'✓' if video.get('date') else '✗'}")
            print(f"   rating: {'✓' if video.get('rating') else '✗'}")
            print(f"   url: {'✓' if video.get('url') else '✗'}")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_videos():
    """测试多个视频的数据抓取"""
    print("\n" + "=" * 70)
    print("测试5: 多个视频数据抓取")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        # 测试几个不同的视频ID
        video_ids = ["YwG8Ve", "Xk7p2q", "Wm5n1r"]
        
        print(f"\n测试 {len(video_ids)} 个视频:")
        
        for video_id in video_ids:
            try:
                detail = api.get_video_detail(video_id, download_images=False)
                print(f"\n✅ {video_id}:")
                print(f"   code: {detail.get('code')}")
                print(f"   title: {detail.get('title', '')[:30]}...")
                print(f"   tags: {len(detail.get('tags', []))}个")
                print(f"   actors: {len(detail.get('actors', []))}个")
                print(f"   magnets: {len(detail.get('magnets', []))}个")
            except Exception as e:
                print(f"\n❌ {video_id}: {e}")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🧪 数据抓取完整性验证")
    print("=" * 70)
    
    tests = [
        ("视频详情数据完整性", test_video_detail_completeness),
        ("演员作品数据完整性", test_actor_works_completeness),
        ("获取完整视频详情", test_full_video_detail),
        ("搜索结果完整性", test_search_results),
        ("多个视频数据抓取", test_multiple_videos),
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


if __name__ == '__main__':
    main()
