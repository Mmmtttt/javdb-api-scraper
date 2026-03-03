# JAVDB API 完整文档

本文档详细介绍 JAVDB API Scraper 的所有功能、用法、参数和返回格式。

## 目录

1. [7个核心 API 接口](#7个核心-api-接口)
2. [快速开始](#快速开始)
3. [其他 API 函数](#其他-api-函数)
4. [多平台支持](#多平台支持)
5. [标签搜索系统](#标签搜索系统)
6. [数据格式详解](#数据格式详解)
7. [错误处理](#错误处理)
8. [附录：AV 在线播放器](#附录av-在线播放器)

---

## 7个核心 API 接口

以下是 API 中最重要的7个功能，按重要性排序：

### 1. 搜索演员的作品ID列表

#### `search_actor_works(actor_id, start=0, end=20, platform=None)`

搜索演员的作品ID列表，支持传入起始个数和结束个数。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| actor_id | str | 是 | 演员ID |
| start | int | 否 | 起始个数（从0开始），默认0 |
| end | int | 否 | 结束个数（不包含），默认20 |
| platform | str | 否 | 平台名称：'javdb'(默认) 或 'javbus' |

**返回:** 作品列表

```python
[
    {
        "video_id": "YwG8Ve",
        "code": "MIDA-583",
        "title": "作品标题",
        "date": "2026-03-04",
        "rating": "4.57分"
    },
    ...
]
```

**示例:**
```python
from lib import search_actor_works

# 获取演员前20个作品
works = search_actor_works("0R1n3", start=0, end=20)
for work in works:
    print(f"{work['code']}: {work['title']}")

# 获取第21-40个作品
works = search_actor_works("0R1n3", start=20, end=40)

# 使用 JavBus 平台
works = search_actor_works("star_id", start=0, end=20, platform="javbus")
```

---

### 2. 通过作品ID获取作品详细信息

#### `get_video_detail(video_id, platform=None)`

通过作品ID获取作品的详细信息，包括标题、标签、作者、磁力链接等。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| video_id | str | 是 | 作品ID |
| platform | str | 否 | 平台名称：'javdb'(默认) 或 'javbus' |

**返回:** 作品详情字典

```python
{
    "video_id": "YwG8Ve",
    "code": "MIDA-583",
    "title": "作品标题",
    "date": "2026-03-04",
    "tags": ["美少女電影", "單體作品"],
    "actors": ["井上もも"],
    "series": "系列名",
    "magnets": [
        {"magnet": "magnet:?xt=urn:btih:...", "size_text": "5.27GB"}
    ],
    "thumbnail_images": ["https://.../1.jpg", "https://.../2.jpg"],
    "cover_url": "https://.../cover.jpg"
}
```

**示例:**
```python
from lib import get_video_detail

# 获取作品详情
detail = get_video_detail("YwG8Ve")
print(f"标题: {detail['title']}")
print(f"演员: {', '.join(detail['actors'])}")
print(f"标签: {', '.join(detail['tags'])}")
print(f"磁力链接: {len(detail['magnets'])} 个")

# 使用 JavBus 平台
detail = get_video_detail("SSIS-865", platform="javbus")
```

---

### 3. 通过作品ID下载高清预览图和封面

#### `download_video_images(video_id, output_dir="output/images", platform=None)`

通过作品ID获取作品的高清预览图和封面并下载。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| video_id | str | 是 | 作品ID |
| output_dir | str | 否 | 输出目录，默认"output/images" |
| platform | str | 否 | 平台名称：'javdb'(默认) 或 'javbus' |

**返回:** 下载结果字典

```python
{
    "downloaded": 10,           # 成功下载数量
    "total": 12,                # 总数量
    "success_rate": 83.3,       # 成功率（百分比）
    "download_dir": "output/images/MIDA-583",  # 下载目录
    "files": [".../cover.jpg", ".../preview_001.jpg", ...]  # 文件路径列表
}
```

**示例:**
```python
from lib import download_video_images

# 下载作品图片
result = download_video_images("YwG8Ve", output_dir="./images")
print(f"下载完成: {result['downloaded']}/{result['total']}")
print(f"保存位置: {result['download_dir']}")

# 使用 JavBus 平台
result = download_video_images("SSIS-865", platform="javbus")
```

---

### 4. 通过标签内容搜索作品ID列表

#### `search_videos_by_tags(tag_names, start=0, end=20, platform=None)`

通过标签的内容搜索作品ID列表，支持多个标签同时搜索。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tag_names | list | 是 | 标签名称列表，如["美少女", "水手服"] |
| start | int | 否 | 起始个数（从0开始），默认0 |
| end | int | 否 | 结束个数（不包含），默认20 |
| platform | str | 否 | 平台名称：'javdb'(默认) 或 'javbus' |

**返回:** 作品列表

```python
[
    {
        "video_id": "YwG8Ve",
        "code": "MIDA-583",
        "title": "作品标题",
        "date": "2026-03-04"
    },
    ...
]
```

**注意:**
- JavBus 不支持标签搜索，使用 JavBus 时会返回空列表
- 标签名称支持简体中文自动转换为繁体中文

**示例:**
```python
from lib import search_videos_by_tags

# 单标签搜索
works = search_videos_by_tags(["美少女"], start=0, end=20)

# 多标签组合搜索（同时包含所有标签）
works = search_videos_by_tags(["美少女", "水手服"], start=0, end=20)

# 获取第21-40个结果
works = search_videos_by_tags(["美少女"], start=20, end=40)
```

---

### 5. 搜索已登录用户的所有清单名称

#### `get_user_lists()`

搜索已登录用户的所有清单名称（想看、看过、自定义清单等）。

**注意:**
- 此功能仅支持 JAVDB 平台
- 需要先登录才能使用

**返回:** 清单列表

```python
[
    {
        "list_id": "0W97k",
        "list_name": "我的收藏",
        "list_url": "https://javdb.com/users/list_detail?id=0W97k",
        "video_count": 50
    },
    ...
]
```

**示例:**
```python
from lib import get_user_lists

# 获取用户清单
lists = get_user_lists()
for lst in lists:
    print(f"{lst['list_name']}: {lst['video_count']} 个作品")
```

---

### 6. 在用户的某清单中搜索所有作品ID列表

#### `get_list_works(list_id, start=0, end=20)`

在用户的某清单中搜索所有作品ID列表，支持传入起始个数和结束个数。

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| list_id | str | 是 | 清单ID |
| start | int | 否 | 起始个数（从0开始），默认0 |
| end | int | 否 | 结束个数（不包含），默认20 |

**注意:**
- 此功能仅支持 JAVDB 平台
- 需要先登录才能使用

**返回:** 作品列表

```python
[
    {
        "video_id": "YwG8Ve",
        "code": "MIDA-583",
        "title": "作品标题",
        "date": "2026-03-04"
    },
    ...
]
```

**示例:**
```python
from lib import get_list_works

# 获取清单前20个作品
works = get_list_works("0W97k", start=0, end=20)

# 获取第21-40个作品
works = get_list_works("0W97k", start=20, end=40)
```

---

### 7. 支持登录

#### `login()`

引导用户完成 JAVDB 登录流程，保存登录凭证。

**注意:**
- 此功能仅支持 JAVDB 平台
- 会打开浏览器引导用户完成登录
- 登录凭证会保存到 cookies.json

**返回:** 登录是否成功 (bool)

**示例:**
```python
from lib import login

# 登录
success = login()
if success:
    print("登录成功")
else:
    print("登录失败")
```

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

### 快速使用示例

```python
from lib import (
    search_actor_works,
    get_video_detail,
    download_video_images,
    search_videos_by_tags,
    get_user_lists,
    get_list_works,
    login
)

# 1. 登录
success = login()

# 2. 获取演员作品
works = search_actor_works("0R1n3", start=0, end=20)

# 3. 获取作品详情
detail = get_video_detail("YwG8Ve")

# 4. 下载图片
result = download_video_images("YwG8Ve", output_dir="./images")

# 5. 标签搜索
works = search_videos_by_tags(["美少女", "水手服"], start=0, end=20)

# 6. 获取用户清单
lists = get_user_lists()

# 7. 获取清单作品
works = get_list_works("0W97k", start=0, end=20)
```

---

## 其他 API 函数

### 视频搜索

#### `search_videos(keyword, max_pages=1, platform=None)`

搜索视频作品。

**示例:**
```python
from lib import search_videos

videos = search_videos("SSIS", max_pages=2)
for video in videos:
    print(f"{video['code']}: {video['title']}")
```

### 根据番号获取详情

#### `get_video_by_code(code, platform=None)`

根据番号获取视频详情。

**示例:**
```python
from lib import get_video_by_code

detail = get_video_by_code("MIDA-583")
print(detail['title'])
```

### 搜索演员

#### `search_actor(actor_name, platform=None)`

搜索演员。

**示例:**
```python
from lib import search_actor

actors = search_actor("井上もも")
for actor in actors:
    print(f"{actor['actor_name']}: {actor['actor_id']}")
```

### 获取演员作品（分页方式）

#### `get_actor_works(actor_id, page=1, max_pages=1, platform=None)`

获取演员作品（使用页码方式）。

**示例:**
```python
from lib import get_actor_works

result = get_actor_works("0R1n3", max_pages=2)
for work in result['works']:
    print(f"{work['code']}: {work['title']}")
```

### 获取磁力链接

#### `get_movie_magnets(video_id, platform=None, gid=None, uc=None)`

获取影片磁力链接（主要支持 JavBus）。

**示例:**
```python
from lib import get_video_detail, get_movie_magnets

# 先获取详情获取 gid 和 uc
detail = get_video_detail("SSIS-865", platform="javbus")
magnets = get_movie_magnets("SSIS-865", platform="javbus",
                            gid=detail['gid'], uc=detail['uc'])
for magnet in magnets:
    print(f"{magnet['title']}: {magnet['size']}")
```

---

## 多平台支持

本库支持多个数据源平台，可以在调用 API 时通过 `platform` 参数指定。

### 支持的平台

| 平台 | 名称 | 特点 | 支持功能 |
|------|------|------|----------|
| **javdb** | JAVDB | 需要登录，有清单功能 | 完整功能 |
| **javbus** | JavBus | 无需登录，有码/无码分类 | 搜索、详情、磁力链接 |

### 平台对比

| 功能 | JAVDB | JavBus |
|------|-------|--------|
| 搜索视频 | ✅ | ✅ |
| 视频详情 | ✅ | ✅ |
| 磁力链接 | ✅ | ✅ |
| 演员搜索 | ✅ | ⚠️ 有限支持 |
| 演员作品 | ✅ | ✅ |
| 标签搜索 | ✅ | ❌ |
| 用户清单 | ✅ | ❌ |
| 登录功能 | ✅ 必需 | ❌ 不需要 |
| 有码/无码分类 | ❌ | ✅ |

### 使用示例

#### 设置默认平台

```python
from lib import set_default_platform

# 设置默认使用 JavBus
set_default_platform("javbus")
```

#### JavBus 特有功能

```python
from lib import search_videos, get_video_detail

# 搜索有码影片（默认）
videos = search_videos("SSIS", platform="javbus", movie_type="normal")

# 搜索无码影片
videos = search_videos("SSIS", platform="javbus", movie_type="uncensored")

# 获取影片详情
detail = get_video_detail("SSIS-865", platform="javbus", movie_type="uncensored")
```

---

## 标签搜索系统

### 通过标签名称搜索

使用 `search_videos_by_tags` 函数可以通过标签名称搜索作品。

**示例:**
```python
from lib import search_videos_by_tags

# 单标签搜索
works = search_videos_by_tags(["美少女"], start=0, end=20)

# 多标签组合搜索
works = search_videos_by_tags(["美少女", "水手服"], start=0, end=20)

# 获取第21-40个结果
works = search_videos_by_tags(["美少女"], start=20, end=40)
```

### 标签管理器

#### `TagManager` 类

用于管理标签信息，支持从加密数据库加载。

```python
from lib.tag_manager import TagManager

tag_manager = TagManager()

# 通过名称查找标签
tag_info = tag_manager.get_tag_by_name("淫亂真實")
print(f"标签ID: {tag_info['id']}")

# 通过ID查找标签
tag_info = tag_manager.get_tag_by_id("c1=23")
print(f"标签名称: {tag_info['name']}")

# 关键词搜索
tags = tag_manager.search_tags_by_keyword("美女")
for tag in tags:
    print(f"{tag['name']}: {tag['id']}")
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

### 清单信息

```python
{
    "list_id": "0W97k",           # 清单ID
    "list_name": "我的收藏",       # 清单名称
    "list_url": "https://javdb.com/users/list_detail?id=0W97k",
    "video_count": 50             # 视频数量
}
```

---

## 错误处理

### 常见错误

| 错误类型 | 说明 | 解决方案 |
|----------|------|----------|
| `ValueError: 未找到标签` | 标签名称不存在 | 检查标签名称拼写，或尝试简体/繁体 |
| `ConnectionError` | 网络连接失败 | 检查网络，或更换域名 |
| `LoginRequiredError` | 需要登录 | 调用 `login()` 完成登录 |

### 错误处理示例

```python
from lib import search_videos_by_tags

try:
    works = search_videos_by_tags(["不存在的标签"])
except ValueError as e:
    print(f"标签错误: {e}")

# 网络错误处理
from lib import search_actor_works
import time

for i in range(3):  # 重试3次
    try:
        works = search_actor_works("0R1n3", start=0, end=20)
        break
    except ConnectionError as e:
        print(f"连接失败，第{i+1}次重试...")
        time.sleep(2)
```

---

## 附录：AV 在线播放器（独立工具）

> ⚠️ **注意**：这不是 JAVDB API 的一部分，是一个独立的辅助工具，用于在线播放视频。

### 概述

AV 在线播放器是一个基于 Web 的独立工具，允许用户通过浏览器在线观看视频。

### 使用方法

```bash
python player/av_player_server.py
```

打开浏览器访问 `http://127.0.0.1:5000`

### 文件结构

```
javdb-api-scraper/
├── player/                # AV 在线播放器目录
│   ├── av_player_server.py    # 后端服务器
│   ├── index.html             # 前端页面
│   └── README.md              # 播放器说明文档
└── API_DOCUMENTATION.md   # 本文档
```

---

**免责声明**: 此工具仅用于技术学习和研究，开发者不对使用此工具产生的任何后果负责。请遵守相关法律法规。

## 许可证

MIT License
