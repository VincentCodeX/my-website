#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Blog Image SEO Publisher Helper Script
通用部落格文章圖片裁切 (800x422)、WebP 轉檔、SEO Alt 注入與雙位置同步腳本
"""

import os
import shutil
import re
import argparse
import subprocess

def get_image_size(path):
    out = subprocess.check_output(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path]).decode('utf-8')
    width_match = re.search(r'pixelWidth:\s*(\d+)', out)
    height_match = re.search(r'pixelHeight:\s*(\d+)', out)
    width = int(width_match.group(1))
    height = int(height_match.group(1))
    return width, height

def crop_and_resize_to_800_422(src_path, dest_webp_path):
    """使用 sips 與 cwebp 將圖片中央裁切並縮放到精確的 800 x 422 像素，並轉檔為 WebP"""
    width, height = get_image_size(src_path)
    target_ratio = 800.0 / 422.0
    current_ratio = float(width) / float(height)
    
    if current_ratio > target_ratio:
        crop_width = int(height * target_ratio)
        crop_height = height
    else:
        crop_width = width
        crop_height = int(width / target_ratio)
        
    temp_png = dest_webp_path + ".tmp.png"
    shutil.copy(src_path, temp_png)
    
    # 1. 從中央裁切
    subprocess.check_call(["sips", "-c", str(crop_height), str(crop_width), temp_png])
    # 2. 縮放到 800 x 422
    subprocess.check_call(["sips", "-z", "422", "800", temp_png])
    # 3. 使用 cwebp 轉為 WebP (quality=75)
    subprocess.check_call(["/opt/homebrew/bin/cwebp", "-q", "75", temp_png, "-o", dest_webp_path])
    
    if os.path.exists(temp_png):
        os.remove(temp_png)
        
    size_kb = os.path.getsize(dest_webp_path) / 1024
    print(f"轉檔完成：{dest_webp_path} ({size_kb:.2f} KB)")
    return True

def update_markdown_seo(md_path, dest_md_path, seo_alts_dict=None):
    """更新 Markdown 中的 HTML 圖片標籤，注入 SEO alt 屬性並將寬度控制為 max-width: 800px"""
    print(f"正在更新 Markdown SEO 格式：{md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    seo_alts = seo_alts_dict or {}
    
    def replacer(match):
        img_block = match.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', img_block)
        if src_match:
            src = src_match.group(1)
            filename = os.path.basename(src)
            alt_text = seo_alts.get(filename, "部落格文章主題配圖與視覺展示")
            
            new_block = f"""<div style="text-align:center;">
  <img
    src="{src}"
    alt="{alt_text}"
    style="
      width: 100%;
      max-width: 800px;
      height: auto;
      border-radius: 12px;
    "
  />
</div>"""
            return new_block
        return img_block
        
    pattern = re.compile(r'<div style="text-align:center;">\s*<img\s+src="[^"]+"\s+style="[^"]+"\s*/>\s*</div>', re.DOTALL)
    updated_content = pattern.sub(replacer, content)
    
    with open(dest_md_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"已成功更新 Markdown：{dest_md_path}")

def sync_post(desktop_md_path, project_dir="/Users/vincent/Desktop/my-website"):
    filename = os.path.basename(desktop_md_path)
    target_blog_md = os.path.join(project_dir, "src/content/blog", filename)
    shutil.copy(desktop_md_path, target_blog_md)
    print(f"已同步文章到專案正式目錄：{target_blog_md}")

def main():
    parser = argparse.ArgumentParser(description="Blog Image SEO Publisher Tool")
    parser.add_argument("--md", required=True, help="Markdown 檔案路徑")
    parser.add_argument("--src-dir", help="原始圖檔目錄")
    parser.add_argument("--project-dir", default="/Users/vincent/Desktop/my-website", help="網頁專案根目錄")
    
    args = parser.parse_args()
    if os.path.exists(args.md):
        update_markdown_seo(args.md, args.md)
        sync_post(args.md, args.project_dir)

if __name__ == "__main__":
    main()
