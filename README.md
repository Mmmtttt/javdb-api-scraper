# JAVDB API Scraper

JAVDB 爬虫 API，支持无浏览器爬取、Cloudflare 绕过、标签搜索、演员作品抓取等功能。

## 功能特性

- **无浏览器爬取**：使用 curl_cffi 绕过 Cloudflare，无需打开浏览器
- **自动登录**：支持账号密码登录，自动保存 cookies
- **视频详情抓取**：番号、标题、标签、演员、磁力链接、缩略图等
- **演员作品抓取**：支持分页、全量信息抓取
- **标签搜索**：支持多类标签组合搜索（如 c1=23&c3=78）
- **标签数据库**：342 个标签，10 个分类
- **图片下载**：自动下载高清缩略图

## 目录结构

```
javdb-api-scraper/
├── config.py              # 配置文件（含账号信息）
├── javdb_api.py           # 核心 API 模块
├── tag_manager.py         # 标签管理模块
├── login.py               # 自动登录模块
├── utils.py               # 工具函数
├── parse_tags_html.py     # 标签数据库解析脚本
├── test_all_apis.py       # API 测试脚本
├── test_tags_final.py     # 标签功能测试
├── requirements.txt       # 依赖列表
├── cookies.json           # 登录 cookies
└── output/
    ├── tags_database.json # 标签数据库
    ├── json/              # JSON 数据输出
    ├── images/            # 缩略图下载
    └── magnets/           # 磁力链接导出
```

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制配置文件模板：
```bash
cp config.example.py config.py
```

2. 编辑 `config.py` 填入你的账号信息：
```python
LOGIN = {
    'username': 'your_username',
    'password': 'your_password',
}
```

## API 接口

### 视频相关

```python
from javdb_api import get_video_detail, get_video_by_code

# 抓取作品页全量信息
detail = get_video_detail("YwG8Ve", download_images=True)
print(detail['code'])      # MIDA-583
print(detail['tags'])      # ['美少女電影', '單體作品', ...]
print(detail['actors'])    # ['井上もも']

# 根据番号搜索并获取详情
detail = get_video_by_code("MIDA-583")
```

### 演员相关

```python
from javdb_api import search_actor, get_actor_works_by_page, get_actor_works_full_by_page

# 搜索演员
actors = search_actor("井上もも")
print(actors[0]['actor_id'])  # 0R1n3

# 获取演员作品（分页，基础信息）
result = get_actor_works_by_page("0R1n3", page=1)
print(result['has_next'])     # 是否有下一页
print(len(result['works']))   # 作品数量

# 获取演员作品全量信息（分页）
result = get_actor_works_full_by_page("0R1n3", page=1, download_images=True)
```

### 标签搜索

```python
from javdb_api import search_by_tags, search_by_tags_full

# 多类标签组合搜索（基础信息）
result = search_by_tags(page=1, c3=78)           # 水手服
result = search_by_tags(page=1, c4=17, c5=18)    # 巨乳 + 中出

# 多类标签组合搜索（全量信息）
result = search_by_tags_full(page=1, c3=78, download_images=True)
```

### 标签管理

```python
from tag_manager import get_tag_info, search_tag_by_name, get_category_list

# 查询标签信息
tag = get_tag_info("c3", 78)  # 水手服
print(tag['name'])  # 水手服

# 根据名称搜索标签
results = search_tag_by_name("巨乳")
# 结果: c4 (體型): 17 = 巨乳

# 获取所有分类
categories = get_category_list()
```

## 标签分类

| 分类 | 名称 | 标签数 |
|------|------|--------|
| c1 | 主題 | 60 |
| c2 | 角色 | 53 |
| c3 | 服裝 | 39 |
| c4 | 體型 | 20 |
| c5 | 行爲 | 40 |
| c6 | 玩法 | 37 |
| c7 | 類別 | 58 |
| c9 | 時長 | 2 |
| c10 | 基本 | 7 |
| c11 | 年份 | 26 |

## 输出格式

### 视频详情

```json
{
  "video_id": "YwG8Ve",
  "code": "MIDA-583",
  "title": "エッチ覚醒4本番...",
  "date": "2026-03-04",
  "actors": ["井上もも"],
  "tags": ["美少女電影", "單體作品", "情侶", "口交", "顏射", "主觀視角"],
  "series": "系列名称",
  "rating": "4.57分",
  "thumbnail_images": ["https://..."],
  "preview_video": "https://...",
  "magnets": [
    {"name": "MIDA-583", "size": "5.2GB", "link": "magnet:?xt=..."}
  ]
}
```

### 演员作品

```json
{
  "page": 1,
  "has_next": true,
  "works": [
    {
      "video_id": "YwG8Ve",
      "code": "MIDA-583",
      "title": "作品标题",
      "date": "2026-03-04",
      "rating": "4.57分"
    }
  ]
}
```

## 更新标签数据库

1. 登录 JAVDB 后访问 `https://javdb.com/tags`
2. 保存网页为 HTML 文件
3. 运行解析脚本：

```bash
python parse_tags_html.py
```

## 测试

```bash
# 测试所有 API
python test_all_apis.py

# 测试标签功能
python test_tags_final.py
```

## 注意事项

- 请合理使用，避免频繁请求
- 标签页面需要登录后才能访问完整内容
- 图片下载会自动使用高清版本（_l_ 替换 _s_）
