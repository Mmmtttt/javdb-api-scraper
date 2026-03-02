"""
测试新功能：演员作品标签筛选和自动化登录
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from javdb_api import JavdbAPI
from lib import auto_login


def test_auto_login():
    """测试自动化登录"""
    print("=" * 70)
    print("测试1: 自动化登录")
    print("=" * 70)
    
    print("\n🔐 启动自动化登录助手...")
    print("💡 这将打开一个浏览器窗口，请按照页面提示操作")
    print("💡 登录后，复制 cookies 并粘贴到页面中提交\n")
    
    success = auto_login(timeout=300)  # 等待 5 分钟
    
    if success:
        print("\n✅ 自动化登录成功！")
        print("💡 现在可以使用需要登录的功能了")
    else:
        print("\n❌ 自动化登录失败或超时")
        print("💡 请手动将 cookies 保存到 cookies.json 文件")
    
    return success


def test_actor_works_with_tags():
    """测试演员作品标签筛选"""
    print("\n" + "=" * 70)
    print("测试2: 演员作品标签筛选")
    print("=" * 70)
    
    api = JavdbAPI()
    
    # 测试数据
    test_cases = [
        {
            "name": "永野一夏",
            "actor_id": "NeOr",
            "tag_names": ["水手服"],
            "description": "筛选永野一夏的作品，只保留带有'水手服'标签的"
        },
        {
            "name": "永野一夏",
            "actor_id": "NeOr",
            "tag_names": ["美少女", "單體作品"],
            "description": "筛选永野一夏的作品，同时包含'美少女'和'單體作品'标签"
        },
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"测试用例 {i}: {test_case['description']}")
        print(f"{'=' * 70}")
        
        result = api.get_actor_works_with_tags(
            actor_id=test_case["actor_id"],
            tag_names=test_case["tag_names"],
            max_pages=1,  # 只测试第一页
            get_details=False,  # 不获取详情，只获取基础信息
            save_temp=True
        )
        
        print(f"\n📊 结果统计:")
        print(f"   演员: {test_case['name']}")
        print(f"   总作品数: {result['total_works']}")
        print(f"   筛选标签: {result['tags']}")
        print(f"   筛选后作品数: {result['filtered_works']}")
        print(f"   筛选率: {result['filtered_works']/result['total_works']*100:.1f}%")
        
        if result['temp_file']:
            print(f"   临时文件: {result['temp_file']}")
        
        if result['works']:
            print(f"\n   筛选后的作品（前5个）:")
            for j, work in enumerate(result['works'][:5], 1):
                code = work.get('code', 'N/A')
                title = work.get('title', '')[:40]
                tags = work.get('tags', [])[:3]
                print(f"     {j}. [{code}] {title}...")
                print(f"        标签: {tags}")
            
            if len(result['works']) > 5:
                print(f"     ... 还有 {len(result['works']) - 5} 个作品")
    
    print(f"\n{'=' * 70}")
    print("💡 提示:")
    print("   - 临时文件保存了所有作品数据，可以重复使用")
    print("   - 下次筛选相同演员时，会自动从临时文件加载")
    print("   - 如需重新获取，请删除临时文件或使用不同的 temp_file 参数")
    print(f"{'=' * 70}")


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🧪 新功能测试")
    print("=" * 70)
    
    # 询问用户要测试哪个功能
    print("\n请选择要测试的功能:")
    print("1. 自动化登录")
    print("2. 演员作品标签筛选")
    print("3. 两个都测试")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-3): ").strip()
    
    if choice == "1":
        test_auto_login()
    elif choice == "2":
        test_actor_works_with_tags()
    elif choice == "3":
        # 先测试自动化登录
        login_success = test_auto_login()
        
        if login_success:
            print("\n" + "=" * 70)
            print("等待 3 秒后继续测试标签筛选功能...")
            print("=" * 70)
            import time
            time.sleep(3)
        
        # 再测试标签筛选
        test_actor_works_with_tags()
    elif choice == "0":
        print("退出")
    else:
        print("无效选项")


if __name__ == "__main__":
    main()
