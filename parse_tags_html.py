"""
从 HTML 文件解析标签数据库
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


def parse_tags_from_html(html_file: str, output_file: str = None):
    """
    从 HTML 文件解析标签数据
    
    Args:
        html_file: HTML 文件路径
        output_file: 输出 JSON 文件路径
        
    Returns:
        标签数据库字典
    """
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    # 标签数据库
    tags_db = {
        "categories": {},
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": html_file
    }
    
    # 查找所有标签分类
    # 结构: <dt class="tag-category" id="tag-category-N" data-cid="N">
    category_elements = soup.select('dt.tag-category')
    
    for cat_elem in category_elements:
        # 获取分类 ID
        cat_id = cat_elem.get('data-cid')
        if not cat_id:
            continue
        
        # 获取分类名称 (在 <strong> 标签中)
        strong_elem = cat_elem.select_one('strong')
        if not strong_elem:
            continue
        cat_name = strong_elem.get_text(strip=True)
        
        # 获取该分类下的所有标签
        tags = []
        
        # 查找所有标签链接
        # 结构: <a class="tag is-outlined" href="https://javdb.com/tags?cN=XXX">标签名</a>
        tag_links = cat_elem.select('a.tag.is-outlined')
        
        for link in tag_links:
            href = link.get('href', '')
            tag_name = link.get_text(strip=True)
            
            # 跳过"全部"链接
            if tag_name == '全部' or href.endswith('/tags'):
                continue
            
            # 从 href 中提取标签 ID
            # 格式: https://javdb.com/tags?cN=XXX
            match = re.search(rf'c{cat_id}=(\d+)', href)
            if match:
                tag_id = int(match.group(1))
                tags.append({
                    "id": tag_id,
                    "name": tag_name,
                    "value": str(tag_id)
                })
        
        # 按标签 ID 排序
        tags.sort(key=lambda x: x["id"])
        
        # 存储分类
        cat_key = f"c{cat_id}"
        tags_db["categories"][cat_key] = {
            "name": cat_name,
            "tags": tags
        }
    
    # 保存到文件
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tags_db, f, indent=2, ensure_ascii=False)
        print(f"✅ 已保存到: {output_file}")
    
    return tags_db


def print_tags_summary(tags_db: dict):
    """打印标签数据库摘要"""
    print("=" * 70)
    print("JAVDB 标签分类数据库")
    print("=" * 70)
    print(f"更新时间: {tags_db.get('updated_at', '未知')}")
    print(f"来源: {tags_db.get('source', '未知')}")
    print()
    
    total_tags = 0
    for cat_key, cat_data in sorted(tags_db.get("categories", {}).items()):
        tag_count = len(cat_data.get("tags", []))
        total_tags += tag_count
        print(f"【{cat_key}】{cat_data.get('name', '')} ({tag_count}个标签)")
        
        # 显示前5个标签
        for tag in cat_data.get("tags", [])[:5]:
            print(f"   - {tag['id']}: {tag['name']}")
        
        if tag_count > 5:
            print(f"   ... 还有 {tag_count - 5} 个标签")
        print()
    
    print(f"总计: {len(tags_db.get('categories', {}))} 个分类, {total_tags} 个标签")


if __name__ == '__main__':
    # HTML 文件路径
    html_file = r"d:\code\javdb\有碼分類篩選 _ JavDB 成人影片數據庫.html"
    
    # 输出文件路径
    output_file = r"d:\code\javdb\javdb-api-scraper\output\tags_database.json"
    
    print("=" * 70)
    print("解析 JAVDB 标签页面")
    print("=" * 70)
    
    # 解析标签
    tags_db = parse_tags_from_html(html_file, output_file)
    
    # 打印摘要
    print_tags_summary(tags_db)
    
    # 测试查询
    print("\n" + "=" * 70)
    print("测试查询")
    print("=" * 70)
    
    # 查询水手服
    for cat_key, cat_data in tags_db.get("categories", {}).items():
        for tag in cat_data.get("tags", []):
            if "水手服" in tag["name"]:
                print(f"✅ 找到 '水手服': {cat_key}={tag['id']} ({cat_data['name']})")
    
    # 查询中出
    for cat_key, cat_data in tags_db.get("categories", {}).items():
        for tag in cat_data.get("tags", []):
            if "中出" in tag["name"]:
                print(f"✅ 找到 '中出': {cat_key}={tag['id']} ({cat_data['name']})")
