"""
测试重构后的 API 接口
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from third_party.external_api import (
    search_videos,
    get_video_detail,
    get_video_by_code,
    search_actor,
    get_actor_works,
    get_tag_works,
    search_by_tags,
    convert_to_standard_format,
    get_stats,
    get_supported_platforms,
)

from third_party.adapter_factory import AdapterFactory
from core.platform import Platform


def test_supported_platforms():
    """测试获取支持的平台列表"""
    print("=" * 70)
    print("测试1: 获取支持的平台列表")
    print("=" * 70)
    
    platforms = get_supported_platforms()
    print(f"\n✅ 支持的平台: {platforms}")
    
    return True


def test_search_videos():
    """测试搜索视频"""
    print("\n" + "=" * 70)
    print("测试2: 搜索视频")
    print("=" * 70)
    
    videos = search_videos("SSIS", max_pages=1)
    
    print(f"\n✅ 搜索到 {len(videos)} 个视频:")
    for video in videos[:5]:
        print(f"   - {video.get('code')}: {video.get('title', '')[:40]}...")
    
    return len(videos) > 0


def test_get_video_detail():
    """测试获取视频详情"""
    print("\n" + "=" * 70)
    print("测试3: 获取视频详情")
    print("=" * 70)
    
    detail = get_video_detail("YwG8Ve")
    
    print(f"\n✅ 视频详情:")
    print(f"   video_id: {detail.get('video_id')}")
    print(f"   code: {detail.get('code')}")
    print(f"   title: {detail.get('title', '')[:50]}...")
    print(f"   date: {detail.get('date')}")
    print(f"   tags: {detail.get('tags', [])}")
    print(f"   actors: {detail.get('actors', [])}")
    print(f"   series: {detail.get('series')}")
    print(f"   magnets: {len(detail.get('magnets', []))}个")
    print(f"   thumbnail_images: {len(detail.get('thumbnail_images', []))}张")
    
    return detail.get('video_id') == "YwG8Ve"


def test_get_video_by_code():
    """测试根据番号获取视频"""
    print("\n" + "=" * 70)
    print("测试4: 根据番号获取视频")
    print("=" * 70)
    
    detail = get_video_by_code("MIDA-583")
    
    if detail:
        print(f"\n✅ 找到番号 MIDA-583:")
        print(f"   code: {detail.get('code')}")
        print(f"   title: {detail.get('title', '')[:50]}...")
        print(f"   tags: {detail.get('tags', [])}")
        return True
    else:
        print(f"\n❌ 未找到")
        return False


def test_search_actor():
    """测试搜索演员"""
    print("\n" + "=" * 70)
    print("测试5: 搜索演员")
    print("=" * 70)
    
    actors = search_actor("井上もも")
    
    print(f"\n✅ 找到 {len(actors)} 个演员:")
    for actor in actors:
        print(f"   - {actor.get('actor_name')} (ID: {actor.get('actor_id')})")
    
    return len(actors) > 0


def test_get_actor_works():
    """测试获取演员作品"""
    print("\n" + "=" * 70)
    print("测试6: 获取演员作品")
    print("=" * 70)
    
    result = get_actor_works("0R1n3", max_pages=1)
    
    print(f"\n✅ 演员作品:")
    print(f"   page: {result.get('page')}")
    print(f"   has_next: {result.get('has_next')}")
    print(f"   works: {len(result.get('works', []))}个")
    
    for work in result.get('works', [])[:5]:
        print(f"   - {work.get('code')}: {work.get('title', '')[:40]}...")
    
    return len(result.get('works', [])) > 0


def test_convert_to_standard_format():
    """测试数据转换为标准格式"""
    print("\n" + "=" * 70)
    print("测试7: 数据转换为标准格式")
    print("=" * 70)
    
    # 先搜索一些视频
    videos = search_videos("MIDA", max_pages=1)
    
    # 转换为标准格式
    data = convert_to_standard_format(videos)
    
    print(f"\n✅ 转换结果:")
    print(f"   视频数: {len(data.get('videos', []))}")
    print(f"   标签数: {len(data.get('tags', []))}")
    
    if data.get('videos'):
        video = data['videos'][0]
        print(f"\n第一个视频:")
        print(f"   id: {video.get('id')}")
        print(f"   code: {video.get('code')}")
        print(f"   title: {video.get('title', '')[:40]}...")
        print(f"   tag_ids: {video.get('tag_ids', [])}")
    
    return len(data.get('videos', [])) > 0


def test_adapter_factory():
    """测试适配器工厂"""
    print("\n" + "=" * 70)
    print("测试8: 适配器工厂")
    print("=" * 70)
    
    # 获取适配器
    adapter = AdapterFactory.get_adapter(Platform.JAVDB)
    
    print(f"\n✅ 获取到适配器:")
    print(f"   平台: {adapter.get_platform()}")
    
    # 使用适配器搜索
    videos = adapter.search_videos("SSIS", max_pages=1)
    print(f"   搜索结果: {len(videos)}个视频")
    
    return True


def test_get_stats():
    """测试获取统计信息"""
    print("\n" + "=" * 70)
    print("测试9: 获取统计信息")
    print("=" * 70)
    
    stats = get_stats()
    
    print(f"\n✅ 请求统计:")
    print(f"   {stats}")
    
    return True


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🧪 重构后 API 功能测试")
    print("=" * 70)
    
    tests = [
        ("获取支持的平台列表", test_supported_platforms),
        ("搜索视频", test_search_videos),
        ("获取视频详情", test_get_video_detail),
        ("根据番号获取视频", test_get_video_by_code),
        ("搜索演员", test_search_actor),
        ("获取演员作品", test_get_actor_works),
        ("数据转换为标准格式", test_convert_to_standard_format),
        ("适配器工厂", test_adapter_factory),
        ("获取统计信息", test_get_stats),
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
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 70)


if __name__ == '__main__':
    main()
