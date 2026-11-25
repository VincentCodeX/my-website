---
name: blog-image-seo-publisher
description: 部落格文章自動化配圖、800x422 WebP 轉檔、SEO alt 標籤注入與雙位置同步發布工作流。適用於使用者提供桌面 Markdown 文章，需要配圖、轉換 800x422 WebP 格式、寫入繁體中文 SEO alt 屬性，並同步覆蓋至專案發布目錄與桌面備份。
---

# 部落格文章配圖、800x422 WebP 轉檔與 SEO 發布工作流 (Blog Image SEO Publisher)

本 Skill 定義了處理部落格 Markdown 文章配圖、SEO 最佳化、圖片尺寸轉檔與同步發布的標準作業流程 (SOP)。

---

## 核心執行流程 (Standard Operating Procedure)

當使用者要求處理桌面上（或指定位置）的部落格 Markdown 文章時，請嚴格按照以下 5 個步驟執行：

### 1. 讀取與分析文章 (Read & Analyze)
- **讀取標的**：檢視桌面上的 `/Users/vincent/Desktop/<filename>.md`。
- **解析內容**：
  - 提取 Front Matter（`title`, `description`, `heroImage`, `tags` 等）。
  - 分析文章段落結構，識別所有的圖片插入點（包含 `<div style="text-align:center;"><img .../></div>` 或 Markdown `![alt](url)` 結構）。
  - 確認需要處理的圖片數量（通常包含 1 張 `heroImage` 封面圖與若干張內頁插圖）。

---

### 2. 圖片生成與視覺風格規範 (Image Generation Guidelines)
使用 `generate_image` 工具生成所需圖片時，必須遵守以下設計標準：
- **極致寫實與現代感**：採用現代商業攝影、產品展示照、高畫質電競大片或遊戲臨場視覺風格。**嚴禁充滿明顯 AI 繪圖感的畫風**。
- **文字與符號限制**：**圖片中絕對不得出現任何亂碼文字、拼錯的英文字母或怪異符號**。提示詞中必須明確包含：`no text, textless, no typos`。
- **封面圖片 (Hero Image) 特別要求**：
  - 必須具備強烈的話題吸引力、視覺張力與議題衝突感（符合「吸睛帶有強烈腥膻色的本質不違規」）。
  - 使用強烈的燈光對比、流光霓虹、倒數計時、金錢/籌碼流逝或暗黑奢華氛圍，引發讀者強烈好奇心，但畫面內容必須健康安全、符合規律無違規暴露。
- **內頁插圖**：必須精確對應文章該大段落的主題與觀點，提供具說服力的實體產品、辦公室情境、遊戲場面或數據圖表視覺。

---

### 3. 圖片裁切、縮放與 WebP 轉換 (800x422 WebP Processing)
所有的圖片（包含封面與內頁圖）必須處理成統一的標準規格：
- **目標尺寸**：精確 **800 x 422 像素**（黃金 1.895:1 橫式比例）。
- **裁切邏輯**：以圖片中央為基準進行比例裁切，避免人物或核心主體變形。
- **轉檔格式**：轉換為 WebP 格式（品質 `quality=75`），將圖片總體積壓縮至最輕量（通常單張 10KB - 50KB）。
- **工具鏈**：使用系統內建 `sips`（中央裁切與縮放）搭配 `/opt/homebrew/bin/cwebp` 命令進行高效 WebP 轉換。
- **輸出目標路徑**：`/Users/vincent/Desktop/my-website/public/images/<image-slug>.webp`。

---

### 4. 內文閱讀性與 SEO 最佳化 (Readability & SEO Optimization)
- **深色版型閱讀性優化（避免字牆）**：
  - 網站採用深色毛玻璃版型（`BlogPostLayout.astro`），`<ul><li>` 預設字色偏暗且行距較窄，因此**嚴禁在圓點清單項目中塞入超過 2 句的長段落**；凡是長篇觀點或條列分析，一律改用 **`###` 獨立小標題（暖橘金色）搭配 2～3 句一段的短段落**。
  - 精簡同一句話內連續出現的多餘英文括號註解，保持行文流暢；在每小節核心金句加上 **粗體強調** 方便讀者掃讀；遇到多平台分數或數據比較時，可加入深色圓角 HTML 對照表。
  - **100% 保留作者原本的第一人稱語氣、個人體感與核心觀點**，不竄改原意。
- **繁體中文 Alt 屬性**：為每一張圖片撰寫富含繁體中文關鍵字、精確描述圖片內容與段落主旨的 `alt` 屬性（不得使用空白或預設檔名）。
- **HTML 圖片容器結構**：在 Markdown 中將圖片統一改寫為以下標準置中且響應式的 HTML 結構：
  ```html
  <div style="text-align:center;">
    <img
      src="/images/<image-slug>.webp"
      alt="[富含關鍵字的繁體中文描述]"
      style="
        width: 100%;
        max-width: 800px;
        height: auto;
        border-radius: 12px;
      "
    />
  </div>
  ```
- **Front Matter 修正**：確保 Front Matter 的 `heroImage` 屬性指向正確的封面圖片路徑（如 `heroImage: "/images/<hero-slug>.webp"`）。

---

### 5. 嚴格順序同步發布與日誌更新 (Strict Order Sync & Log)
> **⚠️ 關鍵防漏圖規則（必讀）**：專案設有監聽 `src/content/blog/` 的自動 Commit & Push 背景腳本！一旦 `.md` 寫入 `src/content/blog/` 就會在數秒內自動打包推送。因此**絕對不可將「複製圖片」與「寫入正式部落格 `.md`」放在同一個平行回合執行**！

請嚴格遵守以下**先後順序**分步執行：
1. **第一步（先放圖片）**：將所有轉檔完成的 `.webp` 圖片複製到 `/Users/vincent/Desktop/my-website/public/images/<image-slug>.webp`，並確認檔案皆已就位。
2. **第二步（更新桌面備份）**：更新 `/Users/vincent/Desktop/<filename>.md`。
3. **第三步（最後才寫入正式文章觸發自動發布）**：確認圖片都已在 `public/images/` 後，才將最終 `.md` 寫入 `/Users/vincent/Desktop/my-website/src/content/blog/<filename>.md`，讓自動發布腳本把圖片與文章一起打包推送。
4. **第四步（驗證 Git 狀態與更新日誌）**：檢查 `.git` 紀錄或 `git status`，確認圖片沒有遺留在未追蹤（`??`）狀態，並在 `/Users/vincent/.gemini/antigravity/brain/<conversation-id>/walkthrough.md` 尾端追加本次成果紀錄。

---

## 自動化工具腳本 (Helper Script)

Skill 提供預先撰寫好的 Python 自動化腳本：`scripts/blog_publisher.py`，支援全自動處理圖片裁切、WebP 壓縮、SEO alt 標籤寫入與檔案同步。

腳本使用範例：
```bash
python3 /Users/vincent/Desktop/my-website/.agents/skills/blog-image-seo-publisher/scripts/blog_publisher.py \
  --md "/Users/vincent/Desktop/<filename>.md" \
  --slug "<article-slug>"
```
