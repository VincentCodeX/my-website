-----
title: “聊個天就自動發文？我用 Claude + Automator + GitHub 打造零摩擦部落格流程”
description: “從聊天到文章上線，只需要丟一個檔案。這篇分享我怎麼把 Claude 專案、Automator、GitHub、Cloudflare 全部串起來，讓發文變成世界上最簡單的事。”
pubDate: “2026-05-21”
tags: [“自動化”, “Claude AI”, “部落格”, “GitHub”, “Automator”]
-----
> 🎯 **這篇文章想分享給：**
> 想經營部落格、但每次發文都覺得流程超麻煩的創作者

<hr />

## 🪐 1. 探索的起點 (背景動機)

我一直想讓部落格更新這件事變得「沒有摩擦」。

傳統的更新方式太痛了——要登入後台、手動排版、設定各種欄位，光是這些前置作業就夠讓人懶得發文了。身為一個同時在跑 YouTube 頻道的人，我沒有多餘的心力花在這些事情上。

所以我開始研究：**有沒有辦法讓「想到什麼就發什麼」這件事，真的只要幾個動作就完成？**

今天終於把整個流程跑通了，而且比我預期的還要簡單。

<hr />

## 🛠️ 2. 核心實測與工具拆解

整個流程只有三個步驟：

1. **在 Claude 專案裡聊天** → 跟 AI 討論今天想寫的主題，聊完直接拿到格式完整的 `.md` 檔案
1. **把檔案丟進指定資料夾** → 就這樣，真的就這樣
1. **Automator 自動偵測異動 → 同步上線** → GitHub 更新、Cloudflare 自動 deploy，文章就上網了

- **🎯 關鍵重點 A：Claude 專案設定是核心**
  在 Claude 專案裡預先設定好文章的格式規則與語氣，之後每次聊完只要說「幫我整理成文章」，AI 就會直接輸出符合格式的 `.md` 檔，完全不需要手動調整排版。
- **🎯 關鍵重點 B：Automator Folder Action 是魔法**
  用 macOS 內建的 Automator，設定「資料夾動作（Folder Action）」監控指定資料夾。只要偵測到新檔案出現，就自動觸發後續的 Git 指令，把檔案推上 GitHub。金鑰透過 macOS Keychain 管理，安全又不用每次手動輸入。
- **🎯 關鍵重點 C：GitHub + Cloudflare 負責最後一哩路**
  Repo 一有更新，Cloudflare 就自動重新 build 並 deploy 靜態網站。整個過程大概不到一分鐘，完全在背景跑，我什麼都不用管。

<hr />

## 💡 3. 🚀 探索者私房大補帖

> 💡 **重要發現與踩坑筆記：**
> 原本打算用終端機腳本來做自動化，但因為 iCloud 資料夾的關係（路徑行為比較特別），後來改用 Automator 的 Folder Action 反而更穩、更直覺。如果你也想複製這個流程，建議直接從 Automator 下手，不用繞終端機那條路。

### 💻 實用指令 / 程式碼備忘

```bash
# Automator Folder Action 內呼叫的 shell script 核心邏輯
cd /path/to/your/blog/repo
git add .
git commit -m "auto: new post $(date '+%Y-%m-%d %H:%M')"
git push origin main
```

<hr />

## 🌟 4. 總結與下一步

以前更新部落格要經歷登入後台、手動排版、設定欄位一整套流程，現在只剩「聊天 → 丟檔案」兩個動作，GitHub、Cloudflare、Automator 全部隱形在背後跑。**這套流程的價值不在技術有多複雜，而在於它讓發文這件事的心理門檻幾乎降到零。**

下一步可以試試看：把 Claude 專案進一步優化，讓 AI 連圖片描述、SEO meta 都一起生成，讓整個流程再少一個環節。

> 🔗 **相關資源：**
> 
> - [Automator 官方說明](https://support.apple.com/guide/automator/welcome/mac)
> - [Cloudflare Pages 文件](https://developers.cloudflare.com/pages/)
> - [GitHub Actions 自動化參考](https://docs.github.com/en/actions)

<hr />

*如果這篇對你有幫助，歡迎訂閱 [Vincent 的 YouTube 頻道](https://www.youtube.com/@VincentGame) 👾*