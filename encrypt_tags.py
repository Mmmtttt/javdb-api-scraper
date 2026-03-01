"""
标签数据库加密脚本
将 tags_database.json 加密为 tags_database.enc
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from crypto_utils import CryptoUtils, DEFAULT_KEY


def encrypt_tags_database():
    """
    加密标签数据库
    """
    # 定义文件路径
    output_dir = Path(__file__).parent / "output"
    input_file = output_dir / "tags_database.json"
    output_file = output_dir / "tags_database.enc"
    
    # 检查输入文件是否存在
    if not input_file.exists():
        print(f"❌ 输入文件不存在: {input_file}")
        return False
    
    try:
        # 执行加密
        CryptoUtils.encrypt_file(
            input_file=str(input_file),
            output_file=str(output_file),
            key=DEFAULT_KEY
        )
        
        # 验证加密成功
        if output_file.exists():
            print(f"✅ 加密成功: {output_file}")
            print(f"   大小: {output_file.stat().st_size} 字节")
            
            # 可选：删除原文件
            if input_file.exists():
                input_file.unlink()
                print(f"✅ 已删除原文件: {input_file}")
            
            return True
        else:
            print("❌ 加密失败，输出文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ 加密失败: {str(e)}")
        return False


def main():
    """
    主函数
    """
    print("🔒 标签数据库加密脚本")
    print("=" * 50)
    
    success = encrypt_tags_database()
    
    print("=" * 50)
    if success:
        print("🎉 加密完成！")
        print("   加密文件: output/tags_database.enc")
        print("   密钥: 使用默认密钥")
    else:
        print("❌ 加密失败！")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
