# JAVDB API 完整文档

本文档详细介绍 JAVDB API Scraper 的所有功能、用法、参数和返回格式。

## 目录

1. [快速开始](#快速开始)
2. [核心 API 函数](#核心-api-函数)
3. [标签搜索系统](#标签搜索系统)
4. [数据格式详解](#数据格式详解)
5. [高级功能](#高级功能)
6. [错误处理](#错误处理)

---

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 基本配置

```python
# config.py
JAVDB = {
    'domains': ['javdb.com', 'javdb123.com'],
    'timeout': 30,
    'retry_times': 3,
    'sleep_time': 0.5
}

LOGIN = {
    'username': '',  # 可选
    'password': ''   # 可选
}
```

---

## 核心 API 函数

### 1. 视频搜索

#### `search_videos(keyword, max_pages=1, platform=None)`

搜索视频作品。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | str | 是 | 搜索关键词，如 "SSIS", "MIDA-583" |
| max_pages | int | 否 | 最大搜索页数，默认1页 |
| platform | str | 否 | 平台名称，默认使用配置中的默认平台 |

**返回:** 视频列表

```python
[
    {
        "video_id": "YwG8Ve",
        "code": "MIDA-583",
        "title": "作品标题",
        "date": "2026-03-04",
        "rating": "4.57分",
        "url": "https://javdb.com/v/YwG8Ve"
    },
    ...
]
```

**示例:**
```python
from lib import search_videos

# 搜索关键词
videos = search_videos("SSIS", max_pages=2)
for video in videos:
    print(f"{video['code']}: {video['title']}")
```

---

### 2. 获取视频详情

#### `get_video_detail(video_id, platform=None)`

获取单个视频的详细信息。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| video_id | str | 是 | 视频ID，如 "YwG8Ve" |
| platform | str | 否 | 平台名称 |

**返回:** 视频详情字典

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

**示例:**
```python
from lib import get_video_detail

detail = get_video_detail("YwG8Ve")
print(f"标题: {detail['title']}")
print(f"演员: {', '.join(detail['actors'])}")
print(f"磁力链接数: {len(detail['magnets'])}")
```

---

### 3. 根据番号搜索

#### `get_video_by_code(code, platform=None)`

根据番号（如 MIDA-583）搜索视频详情。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | str | 是 | 番号，如 "MIDA-583" |
| platform | str | 否 | 平台名称 |

**返回:** 视频详情字典（格式同上）

**示例:**
```python
from lib import get_video_by_code

detail = get_video_by_code("MIDA-583")
print(f"标题: {detail['title']}")
```

---

### 4. 演员搜索

#### `search_actor(actor_name, platform=None)`

搜索演员。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| actor_name | str | 是 | 演员名字，如 "井上もも" |
| platform | str | 否 | 平台名称 |

**返回:** 演员列表

```python
[
    {
        "actor_id": "0R1n3",
        "actor_name": "井上もも",
        "actor_url": "https://javdb.com/actors/0R1n3"
    },
    ...
]
```

**示例:**
```python
from lib import search_actor

actors = search_actor("井上もも")
for actor in actors:
    print(f"{actor['actor_name']}: {actor['actor_id']}")
```

---

### 5. 获取演员作品

#### `get_actor_works(actor_id, page=1, max_pages=1, full_detail=False, platform=None)`

获取演员的作品列表。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| actor_id | str | 是 | 演员ID，如 "0R1n3" |
| page | int | 否 | 起始页码，默认1 |
| max_pages | int | 否 | 最大页数，默认1 |
| full_detail | bool | 否 | 是否获取完整详情，默认False |
| platform | str | 否 | 平台名称 |

**返回:** 作品列表和分页信息

```python
{
    "page": 1,
    "has_next": True,
    "actor_id": "0R1n3",
    "actor_name": "井上もも",
    "works": [
        {
            "video_id": "YwG8Ve",
            "code": "MIDA-583",
            "title": "作品标题",
            "date": "2026-03-04",
            "rating": "4.57分",
            "url": "https://javdb.com/v/YwG8Ve"
        },
        ...
    ]
}
```

**示例:**
```python
from lib import get_actor_works

result = get_actor_works("0R1n3", max_pages=2)
print(f"演员: {result['actor_name']}")
print(f"作品数: {len(result['works'])}")
for work in result['works']:
    print(f"  {work['code']}: {work['title']}")
```

---

## 标签搜索系统

### 1. 多标签组合搜索

#### `search_by_tags(page=1, **tag_params)`

多类标签组合搜索，支持多种输入方式。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| **tag_params | dict | 是 | 标签参数，支持多种格式 |

**标签参数格式:**

| 格式 | 示例 | 说明 |
|------|------|------|
| 直接标签名 | `**{"淫亂真實": ""}` | 最简单方式 |
| tags列表 | `tags=["淫亂真實", "水手服"]` | 多标签组合 |
| 带分类前缀 | `tag_主題="淫亂真實"` | 精确指定分类 |
| 传统ID | `c1=23, c3=78` | 向后兼容 |

**返回:** 作品列表和标签信息

```python
{
    "page": 1,
    "has_next": True,
    "tag_params": {"c1": 23, "c3": 78},
    "works": [
        {
            "video_id": "YwG8Ve",
            "code": "MIDA-583",
            "title": "作品标题",
            "date": "2026-03-04",
            "rating": "4.57分",
            "url": "https://javdb.com/v/YwG8Ve"
        },
        ...
    ]
}
```

**示例:**
```python
from javdb_api import search_by_tags

# 方式1: 最简单 - 直接输入标签名
result = search_by_tags(page=1, **{"淫亂真實": ""})
# 输出: ✓ 找到标签 '淫亂真實' -> c1=23

# 方式2: 使用 tags 列表（多标签）
result = search_by_tags(page=1, tags=["淫亂真實", "水手服"])
# 输出: ✓ 找到标签 '淫亂真實' -> c1=23
#       ✓ 找到标签 '水手服' -> c3=78

# 方式3: 简体自动转繁体
result = search_by_tags(page=1, **{"淫乱真实": ""})
# 输出: ✓ 找到标签 '淫乱真实' -> c1=23

# 方式4: 带分类前缀（更精确）
result = search_by_tags(page=1, tag_主題="淫亂真實")

# 方式5: 传统ID模式（向后兼容）
result = search_by_tags(page=1, c1=23, c3=78)
```

---

### 2. 标签全量搜索

#### `search_by_tags_full(page=1, download_images=False, **tag_params)`

多标签组合搜索（全量信息），包含作品完整详情。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| download_images | bool | 否 | 是否下载缩略图，默认False |
| **tag_params | dict | 是 | 标签参数（同上） |

**返回:** 包含完整详情的作品列表

```python
{
    "page": 1,
    "has_next": True,
    "tag_params": {"c1": 23},
    "works": [
        {
            "video_id": "YwG8Ve",
            "code": "MIDA-583",
            "title": "作品标题",
            "date": "2026-03-04",
            "tags": ["美少女電影", "單體作品"],
            "actors": ["井上もも"],
            "series": "系列名",
            "magnets": [...],
            "thumbnail_images": [...],
            "cover_url": "https://..."
        },
        ...
    ]
}
```

**示例:**
```python
from javdb_api import search_by_tags_full

result = search_by_tags_full(
    page=1,
    download_images=True,
    tags=["淫亂真實", "水手服"]
)

for work in result['works']:
    print(f"{work['code']}: {work['title']}")
    print(f"  演员: {', '.join(work['actors'])}")
    print(f"  标签: {', '.join(work['tags'])}")
```

---

### 3. 演员作品标签筛选

#### `get_actor_works_with_tags(actor_id, tag_names=None, tag_ids=None, max_pages=1, get_details=False, save_temp=True, temp_file=None)`

获取演员作品并按标签筛选。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| actor_id | str | 是 | 演员ID |
| tag_names | list | 否 | 标签名称列表，如 ["美少女", "水手服"] |
| tag_ids | list | 否 | 标签ID列表，如 ["c1=23", "c3=78"] |
| max_pages | int | 否 | 最大页数，默认1 |
| get_details | bool | 否 | 是否获取详细信息，默认False |
| save_temp | bool | 否 | 是否保存到临时文件，默认True |
| temp_file | str | 否 | 临时文件路径 |

**返回:** 筛选后的作品信息

```python
{
    "actor_id": "NeOr",
    "actor_name": "永野一夏",
    "total_works": 50,
    "filtered_works": 12,
    "tags": ["美少女", "水手服"],
    "works": [
        {
            "video_id": "...",
            "code": "...",
            "title": "...",
            "tags": ["美少女", "水手服", "..."]
        },
        ...
    ]
}
```

**示例:**
```python
from javdb_api import JavdbAPI

api = JavdbAPI()

# 按标签名称筛选
result = api.get_actor_works_with_tags(
    actor_id="NeOr",
    tag_names=["美少女"],
    max_pages=1,
    get_details=True
)

print(f"总作品: {result['total_works']}")
print(f"筛选后: {result['filtered_works']}")

# 按标签ID筛选（多标签组合）
result = api.get_actor_works_with_tags(
    actor_id="NeOr",
    tag_ids=["c1=23", "c3=78"],
    max_pages=1
)
```

---

## 数据格式详解

### 视频基础信息

```python
{
    "video_id": "YwG8Ve",           # 视频唯一ID
    "code": "MIDA-583",             # 番号
    "title": "作品标题",             # 标题
    "date": "2026-03-04",           # 发布日期
    "rating": "4.57分",             # 评分
    "url": "https://javdb.com/v/YwG8Ve"  # 详情页URL
}
```

### 视频完整详情

```python
{
    "video_id": "YwG8Ve",
    "code": "MIDA-583",
    "title": "作品标题",
    "date": "2026-03-04",
    "tags": ["美少女電影", "單體作品", "情侶"],  # 标签列表
    "actors": ["井上もも"],                      # 演员列表
    "series": "系列名",                          # 系列名称
    "magnets": [                                 # 磁力链接列表
        {
            "magnet": "magnet:?xt=urn:btih:...",
            "size_text": "5.27GB",
            "size_mb": 5396.48
        }
    ],
    "thumbnail_images": [                        # 预览图列表
        "https://c0.jdbstatic.com/samples/yw/YwG8Ve_l_0.jpg",
        "https://c0.jdbstatic.com/samples/yw/YwG8Ve_l_1.jpg"
    ],
    "preview_video": "",                         # 预览视频URL
    "cover_url": "https://c0.jdbstatic.com/covers/yw/YwG8Ve.jpg"  # 封面图
}
```

### 演员信息

```python
{
    "actor_id": "0R1n3",                          # 演员ID
    "actor_name": "井上もも",                      # 演员名字
    "actor_url": "https://javdb.com/actors/0R1n3"  # 演员主页
}
```

### 标签信息

```python
{
    "id": "c1=23",           # 完整标签ID
    "name": "淫亂真實",       # 标签名称
    "category": "c1",         # 分类代码
    "category_name": "主題",   # 分类名称
    "tag_id": 23,             # 标签数字ID
    "value": "23"             # 标签值
}
```

---

## 高级功能

### 1. 标签管理器

#### `TagManager` 类

用于管理标签信息，支持从加密数据库加载。

```python
from lib.tag_manager import TagManager

tag_manager = TagManager()

# 通过名称查找标签
tag_info = tag_manager.get_tag_by_name("淫亂真實")
print(f"标签ID: {tag_info['id']}")
print(f"分类: {tag_info['category_name']}")

# 通过ID查找标签
tag_info = tag_manager.get_tag_by_id("c1=23")
print(f"标签名称: {tag_info['name']}")

# 关键词搜索
tags = tag_manager.search_tags_by_keyword("美女")
for tag in tags:
    print(f"{tag['name']}: {tag['id']}")

# 获取分类下的所有标签
tags = tag_manager.get_tags_by_category("c1")
```

### 2. 加密工具

#### `CryptoUtils` 类

提供 XOR 加密解密功能。

```python
from lib.crypto_utils import CryptoUtils, DEFAULT_KEY

# 加密数据
encrypted = CryptoUtils.xor_encrypt("Hello, World!", DEFAULT_KEY)

# 解密数据
decrypted = CryptoUtils.xor_decrypt(encrypted, DEFAULT_KEY)

# 加密文件
CryptoUtils.encrypt_file("input.txt", "output.enc", DEFAULT_KEY)

# 解密文件
content = CryptoUtils.decrypt_file("output.enc", DEFAULT_KEY)
```

### 3. 自动登录

#### `auto_login(timeout=300)`

自动化登录流程，打开浏览器引导用户完成登录。

```python
from lib import auto_login

# 启动自动登录
success = auto_login(timeout=300)  # 等待5分钟

# 流程:
# 1. 自动打开浏览器，显示登录助手页面
# 2. 在页面中点击按钮打开 JAVDB 登录页
# 3. 在 JAVDB 中完成登录
# 4. 从浏览器复制 cookies 并粘贴到助手页面
# 5. 提交后自动保存到 cookies.json
```

### 4. 图片下载

#### `download_video_images(video_id, download_dir=None)`

下载视频缩略图。

```python
from lib import download_video_images

# 下载缩略图
success, total = download_video_images("YwG8Ve", download_dir="./images")
print(f"下载完成: {success}/{total}")
```

---

## 错误处理

### 常见错误

| 错误类型 | 说明 | 解决方案 |
|----------|------|----------|
| `ValueError: 未找到标签` | 标签名称不存在 | 检查标签名称拼写，或尝试简体/繁体 |
| `ConnectionError` | 网络连接失败 | 检查网络，或更换域名 |
| `LoginRequiredError` | 需要登录 | 调用 `auto_login()` 完成登录 |
| `ValueError: 至少需要提供一个标签参数` | 标签参数为空 | 确保提供了有效的标签参数 |

### 错误处理示例

```python
from javdb_api import search_by_tags

try:
    result = search_by_tags(page=1, **{"不存在的标签": ""})
except ValueError as e:
    print(f"标签错误: {e}")
    # 尝试搜索相似标签
    from lib.tag_manager import TagManager
    tm = TagManager()
    similar = tm.search_tags_by_keyword("不存在")
    if similar:
        print(f"您是否要找: {similar[0]['name']}?")

# 网络错误处理
from lib import search_videos
import time

for i in range(3):  # 重试3次
    try:
        videos = search_videos("SSIS", max_pages=1)
        break
    except ConnectionError as e:
        print(f"连接失败，第{i+1}次重试...")
        time.sleep(2)
```

---

## 完整示例

### 示例1: 搜索并下载视频信息

```python
from lib import search_videos, get_video_detail, download_video_images

# 搜索视频
videos = search_videos("SSIS", max_pages=1)

for video in videos[:3]:  # 处理前3个
    print(f"\n处理: {video['code']}")
    
    # 获取详情
    detail = get_video_detail(video['video_id'])
    
    # 打印信息
    print(f"  标题: {detail['title']}")
    print(f"  演员: {', '.join(detail['actors'])}")
    print(f"  标签: {', '.join(detail['tags'])}")
    print(f"  磁力: {len(detail['magnets'])} 个")
    
    # 下载图片
    success, total = download_video_images(video['video_id'], f"./images/{video['code']}")
    print(f"  图片: {success}/{total}")
```

### 示例2: 演员作品标签筛选

```python
from javdb_api import JavdbAPI

api = JavdbAPI()

# 获取演员作品并按标签筛选
result = api.get_actor_works_with_tags(
    actor_id="NeOr",           # 永野一夏
    tag_names=["美少女", "水手服"],
    max_pages=2,
    get_details=True
)

print(f"演员: {result['actor_name']}")
print(f"总作品: {result['total_works']}")
print(f"筛选后: {result['filtered_works']}")
print(f"筛选标签: {', '.join(result['tags'])}")

for work in result['works']:
    print(f"\n{work['code']}: {work['title']}")
    print(f"  标签: {', '.join(work['tags'])}")
```

### 示例3: 多标签组合搜索

```python
from javdb_api import search_by_tags_full

# 多标签组合搜索
result = search_by_tags_full(
    page=1,
    tags=["淫亂真實", "水手服"],  # 多标签组合
    download_images=False
)

print(f"找到 {len(result['works'])} 个作品")
print(f"标签参数: {result['tag_params']}")

for work in result['works'][:5]:
    print(f"{work['code']}: {work['title']}")
```

---

## 注意事项

1. **请求频率**: 建议设置适当的 `sleep_time` 避免被封IP
2. **Cookie 管理**: 登录后 cookies 会自动保存，下次使用时会自动加载
3. **临时文件**: 演员作品筛选会自动保存临时文件，避免重复请求
4. **标签数据库**: 标签信息从加密数据库加载，首次加载可能需要几秒钟

---

## 许可证

MIT License
