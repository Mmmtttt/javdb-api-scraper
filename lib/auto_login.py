"""
自动化登录辅助模块
使用本地服务器接收浏览器登录后的 cookies
"""

import json
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import time

import config


class CookieReceiverHandler(BaseHTTPRequestHandler):
    """Cookie 接收处理器"""
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/':
            # 返回登录页面
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JAVDB 登录助手</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .step {
            margin: 20px 0;
            padding: 15px;
            background: #e8f4f8;
            border-left: 4px solid #2196F3;
        }
        .step h3 {
            margin-top: 0;
            color: #2196F3;
        }
        .code {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            margin: 10px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 0;
        }
        button:hover {
            background: #45a049;
        }
        .success {
            color: #4CAF50;
            font-weight: bold;
        }
        .error {
            color: #f44336;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 JAVDB 自动登录助手</h1>
        
        <div class="step">
            <h3>步骤 1: 点击下方按钮打开 JAVDB 登录页面</h3>
            <button onclick="openJavdb()">打开 JAVDB 登录页面</button>
        </div>
        
        <div class="step">
            <h3>步骤 2: 在新打开的浏览器窗口中登录</h3>
            <p>使用您的账号密码登录 JAVDB</p>
        </div>
        
        <div class="step">
            <h3>步骤 3: 登录后，导出 Cookies</h3>
            <p>在浏览器中按 F12 打开开发者工具，然后：</p>
            <ol>
                <li>切换到 "Application" 或 "存储" 标签</li>
                <li>在左侧找到 "Cookies" → "https://javdb.com"</li>
                <li>右键点击 Cookies 文件夹，选择 "Copy all cookies" 或类似选项</li>
                <li>或者使用浏览器扩展（如 EditThisCookie）导出 cookies</li>
            </ol>
        </div>
        
        <div class="step">
            <h3>步骤 4: 粘贴 Cookies 到下方文本框</h3>
            <textarea id="cookieInput" rows="10" style="width:100%;padding:10px;margin:10px 0;" 
                placeholder='粘贴 cookies JSON 格式，例如：
[
  {
    "name": "_jdb_session",
    "value": "...",
    "domain": ".javdb.com"
  }
]'></textarea>
            <button onclick="submitCookies()">提交 Cookies</button>
        </div>
        
        <div id="result"></div>
    </div>
    
    <script>
        function openJavdb() {
            window.open('https://javdb.com/login', '_blank');
        }
        
        function submitCookies() {
            const cookieInput = document.getElementById('cookieInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!cookieInput.trim()) {
                resultDiv.innerHTML = '<p class="error">请先粘贴 cookies！</p>';
                return;
            }
            
            try {
                const cookies = JSON.parse(cookieInput);
                
                fetch('/save-cookies', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({cookies: cookies})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        resultDiv.innerHTML = '<p class="success">✅ Cookies 保存成功！现在可以关闭此页面。</p>';
                    } else {
                        resultDiv.innerHTML = '<p class="error">❌ 保存失败: ' + data.error + '</p>';
                    }
                })
                .catch(error => {
                    resultDiv.innerHTML = '<p class="error">❌ 提交失败: ' + error.message + '</p>';
                });
            } catch (e) {
                resultDiv.innerHTML = '<p class="error">❌ JSON 格式错误: ' + e.message + '</p>';
            }
        }
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode('utf-8'))
        
        elif self.path == '/save-cookies':
            # 保存 cookies
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                cookies = data.get('cookies', [])
                
                # 转换为字典格式
                cookie_dict = {}
                for cookie in cookies:
                    name = cookie.get('name')
                    value = cookie.get('value')
                    if name and value:
                        cookie_dict[name] = value
                
                # 保存到文件
                with open(config.COOKIE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cookie_dict, f, indent=2, ensure_ascii=False)
                
                # 返回成功
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': True, 'message': 'Cookies saved successfully'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
                print(f"✅ Cookies 已保存到 {config.COOKIE_FILE}")
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'error': str(e)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print(f"❌ 保存 cookies 失败: {e}")
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass


class AutoLogin:
    """自动化登录助手"""
    
    def __init__(self, port=8888):
        self.port = port
        self.server = None
        self.server_thread = None
    
    def start_server(self):
        """启动本地服务器"""
        try:
            self.server = HTTPServer(('localhost', self.port), CookieReceiverHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            print(f"✅ 本地服务器已启动: http://localhost:{self.port}")
            return True
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"⚠️  端口 {self.port} 已被占用，尝试使用其他端口...")
                self.port += 1
                return self.start_server()
            else:
                print(f"❌ 启动服务器失败: {e}")
                return False
    
    def stop_server(self):
        """停止服务器"""
        if self.server:
            self.server.shutdown()
            print("✅ 本地服务器已停止")
    
    def open_login_page(self):
        """打开登录助手页面"""
        url = f"http://localhost:{self.port}"
        print(f"🌐 正在打开浏览器: {url}")
        webbrowser.open(url)
    
    def wait_for_cookies(self, timeout=300):
        """等待 cookies 保存"""
        print(f"⏳ 等待用户登录并提交 cookies (最长 {timeout} 秒)...")
        print(f"💡 提示: 请在浏览器中完成登录并提交 cookies")
        
        cookie_file = Path(config.COOKIE_FILE)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if cookie_file.exists():
                file_time = cookie_file.stat().st_mtime
                if file_time > start_time:
                    print("✅ 检测到 cookies 已更新！")
                    return True
            time.sleep(1)
        
        print(f"⏱️  等待超时 ({timeout} 秒)")
        return False
    
    def run(self, timeout=300):
        """运行自动化登录流程"""
        print("=" * 70)
        print("🔐 JAVDB 自动化登录助手")
        print("=" * 70)
        
        # 启动服务器
        if not self.start_server():
            return False
        
        # 打开浏览器
        self.open_login_page()
        
        # 等待 cookies
        success = self.wait_for_cookies(timeout)
        
        # 停止服务器
        self.stop_server()
        
        return success


def auto_login(timeout=300):
    """
    自动化登录函数
    
    Args:
        timeout: 等待超时时间（秒），默认 5 分钟
        
    Returns:
        是否成功获取 cookies
    """
    login_helper = AutoLogin()
    return login_helper.run(timeout)


if __name__ == "__main__":
    print("启动 JAVDB 自动化登录助手...")
    auto_login()
