"""
测试标签管理功能（使用解析的数据库）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tag_manager import TagManager, get_tag_info, search_tag_by_name
from javdb_api import search_by_tags


def test_tag_database():
    """测试标签数据库功能"""
    print("=" * 70)
    print("测试标签管理功能")
    print("=" * 70)
    
    # 创建 TagManager 实例
    manager = TagManager()
    manager.load_tags()
    
    # 显示分类信息
    print(f"\n✅ 更新时间: {manager.tags_db.get('updated_at', '未知')}")
    print(f"✅ 分类数: {len(manager.tags_db.get('categories', {}))}")
    
    total_tags = 0
    for cat_key, cat_data in sorted(manager.tags_db.get("categories", {}).items()):
        tag_count = len(cat_data.get("tags", []))
        total_tags += tag_count
        print(f"\n【{cat_key}】{cat_data.get('name', '')} ({tag_count}个标签)")
        # 显示前3个标签
        for tag in cat_data.get("tags", [])[:3]:
            print(f"   - {tag['id']}: {tag['name']}")
    
    print(f"\n总计: {total_tags} 个标签")
    return manager.tags_db


def test_get_tag_info():
    """测试获取特定标签信息"""
    print("\n" + "=" * 70)
    print("测试2: 获取特定标签信息")
    print("=" * 70)
    
    # 查询标签
    tag = get_tag_info("c3", 78)  # 第三类第78个标签（水手服）
    if tag:
        print(f"\n✅ c3=78: {tag['name']}")
    else:
        print("\n⚠️ 未找到标签 c3=78")
    
    # 查询其他标签
    tag = get_tag_info("c1", 23)  # 第一类第23个标签
    if tag:
        print(f"✅ c1=23: {tag['name']}")
    
    tag = get_tag_info("c5", 18)  # 第五类第18个标签（中出）
    if tag:
        print(f"✅ c5=18: {tag['name']}")
    
    return tag


def test_search_tag_by_name():
    """测试根据名称搜索标签"""
    print("\n" + "=" * 70)
    print("测试3: 根据名称搜索标签")
    print("=" * 70)
    
    results = search_tag_by_name("水手服")
    print(f"\n✅ 搜索 '水手服' 找到 {len(results)} 个结果")
    for result in results:
        print(f"   - {result['category']} ({result['category_name']}): "
              f"{result['tag']['id']} = {result['tag']['name']}")
    
    # 搜索其他标签
    results = search_tag_by_name("中出")
    print(f"\n✅ 搜索 '中出' 找到 {len(results)} 个结果")
    for result in results[:3]:
        print(f"   - {result['category']} ({result['category_name']}): "
              f"{result['tag']['id']} = {result['tag']['name']}")
    
    results = search_tag_by_name("巨乳")
    print(f"\n✅ 搜索 '巨乳' 找到 {len(results)} 个结果")
    for result in results[:3]:
        print(f"   - {result['category']} ({result['category_name']}): "
              f"{result['tag']['id']} = {result['tag']['name']}")
    
    return results


def test_search_by_tags():
    """测试多类标签组合搜索"""
    print("\n" + "=" * 70)
    print("测试4: 多类标签组合搜索")
    print("=" * 70)
    
    # 示例：搜索 c3=78 (水手服)
    print("\n尝试搜索 c3=78 (水手服)...")
    
    try:
        result = search_by_tags(page=1, c3=78)
        
        print(f"✅ 页码: {result['page']}")
        print(f"✅ 标签参数: {result['tag_params']}")
        print(f"✅ 是否有下一页: {result['has_next']}")
        print(f"✅ 作品数: {len(result['works'])}")
        
        for work in result['works'][:3]:
            print(f"   - {work['code']}: {work['title'][:30]}...")
        
    except Exception as e:
        print(f"⚠️ 搜索失败: {e}")
    
    return True


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🧪 测试标签管理功能（使用解析的数据库）")
    print("=" * 70)
    
    try:
        # 测试1: 加载标签数据库
        tags_db = test_tag_database()
        
        # 测试2: 获取特定标签
        tag = test_get_tag_info()
        
        # 测试3: 搜索标签
        results = test_search_tag_by_name()
        
        # 测试4: 多类标签组合搜索
        test_search_by_tags()
        
        print("\n" + "=" * 70)
        print("✅ 标签管理测试完成!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
