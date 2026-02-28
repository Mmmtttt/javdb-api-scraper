"""
JAVDB 自动登录模块
使用账号密码登录并获取 cookies
"""

import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from curl_cffi import requests
from bs4 import BeautifulSoup

import config


class JavdbLogin:
    """
    JAVDB 自动登录器
    
    功能:
    - 使用账号密码登录
    - 获取并保存 cookies
    - 自动处理登录流程
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.base_url = f"https://{config.JAVDB['domains'][0]}"
    
    def login(self, username: str = None, password: str = None) -> bool:
        """
        登录 JAVDB
        
        Args:
            username: 用户名/邮箱，如果为 None 使用配置文件中的值
            password: 密码，如果为 None 使用配置文件中的值
            
        Returns:
            是否登录成功
        """
        # 使用配置文件中的账号密码
        if username is None:
            username = config.LOGIN.get('username')
        if password is None:
            password = config.LOGIN.get('password')
        
        if not username or not password:
            print("错误: 未提供账号密码")
            return False
        
        try:
            # 1. 访问登录页面获取 authenticity_token
            login_url = f"{self.base_url}/login"
            print(f"访问登录页面: {login_url}")
            
            response = self.session.get(login_url, timeout=config.JAVDB['timeout'])
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 查找 authenticity_token
            token_input = soup.select_one('input[name="authenticity_token"]')
            if not token_input:
                print("错误: 无法获取登录 token")
                return False
            
            authenticity_token = token_input.get('value', '')
            print(f"获取到 token: {authenticity_token[:20]}...")
            
            # 2. 提交登录表单
            login_data = {
                'authenticity_token': authenticity_token,
                'user[email]': username,
                'user[password]': password,
                'user[remember_me]': '1',
            }
            
            print(f"正在登录: {username}")
            response = self.session.post(
                login_url,
                data=login_data,
                timeout=config.JAVDB['timeout'],
                allow_redirects=True
            )
            
            # 3. 检查登录结果
            if '/users/sign_in' in response.url or '登录' in response.text:
                print("错误: 登录失败，请检查账号密码")
                return False
            
            # 4. 确认已满18岁
            print("确认年龄...")
            self._confirm_over18()
            
            # 5. 保存 cookies
            self._save_cookies()
            
            print("✅ 登录成功!")
            print(f"   Cookies 已保存到: {config.COOKIE_FILE}")
            
            return True
            
        except Exception as e:
            print(f"登录出错: {e}")
            return False
    
    def _confirm_over18(self):
        """确认已满18岁"""
        try:
            url = f"{self.base_url}/over18?respond=1"
            self.session.get(url, timeout=config.JAVDB['timeout'])
            return True
        except Exception as e:
            print(f"确认年龄失败: {e}")
            return False
    
    def _save_cookies(self):
        """保存 cookies 到文件"""
        cookies = dict(self.session.cookies)
        with open(config.COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
    
    def load_cookies(self) -> bool:
        """
        从文件加载 cookies
        
        Returns:
            是否成功加载
        """
        cookie_path = Path(config.COOKIE_FILE)
        if cookie_path.exists():
            try:
                with open(cookie_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                    self.session.cookies.update(cookies)
                print(f"✅ 已加载 cookies: {config.COOKIE_FILE}")
                # 同时确认年龄
                self._confirm_over18()
                return True
            except Exception as e:
                print(f"加载 cookies 失败: {e}")
                return False
        return False
    
    def check_login_status(self) -> bool:
        """
        检查登录状态
        
        Returns:
            是否已登录
        """
        try:
            # 访问需要登录的页面
            url = f"{self.base_url}/tags"
            response = self.session.get(url, timeout=config.JAVDB['timeout'])
            
            # 如果页面包含登录链接，说明未登录
            if '/login' in response.text or '登入' in response.text:
                return False
            
            # 检查是否有用户相关信息
            soup = BeautifulSoup(response.text, 'lxml')
            user_menu = soup.select_one('.user-menu, .dropdown-toggle')
            
            return user_menu is not None
            
        except Exception as e:
            print(f"检查登录状态出错: {e}")
            return False
    
    def ensure_login(self) -> bool:
        """
        确保已登录（自动加载 cookies 或重新登录）
        
        Returns:
            是否已登录
        """
        # 先尝试加载 cookies
        if self.load_cookies():
            if self.check_login_status():
                print("✅ 使用已有 cookies 登录成功")
                return True
            else:
                print("⚠️ Cookies 已过期，需要重新登录")
        
        # 重新登录
        return self.login()


# ==================== 便捷函数 ====================

def login(username: str = None, password: str = None) -> bool:
    """
    登录 JAVDB
    
    Args:
        username: 用户名，默认使用配置文件
        password: 密码，默认使用配置文件
        
    Returns:
        是否登录成功
    """
    javdb_login = JavdbLogin()
    return javdb_login.login(username, password)


def ensure_login() -> bool:
    """
    确保已登录（自动加载 cookies 或重新登录）
    
    Returns:
        是否已登录
    """
    javdb_login = JavdbLogin()
    return javdb_login.ensure_login()


if __name__ == '__main__':
    # 测试登录
    print("=" * 70)
    print("JAVDB 自动登录")
    print("=" * 70)
    
    success = ensure_login()
    
    if success:
        print("\n✅ 登录成功!")
    else:
        print("\n❌ 登录失败!")
