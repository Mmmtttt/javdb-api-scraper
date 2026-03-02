# JAVDB API 测试系统使用说明

## 概述

测试系统提供了完整的测试框架，支持配置化测试、结果保存和详细日志。

## 文件结构

```
test/
├── README.md              # 本文档
├── verify_api.py          # 原始验证测试（保留）
├── output/               # 测试结果输出目录
│   ├── test_results_*.json  # JSON 格式结果
│   └── test_results_*.txt   # 文本格式结果
test_config.py          # 测试配置文件
test_runner.py          # 测试运行器
```

## 快速开始

### 1. 配置测试

编辑 `test_config.py` 文件，配置你要运行的测试：

```python
# 视频详情测试
VIDEO_DETAIL_TESTS = [
    {
        "name": "测试视频详情 - 永野一夏作品",
        "video_id": "YwG8Ve",
        "download_images": False,
        "enabled": True,  # 启用此测试
    },
]

# 标签筛选测试
TAG_FILTER_TESTS = [
    {
        "name": "测试标签筛选 - 永野一夏的'美少女'标签作品",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "tag_names": ["美少女"],
        "max_pages": 1,
        "get_details": True,
        "download_images": False,
        "save_temp": True,
        "enabled": True,
    },
]
```

### 2. 运行测试

```bash
# 运行所有启用的测试
python test_runner.py

# 列出所有测试项
python test_runner.py --list

# 只运行视频相关测试
python test_runner.py --video

# 只运行演员相关测试
python test_runner.py --actor

# 只运行标签相关测试
python test_runner.py --tag

# 只运行磁力链接测试
python test_runner.py --magnet

# 只运行图片下载测试
python test_runner.py --image
```

### 3. 查看结果

测试结果会保存在 `test/output/` 目录：

- `test_results_YYYYMMDD_HHMMSS.json` - JSON 格式结果
- `test_results_YYYYMMDD_HHMMSS.txt` - 文本格式结果

## 配置说明

### 测试配置

所有测试配置都在 `test_config.py` 中：

| 配置项 | 说明 |
|--------|------|
| `VIDEO_DETAIL_TESTS` | 视频详情测试 |
| `CODE_SEARCH_TESTS` | 番号搜索测试 |
| `VIDEO_SEARCH_TESTS` | 视频搜索测试 |
| `ACTOR_SEARCH_TESTS` | 演员搜索测试 |
| `ACTOR_WORKS_TESTS` | 演员作品测试 |
| `TAG_FILTER_TESTS` | 标签筛选测试 |
| `TAG_SEARCH_TESTS` | 标签搜索测试 |
| `MAGNET_TESTS` | 磁力链接测试 |
| `IMAGE_DOWNLOAD_TESTS` | 图片下载测试 |

每个测试项包含以下字段：

- `name`: 测试名称
- `enabled`: 是否启用此测试
- 其他特定参数（如 `video_id`, `actor_id`, `tag_names` 等）

### 结果保存配置

```python
RESULT_CONFIG = {
    "save_results": True,  # 是否保存测试结果
    "output_dir": "test/output",  # 结果输出目录
    "save_json": True,  # 是否保存 JSON 格式结果
    "save_text": True,  # 是否保存文本格式结果
    "include_timestamp": True,  # 文件名是否包含时间戳
    "verbose": True,  # 是否输出详细信息
}
```

### 其他配置

```python
# 超时设置
TIMEOUT_CONFIG = {
    "request_timeout": 30,  # 单个请求超时时间（秒）
    "test_timeout": 300,  # 整个测试超时时间（秒）
}

# 重试配置
RETRY_CONFIG = {
    "max_retries": 3,  # 最大重试次数
    "retry_delay": 2,  # 重试延迟（秒）
}

# 日志配置
LOG_CONFIG = {
    "log_level": "INFO",  # 日志级别: DEBUG, INFO, WARNING, ERROR
    "log_to_file": True,  # 是否记录到文件
    "log_file": "test/test.log",  # 日志文件路径
}
```

## 测试类型说明

### 1. 视频详情测试

测试获取视频详情信息：

```python
VIDEO_DETAIL_TESTS = [
    {
        "name": "测试视频详情",
        "video_id": "YwG8Ve",
        "download_images": False,
        "enabled": True,
    },
]
```

### 2. 番号搜索测试

测试根据番号搜索视频：

```python
CODE_SEARCH_TESTS = [
    {
        "name": "测试番号搜索",
        "code": "MIDA-583",
        "enabled": True,
    },
]
```

### 3. 视频搜索测试

测试关键词搜索视频：

```python
VIDEO_SEARCH_TESTS = [
    {
        "name": "测试视频搜索",
        "keyword": "SSIS",
        "max_pages": 1,
        "enabled": True,
    },
]
```

### 4. 演员搜索测试

测试搜索演员：

```python
ACTOR_SEARCH_TESTS = [
    {
        "name": "测试演员搜索",
        "actor_name": "井上もも",
        "enabled": True,
    },
]
```

### 5. 演员作品测试

测试获取演员作品：

```python
ACTOR_WORKS_TESTS = [
    {
        "name": "测试演员作品",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "max_pages": 1,
        "get_details": False,
        "download_images": False,
        "enabled": True,
    },
]
```

### 6. 标签筛选测试

测试按标签筛选演员作品：

```python
TAG_FILTER_TESTS = [
    {
        "name": "测试标签筛选",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "tag_names": ["美少女"],
        "max_pages": 1,
        "get_details": True,
        "download_images": False,
        "save_temp": True,
        "enabled": True,
    },
]
```

### 7. 标签搜索测试

测试搜索标签作品：

```python
TAG_SEARCH_TESTS = [
    {
        "name": "测试标签搜索",
        "tag_id": "c1=23",
        "max_pages": 1,
        "enabled": True,
    },
]
```

### 8. 磁力链接测试

测试获取磁力链接：

```python
MAGNET_TESTS = [
    {
        "name": "测试磁力链接",
        "video_id": "YwG8Ve",
        "enabled": True,
    },
]
```

### 9. 图片下载测试

测试下载视频图片：

```python
IMAGE_DOWNLOAD_TESTS = [
    {
        "name": "测试图片下载",
        "video_id": "YwG8Ve",
        "download_dir": None,  # None 表示使用默认目录
        "enabled": True,
    },
]
```

## 结果格式

### JSON 格式

```json
{
  "timestamp": "2026-03-02T10:30:00",
  "total_tests": 5,
  "passed_tests": 4,
  "failed_tests": 1,
  "results": [
    {
      "test_name": "测试视频详情",
      "test_type": "video_detail",
      "success": true,
      "error": null,
      "duration": 1.23,
      "message": "测试成功",
      "data": {
        "video_id": "YwG8Ve",
        "code": "MIDA-583",
        "title": "作品标题...",
        "date": "2026-03-04",
        "tags_count": 8,
        "magnets_count": 2
      },
      "start_time": "2026-03-02T10:30:00",
      "end_time": "2026-03-02T10:30:01"
    }
  ]
}
```

### 文本格式

```
======================================================================
JAVDB API 测试结果
======================================================================

时间: 2026-03-02 10:30:00
总测试数: 5
通过: 4
失败: 1

----------------------------------------------------------------------
测试: 测试视频详情
类型: video_detail
状态: ✅ 通过
耗时: 1.23秒
数据: {"video_id": "YwG8Ve", "code": "MIDA-583", ...}
```

## 自动化登录

### 使用方式 1: 直接粘贴 Session 值（推荐）

1. 运行 `python test_runner.py`
2. 如果需要登录，浏览器会自动打开登录助手页面
3. 在浏览器中登录 JAVDB
4. 按 F12 打开开发者工具，找到 `_jdb_session` 的值
5. 复制并粘贴到助手的"Session 值"标签页
6. 点击"提交 Session"

### 使用方式 2: 完整 Cookies

1. 在浏览器开发者工具中，复制所有 cookies
2. 粘贴到助手的"完整 Cookies"标签页
3. 点击"提交 Cookies"

### 使用方式 3: 上传截图

1. 截图登录成功的页面
2. 在助手的"上传截图"标签页，选择图片
3. 点击"提交截图"
4. 图片会保存到 `output/screenshots/` 目录

## 常见问题

### Q: 如何只运行某个测试？

A: 在 `test_config.py` 中，将对应测试的 `enabled` 字段设置为 `True`，其他设置为 `False`。

### Q: 测试结果保存在哪里？

A: 默认保存在 `test/output/` 目录，可以在 `RESULT_CONFIG` 中修改。

### Q: 如何增加新的测试？

A: 在 `test_config.py` 中添加新的测试项，然后在 `test_runner.py` 中添加对应的测试函数。

### Q: 测试失败怎么办？

A: 检查：
1. 网络连接是否正常
2. cookies 是否有效（如果需要登录）
3. 测试参数是否正确（如 video_id, actor_id 等）
4. 查看 `test/test.log` 日志文件

## 示例

### 示例 1: 测试单个演员的标签筛选

```python
# test_config.py
TAG_FILTER_TESTS = [
    {
        "name": "测试永野一夏的美少女作品",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "tag_names": ["美少女"],
        "max_pages": 1,
        "get_details": True,
        "download_images": False,
        "save_temp": True,
        "enabled": True,
    },
]

# 其他测试都禁用
VIDEO_DETAIL_TESTS = []
CODE_SEARCH_TESTS = []
# ...
```

运行：
```bash
python test_runner.py --tag
```

### 示例 2: 批量测试多个演员

```python
# test_config.py
ACTOR_WORKS_TESTS = [
    {
        "name": "测试演员1",
        "actor_id": "0R1n3",
        "actor_name": "井上もも",
        "max_pages": 1,
        "enabled": True,
    },
    {
        "name": "测试演员2",
        "actor_id": "NeOr",
        "actor_name": "永野一夏",
        "max_pages": 1,
        "enabled": True,
    },
]
```

运行：
```bash
python test_runner.py --actor
```
