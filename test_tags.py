"""
测试标签功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from javdb_api import JavdbAPI
from tag_manager import fetch_tags, get_tag_info, search_tag_by_name, get_category_list


def test_fetch_tags():
    """测试获取标签数据库"""
    print("=" * 70)
    print("测试1: 获取标签数据库")
    print("=" * 70)
    
    try:
        tags_db = fetch_tags(force_update=False, auto_login=False)
        
        print(f"\n✅ 成功获取标签数据库:")
        print(f"   更新时间: {tags_db.get('updated_at')}")
        print(f"   分类数: {len(tags_db.get('categories', {}))}")
        
        for cat_key, cat_data in sorted(tags_db.get('categories', {}).items()):
            print(f"   【{cat_key}】{cat_data.get('name')}: {len(cat_data.get('tags', []))}个标签")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_category_list():
    """测试获取分类列表"""
    print("\n" + "=" * 70)
    print("测试2: 获取分类列表")
    print("=" * 70)
    
    try:
        categories = get_category_list()
        
        print(f"\n✅ 成功获取分类列表:")
        for cat in categories:
            print(f"   - {cat['key']}: {cat['name']} ({cat['tag_count']}个标签)")
        
        return True
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_tag_by_name():
    """测试根据名称搜索标签"""
    print("\n" + "=" * 70)
    print("测试3: 根据名称搜索标签")
    print("=" * 70)
    
    try:
        results = search_tag_by_name("水手服")
        
        print(f"\n✅ 搜索 '水手服' 找到 {len(results)} 个结果:")
        for result in results:
            print(f"   - [{result['category']}] {result['category_name']}: {result['tag']['name']} (ID: {result['tag']['id']})")
        
        return len(results) > 0
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_tag_info():
    """测试获取标签信息"""
    print("\n" + "=" * 70)
    print("测试4: 获取标签信息")
    print("=" * 70)
    
    try:
        tag_info = get_tag_info("c3", 78)
        
        if tag_info:
            print(f"\n✅ 成功获取标签信息:")
            print(f"   id: {tag_info.get('id')}")
            print(f"   name: {tag_info.get('name')}")
            print(f"   value: {tag_info.get('value')}")
            return True
        else:
            print(f"\n❌ 未找到标签")
            return False
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_by_tags_with_real_ids():
    """测试使用真实标签ID搜索"""
    print("\n" + "=" * 70)
    print("测试5: 使用真实标签ID搜索")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        # 先搜索一个标签获取真实ID
        results = search_tag_by_name("可播放")
        
        if results:
            tag_id = results[0]['tag']['id']
            category = results[0]['category']
            
            print(f"\n使用标签: {results[0]['tag']['name']} (ID: {tag_id}, 分类: {category})")
            
            # 构建搜索参数
            tag_params = {category: tag_id}
            
            result = api.search_by_tags(page=1, **tag_params)
            
            print(f"\n✅ 成功搜索:")
            print(f"   tag_params: {result.get('tag_params')}")
            print(f"   page: {result.get('page')}")
            print(f"   has_next: {result.get('has_next')}")
            print(f"   works: {len(result.get('works', []))}个")
            
            for work in result.get('works', [])[:5]:
                print(f"   - {work.get('code')}: {work.get('title', '')[:30]}...")
            
            return len(result.get('works', [])) > 0
        else:
            print(f"\n❌ 未找到标签")
            return False
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_tag_works_with_real_id():
    """测试使用真实标签ID获取作品"""
    print("\n" + "=" * 70)
    print("测试6: 使用真实标签ID获取作品")
    print("=" * 70)
    
    api = JavdbAPI()
    
    try:
        # 先搜索一个标签获取真实ID
        results = search_tag_by_name("美少女")
        
        if results:
            tag_id = results[0]['tag']['id']
            
            print(f"\n使用标签: {results[0]['tag']['name']} (ID: {tag_id})")
            
            result = api.get_tag_works_by_page(str(tag_id), page=1)
            
            print(f"\n✅ 成功获取标签作品:")
            print(f"   tag_id: {tag_id}")
            print(f"   page: {result.get('page')}")
            print(f"   has_next: {result.get('has_next')}")
            print(f"   works: {len(result.get('works', []))}个")
            
            for work in result.get('works', [])[:5]:
                print(f"   - {work.get('code')}: {work.get('title', '')[:30]}...")
            
            return len(result.get('works', [])) > 0
        else:
            print(f"\n❌ 未找到标签")
            return False
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🧪 标签功能测试")
    print("=" * 70)
    
    tests = [
        ("获取标签数据库", test_fetch_tags),
        ("获取分类列表", test_get_category_list),
        ("根据名称搜索标签", test_search_tag_by_name),
        ("获取标签信息", test_get_tag_info),
        ("使用真实标签ID搜索", test_search_by_tags_with_real_ids),
        ("使用真实标签ID获取作品", test_get_tag_works_with_real_id),
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
