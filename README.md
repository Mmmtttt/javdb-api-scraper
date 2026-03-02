# JAVDB API Scraper

JAVDB 视频平台 API 抓取工具，采用适配器模式设计，支持多种视频平台的统一接口访问。

## 架构设计

```
javdb-api-scraper/
├── lib/                          # 核心库
│   ├── __init__.py               # 库入口，导出所有公共接口
│   ├── platform.py               # 平台枚举和ID处理
│   ├── base_adapter.py           # 适配器基类
│   ├── javdb_adapter.py          # JAVDB平台适配器
│   ├── adapter_factory.py        # 适配器工厂
│   ├── external_api.py           # 统一外部API接口
│   ├── crypto_utils.py           # 加密/解密工具
│   └── login.py                 # 登录功能
├── test/                        # 测试目录
│   ├── README.md                 # 测试说明
│   └── verify_api.py            # API验证测试
├── javdb_api.py                 # 原始JAVDB API实现
├── config.example.py             # 配置示例
├── third_party_config.json       # 第三方API配置
├── requirements.txt              # 依赖
└── README.md                    # 本文档
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. 复制配置示例文件：
```bash
cp config.example.py config.py
```

2. 编辑 `config.py`，配置域名、超时时间等参数

3. （可选）如需登录功能，配置账号密码

### 使用统一 API 接口

```python
from lib import (
    search_videos,
    get_video_detail,
    get_video_by_code,
    search_actor,
    get_actor_works,
)

# 搜索视频
videos = search_videos("SSIS", max_pages=2)
for video in videos:
    print(f"{video['code']}: {video['title']}")

# 获取视频详情
detail = get_video_detail("YwG8Ve")
print(f"标题: {detail['title']}")
print(f"磁力链接: {detail['magnets']}")

# 根据番号搜索
detail = get_video_by_code("MIDA-583")
print(f"标题: {detail['title']}")

# 搜索演员
actors = search_actor("井上もも")
for actor in actors:
    print(f"{actor['actor_name']}: {actor['actor_id']}")

# 获取演员作品
result = get_actor_works("0R1n3", max_pages=2)
for work in result['works']:
    print(f"{work['code']}: {work['title']}")
```

### 使用适配器模式

```python
from lib import AdapterFactory, Platform

# 获取适配器
adapter = AdapterFactory.get_adapter(Platform.JAVDB)

# 使用适配器方法
videos = adapter.search_videos("SSIS", max_pages=2)
detail = adapter.get_video_detail("YwG8Ve")

# 转换为标准格式
data = adapter.convert_to_standard_format(videos)
print(f"视频数: {len(data['videos'])}")
print(f"标签数: {len(data['tags'])}")
```

### 使用加密功能

```python
from lib import CryptoUtils, DEFAULT_KEY

# 加密数据
encrypted = CryptoUtils.xor_encrypt("Hello, World!", DEFAULT_KEY)

# 解密数据
decrypted = CryptoUtils.xor_decrypt(encrypted, DEFAULT_KEY)

# 加密文件
CryptoUtils.encrypt_file("input.txt", "output.enc", DEFAULT_KEY)

# 解密文件
content = CryptoUtils.decrypt_file("output.enc", DEFAULT_KEY)
```

### 使用登录功能

```python
from lib import login, ensure_login

# 登录（使用配置文件中的账号密码）
success = login()

# 自动登录（先尝试加载 cookies，过期则重新登录）
success = ensure_login()
```

## API 参考

### 视频相关

#### `search_videos(keyword, max_pages=1, platform=None)`
搜索视频

**参数:**
- `keyword`: 搜索关键词
- `max_pages`: 最大搜索页数
- `platform`: 平台名称，默认使用配置中的默认平台

**返回:** 视频列表

#### `get_video_detail(video_id, platform=None)`
获取视频详情

**参数:**
- `video_id`: 视频ID
- `platform`: 平台名称

**返回:** 视频详情字典

#### `get_video_by_code(code, platform=None)`
根据番号获取视频详情

**参数:**
- `code`: 番号（如 MIDA-583）
- `platform`: 平台名称

**返回:** 视频详情字典

### 演员相关

#### `search_actor(actor_name, platform=None)`
搜索演员

**参数:**
- `actor_name`: 演员名字
- `platform`: 平台名称

**返回:** 演员列表

#### `get_actor_works(actor_id, page=1, max_pages=1, full_detail=False, platform=None)`
获取演员作品

**参数:**
- `actor_id`: 演员ID
- `page`: 起始页码
- `max_pages`: 最大页数
- `full_detail`: 是否获取完整详情
- `platform`: 平台名称

**返回:** 作品列表和分页信息

### 标签相关

#### `get_tag_works(tag_id, page=1, max_pages=1, platform=None)`
获取标签作品

**参数:**
- `tag_id`: 标签ID
- `page`: 起始页码
- `max_pages`: 最大页数
- `platform`: 平台名称

**返回:** 作品列表和分页信息

#### `search_by_tags(page=1, max_pages=1, platform=None, **tag_params)`
多标签组合搜索

**参数:**
- `page`: 起始页码
- `max_pages`: 最大页数
- `platform`: 平台名称
- `**tag_params`: 标签参数，如 c1=23, c3=78

**返回:** 作品列表和分页信息

### 下载相关

#### `download_video_images(video_id, download_dir=None, platform=None)`
下载视频缩略图

**参数:**
- `video_id`: 视频ID
- `download_dir`: 下载目录
- `platform`: 平台名称

**返回:** (成功下载数, 总数)

### 数据转换

#### `convert_to_standard_format(videos, platform=None)`
将平台数据转换为系统标准格式

**参数:**
- `videos`: 视频数据列表
- `platform`: 平台名称

**返回:** 标准格式的视频和标签数据

## 数据格式

### 视频详情格式

```python
{
    "video_id": "YwG8Ve",
    "code": "MIDA-583",
    "title": "作品标题",
    "date": "2026-03-04",
    "tags": ["美少女電影", "單體作品", "情侶"],
    "actors": ["井上もも"],
    "series": "系列名",
    "magnets": [
        {
            "magnet": "magnet:?xt=urn:btih:...",
            "size_text": "5.27GB",
            "size_mb": 5396.48
        }
    ],
    "thumbnail_images": [
        "https://c0.jdbstatic.com/samples/yw/YwG8Ve_l_0.jpg",
        ...
    ],
    "preview_video": "",
    "cover_url": "https://c0.jdbstatic.com/covers/yw/YwG8Ve.jpg"
}
```

### 标准格式

```python
{
    "videos": [
        {
            "id": "JAVDB_YwG8Ve",
            "video_id": "YwG8Ve",
            "code": "MIDA-583",
            "title": "作品标题",
            "date": "2026-03-04",
            "cover_path": "https://...",
            "thumbnail_images": [...],
            "magnets": [...],
            "actors": ["井上もも"],
            "series": "",
            "rating": "4.57分",
            "tag_ids": ["tag_001", "tag_002"],
            "create_time": "2026-03-02T10:00:00",
            "last_read_time": "2026-03-02T10:00:00",
            "is_deleted": False
        }
    ],
    "tags": [
        {
            "id": "tag_001",
            "name": "美少女電影",
            "create_time": "2026-03-02T10:00:00"
        }
    ]
}
```

## 添加新平台

要添加新的视频平台，需要：

1. 在 `lib/platform.py` 中添加平台枚举
2. 创建新的适配器类，继承 `BaseAdapter`
3. 在 `lib/adapter_factory.py` 中注册适配器
4. 在 `third_party_config.json` 中添加配置

## 配置

编辑 `config.py` 文件：

```python
JAVDB = {
    'domains': ['javdb.com', 'javdb123.com'],
    'timeout': 30,
    'retry_times': 3,
    'sleep_time': 0.5
}

LOGIN = {
    'username': 'your_email@example.com',
    'password': 'your_password'
}
```

## 测试

运行 API 验证测试：

```bash
cd test
python verify_api.py
```

## 许可证

MIT License
