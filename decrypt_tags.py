"""
标签数据库解密脚本
将 tags_database.enc 解密为内存中的数据
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from crypto_utils import CryptoUtils, DEFAULT_KEY


def decrypt_tags_database():
    """
    解密标签数据库
    
    Returns:
        dict: 解密后的标签数据库
    """
    # 定义文件路径
    output_dir = Path(__file__).parent / "output"
    encrypted_file = output_dir / "tags_database.enc"
    
    # 检查加密文件是否存在
    if not encrypted_file.exists():
        print(f"❌ 加密文件不存在: {encrypted_file}")
        return None
    
    try:
        # 执行解密
        decrypted_content = CryptoUtils.decrypt_file(
            input_file=str(encrypted_file),
            key=DEFAULT_KEY
        )
        
        # 解析 JSON
        tags_db = json.loads(decrypted_content)
        
        print("✅ 解密成功！")
        print(f"   分类数: {len(tags_db.get('categories', {}))}")
        
        # 计算总标签数
        total_tags = 0
        for category in tags_db.get('categories', {}).values():
            total_tags += len(category.get('tags', []))
        
        print(f"   总标签数: {total_tags}")
        
        return tags_db
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ 解密失败: {str(e)}")
        return None


def main():
    """
    主函数
    """
    print("🔓 标签数据库解密脚本")
    print("=" * 50)
    
    tags_db = decrypt_tags_database()
    
    print("=" * 50)
    if tags_db:
        print("🎉 解密完成！")
        print("   数据已加载到内存")
    else:
        print("❌ 解密失败！")
    
    return 0 if tags_db else 1


if __name__ == "__main__":
    sys.exit(main())
