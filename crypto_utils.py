"""
加密/解密工具模块
提供简单的 XOR 加密功能，用于保护敏感数据
"""

import json
import base64
from pathlib import Path


class CryptoUtils:
    """加密工具类"""
    
    @staticmethod
    def xor_encrypt(data: str, key: str) -> str:
        """
        使用 XOR 算法加密数据
        
        Args:
            data: 要加密的字符串
            key: 加密密钥
            
        Returns:
            加密后的 base64 字符串
        """
        # 确保密钥长度足够
        while len(key) < len(data):
            key += key
        
        # 执行 XOR 操作
        encrypted = []
        for i, char in enumerate(data):
            encrypted_char = chr(ord(char) ^ ord(key[i]))
            encrypted.append(encrypted_char)
        
        # 转换为 base64
        encrypted_str = ''.join(encrypted)
        return base64.b64encode(encrypted_str.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def xor_decrypt(encrypted_data: str, key: str) -> str:
        """
        使用 XOR 算法解密数据
        
        Args:
            encrypted_data: 加密的 base64 字符串
            key: 解密密钥
            
        Returns:
            解密后的字符串
        """
        # 解码 base64
        encrypted_str = base64.b64decode(encrypted_data).decode('utf-8')
        
        # 确保密钥长度足够
        while len(key) < len(encrypted_str):
            key += key
        
        # 执行 XOR 操作
        decrypted = []
        for i, char in enumerate(encrypted_str):
            decrypted_char = chr(ord(char) ^ ord(key[i]))
            decrypted.append(decrypted_char)
        
        return ''.join(decrypted)
    
    @staticmethod
    def encrypt_file(input_file: str, output_file: str, key: str):
        """
        加密文件
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            key: 加密密钥
        """
        # 读取文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 加密
        encrypted = CryptoUtils.xor_encrypt(content, key)
        
        # 保存加密结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        
        print(f"✅ 已加密: {input_file} -> {output_file}")
    
    @staticmethod
    def decrypt_file(input_file: str, key: str) -> str:
        """
        解密文件
        
        Args:
            input_file: 加密文件路径
            key: 解密密钥
            
        Returns:
            解密后的内容
        """
        # 读取加密文件
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()
        
        # 解密
        decrypted = CryptoUtils.xor_decrypt(encrypted_content, key)
        
        return decrypted
    
    @staticmethod
    def encrypt_json(data: dict, key: str) -> str:
        """
        加密 JSON 数据
        
        Args:
            data: JSON 数据
            key: 加密密钥
            
        Returns:
            加密后的 base64 字符串
        """
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        return CryptoUtils.xor_encrypt(json_str, key)
    
    @staticmethod
    def decrypt_json(encrypted_data: str, key: str) -> dict:
        """
        解密 JSON 数据
        
        Args:
            encrypted_data: 加密的 base64 字符串
            key: 解密密钥
            
        Returns:
            解密后的 JSON 数据
        """
        decrypted_str = CryptoUtils.xor_decrypt(encrypted_data, key)
        return json.loads(decrypted_str)


# 默认密钥（实际使用时可以从环境变量或配置文件读取）
DEFAULT_KEY = "javdb_api_key_2026"


if __name__ == "__main__":
    # 测试加密解密
    test_data = "Hello, World!"
    encrypted = CryptoUtils.xor_encrypt(test_data, DEFAULT_KEY)
    decrypted = CryptoUtils.xor_decrypt(encrypted, DEFAULT_KEY)
    
    print(f"原始数据: {test_data}")
    print(f"加密后: {encrypted}")
    print(f"解密后: {decrypted}")
    print(f"解密正确: {decrypted == test_data}")
