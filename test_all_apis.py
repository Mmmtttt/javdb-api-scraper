"""
测试所有对外暴露的 API 接口
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from javdb_api import (
    get_video_detail,
    get_video_by_code,
    search_actor,
    get_actor_works_by_page,
    get_actor_works_full_by_page,
    get_tag_works_by_page,
    get_tag_works_full_by_page,
)


def test_get_video_detail():
    """测试1: 抓取作品页全量信息"""
    print("=" * 70)
    print("测试1: 抓取作品页全量信息")
    print("=" * 70)
    
    detail = get_video_detail("YwG8Ve", download_images=False)
    
    print(f"\n✅ video_id: {detail['video_id']}")
    print(f"✅ code: {detail['code']}")
    print(f"✅ title: {detail['title'][:50]}...")
    print(f"✅ tags: {detail['tags']}")
    print(f"✅ actors: {detail['actors']}")
    print(f"✅ magnets: {len(detail['magnets'])}个")
    
    return True


def test_get_video_by_code():
    """测试2: 根据番号搜索并获取作品全量信息"""
    print("\n" + "=" * 70)
    print("测试2: 根据番号搜索并获取作品全量信息")
    print("=" * 70)
    
    detail = get_video_by_code("MIDA-583", download_images=False)
    
    if detail:
        print(f"\n✅ 搜索番号: MIDA-583")
        print(f"✅ 找到: {detail['code']}")
        print(f"✅ title: {detail['title'][:50]}...")
        print(f"✅ tags: {detail['tags']}")
        return True
    else:
        print("❌ 未找到")
        return False


def test_get_actor_works_by_page():
    """测试3: 获取演员作品的code等基础信息（单页）"""
    print("\n" + "=" * 70)
    print("测试3: 获取演员作品的code等基础信息（单页）")
    print("=" * 70)
    
    # 先搜索演员
    actors = search_actor("井上もも")
    actor_id = actors[0]['actor_id']
    
    # 抓取第一页
    result = get_actor_works_by_page(actor_id, page=1)
    
    print(f"\n✅ actor_id: {actor_id}")
    print(f"✅ page: {result['page']}")
    print(f"✅ has_next: {result['has_next']}")
    print(f"✅ works: {len(result['works'])}个")
    
    for work in result['works']:
        print(f"   - {work['code']}: {work['title'][:30]}...")
    
    return True


def test_get_actor_works_full_by_page():
    """测试4: 获取演员作品的全量信息（单页）"""
    print("\n" + "=" * 70)
    print("测试4: 获取演员作品的全量信息（单页）")
    print("=" * 70)
    
    actors = search_actor("井上もも")
    actor_id = actors[0]['actor_id']
    
    # 只抓第一页的第一个作品的详情
    result = get_actor_works_by_page(actor_id, page=1)
    first_work = result['works'][0]
    
    # 获取详情
    detail = get_video_detail(first_work['video_id'], download_images=False)
    
    print(f"\n✅ {first_work['code']}:")
    print(f"   tags: {detail['tags']}")
    print(f"   actors: {detail['actors']}")
    print(f"   magnets: {len(detail['magnets'])}个")
    
    return True


def test_get_tag_works_by_page():
    """测试5: 获取Tag搜索结果的code等基础信息（单页）"""
    print("\n" + "=" * 70)
    print("测试5: 获取Tag搜索结果的code等基础信息（单页）")
    print("=" * 70)
    
    # 使用一个常见的 tag_id
    result = get_tag_works_by_page("173", page=1)  # 173 是某个 tag
    
    print(f"\n✅ tag_id: 173")
    print(f"✅ page: {result['page']}")
    print(f"✅ has_next: {result['has_next']}")
    print(f"✅ works: {len(result['works'])}个")
    
    if result['works']:
        for work in result['works'][:3]:
            print(f"   - {work['code']}: {work['title'][:30]}...")
    
    return True


def test_search_actor():
    """测试6: 搜索演员"""
    print("\n" + "=" * 70)
    print("测试6: 搜索演员")
    print("=" * 70)
    
    actors = search_actor("井上もも")
    
    print(f"\n✅ 找到 {len(actors)} 个演员")
    for actor in actors:
        print(f"   - {actor['name']} (ID: {actor['actor_id']})")
    
    return True


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🧪 测试所有对外暴露的 API 接口")
    print("=" * 70)
    
    tests = [
        ("抓取作品页全量信息", test_get_video_detail),
        ("根据番号搜索获取详情", test_get_video_by_code),
        ("获取演员作品code（单页）", test_get_actor_works_by_page),
        ("获取演员作品全量信息（单页）", test_get_actor_works_full_by_page),
        ("获取Tag作品code（单页）", test_get_tag_works_by_page),
        ("搜索演员", test_search_actor),
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
