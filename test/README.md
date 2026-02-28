# 测试说明

本目录包含 JAVDB API 的验证测试脚本。

## 文件列表

| 文件 | 说明 |
|------|------|
| `verify_api.py` | 完整 API 验证测试（推荐） |
| `test_all_apis.py` | API 功能测试 |
| `test_tags_final.py` | 标签功能测试 |

## verify_api.py 详细说明

### 测试概览

| 序号 | 测试名称 | 函数 | 代码行 |
|------|----------|------|--------|
| 1 | 视频详情抓取 | `test_1_get_video_detail()` | L140-165 |
| 2 | 番号搜索 | `test_2_get_video_by_code()` | L168-190 |
| 3 | 演员搜索 | `test_3_search_actor()` | L193-226 |
| 4 | 演员作品（分页） | `test_4_get_actor_works_by_page()` | L229-266 |
| 5 | 演员作品全量（分页） | `test_5_get_actor_works_full_by_page()` | L269-308 |
| 6 | 标签搜索 | `test_6_search_by_tags()` | L311-342 |
| 7 | 标签搜索全量 | `test_7_search_by_tags_full()` | L345-378 |
| 8 | 标签管理 | `test_8_tag_manager()` | L381-418 |
| 9 | 图片下载 | `test_9_image_download()` | L421-458 |

### 测试详情

#### 测试1: get_video_detail - 视频详情抓取

**代码位置**: L140-165

**测试API**: `get_video_detail(video_id, download_images)`

**测试方法**:
```python
detail = get_video_detail("YwG8Ve", download_images=False)
```

**验证字段**:
- `video_id`: 视频 ID
- `code`: 番号 (MIDA-583)
- `title`: 标题
- `date`: 日期
- `actors`: 演员列表
- `tags`: 标签列表
- `magnets`: 磁力链接列表

**预期返回格式**:
```json
{
  "video_id": "YwG8Ve",
  "code": "MIDA-583",
  "title": "エッチ覚醒4本番...",
  "date": "2026-03-04",
  "actors": ["井上もも"],
  "tags": ["美少女電影", "單體作品", ...],
  "magnets": [{"magnet": "magnet:?", "size_text": "5.27GB"}]
}
```

---

#### 测试2: get_video_by_code - 番号搜索

**代码位置**: L168-190

**测试API**: `get_video_by_code(code)`

**测试方法**:
```python
detail = get_video_by_code("MIDA-583")
```

**验证逻辑**:
1. 搜索番号 "MIDA-583"
2. 返回第一个匹配结果的详情
3. 验证返回格式与 `get_video_detail` 相同

---

#### 测试3: search_actor - 演员搜索

**代码位置**: L193-226

**测试API**: `search_actor(actor_name)`

**测试方法**:
```python
actors = search_actor("井上もも")
```

**验证字段**:
- `actor_name`: 演员名称
- `actor_id`: 演员 ID (0R1n3)
- `actor_url`: 演员页面 URL

**预期返回格式**:
```json
[
  {
    "actor_name": "井上もも",
    "actor_id": "0R1n3",
    "actor_url": "https://javdb.com/actors/0R1n3"
  }
]
```

---

#### 测试4: get_actor_works_by_page - 演员作品（分页）

**代码位置**: L229-266

**测试API**: `get_actor_works_by_page(actor_id, page)`

**测试方法**:
```python
result = get_actor_works_by_page("0R1n3", page=1)
```

**验证字段**:
- `page`: 当前页码
- `has_next`: 是否有下一页
- `works`: 作品列表

**预期返回格式**:
```json
{
  "page": 1,
  "has_next": false,
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

---

#### 测试5: get_actor_works_full_by_page - 演员作品全量（分页）

**代码位置**: L269-308

**测试API**: `get_actor_works_full_by_page(actor_id, page, download_images)`

**测试方法**:
```python
result = get_actor_works_full_by_page("0R1n3", page=1, download_images=False)
```

**验证逻辑**:
1. 获取演员作品列表
2. 逐个获取作品详情
3. 验证每个作品包含完整信息（tags, actors, magnets 等）

---

#### 测试6: search_by_tags - 标签搜索

**代码位置**: L311-342

**测试API**: `search_by_tags(page, **tags)`

**测试方法**:
```python
result = search_by_tags(page=1, c3=78)  # 水手服
```

**验证字段**:
- `page`: 当前页码
- `has_next`: 是否有下一页
- `works`: 作品列表（基础信息）

**标签参数说明**:
- `c1`: 主題
- `c2`: 角色
- `c3`: 服裝 (78 = 水手服)
- `c4`: 體型 (17 = 巨乳)
- `c5`: 行爲 (18 = 中出)
- ...

---

#### 测试7: search_by_tags_full - 标签搜索全量

**代码位置**: L345-378

**测试API**: `search_by_tags_full(page, download_images, **tags)`

**测试方法**:
```python
result = search_by_tags_full(page=1, c3=78, download_images=False)
```

**验证逻辑**:
1. 按标签搜索作品
2. 逐个获取作品详情
3. 验证返回完整信息

---

#### 测试8: tag_manager - 标签管理

**代码位置**: L381-418

**测试API**:
- `get_tag_info(category, tag_id)` - L391-398
- `search_tag_by_name(name)` - L400-408
- `get_category_list()` - L410-418

**测试方法**:
```python
# 查询标签
tag = get_tag_info("c3", 78)  # 返回: 水手服

# 搜索标签
results = search_tag_by_name("巨乳")

# 获取分类
categories = get_category_list()
```

---

#### 测试9: image_download - 图片下载

**代码位置**: L421-458

**测试方法**:
```python
# 获取视频详情（包含缩略图链接）
detail = get_video_detail("YwG8Ve", download_images=True)

# 手动下载测试
from utils import ImageDownloader
downloader = ImageDownloader(session)
downloaded = downloader.download_thumbnails(code, image_urls)
```

**验证逻辑**:
1. 获取缩略图链接列表
2. 调用下载器下载图片
3. 验证图片保存到正确目录

**输出目录**: `test/output/images/{code}/`

---

## 运行测试

```bash
# 进入项目目录
cd d:\code\javdb\javdb-api-scraper

# 运行验证测试
python test/verify_api.py
```

## 测试输出

测试结果保存在 `test/output/json/test_results.json`:

```json
{
  "total": 12,
  "passed": 12,
  "failed": 0,
  "timestamp": "2026-03-01 03:17:07",
  "tests": [
    {
      "test": "get_video_detail",
      "passed": true,
      "message": "成功获取: MIDA-583..."
    }
  ]
}
```

## 测试数据

测试使用的固定数据（L55-62）:

```python
TEST_DATA = {
    "video_id": "YwG8Ve",      # 测试视频 ID
    "code": "MIDA-583",        # 测试番号
    "actor_name": "井上もも",   # 测试演员
    "actor_id": "0R1n3",       # 演员 ID
    "tag_c3": 78,              # 标签 ID (水手服)
    "tag_name": "水手服",       # 标签名称
}
```

## 验证函数

### validate_video_detail()

**代码位置**: L106-135

**功能**: 验证视频详情返回格式是否正确

**检查字段**:
- `video_id`, `code`, `title`, `date`, `actors`, `tags`, `magnets`
- 验证 `actors`, `tags`, `magnets` 是否为列表类型

### log_test()

**代码位置**: L88-103

**功能**: 记录并输出测试结果
