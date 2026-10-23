# Lithium（Android EPUB 閱讀器）繁中本地化用語表

目標：**臺灣正體中文**，介面自然、不像機器翻。App 套件名 `com.faultexception.reader`，
是開源書本閱讀器（GPLv3）。翻的是它自己的介面字串。

## 硬性規則（一條都不能違反）

1. **只用繁體字**，不得出現簡體字（例：單→檔、設→設、書→書、庫→庫、選→選、開→開、關→關、進→進、變→變、應→應、图→圖、页→頁、关→關、内→內、里→裡）。
2. **佔位符與跳脫原樣保留**，順序與數量不變：`%s` `%1$s` `%2$s` `%d` `%1$d` `%s` `%%`、`\n`（換行）、`\'`（跳脫單引號）、`\"`。
   - 例：`Delete %1$s?` → `確定要刪除 %1$s？`（`%1$s` 一個字都不能動）。
3. **技術字串不翻，直接照抄原文**：Java 類別名（`com.google.android.material...`）、
   資源參考（`@android:string/cancel`）、SVG 路徑（`M12,4.5C7,4.5...`）、純格式（`%1$d/%2$d`、`:`）、
   URL、純符號、單字英文代號。整條都是這種東西時，譯文＝原文。
4. **專有名詞保留原文**：`Lithium`、`Lithium Pro`、`EPUB`、`PDF`、`ZIP`、`HTML`、`CSS`、
   `Google Drive`、`Dropbox`、`OneDrive`、`WebDAV`、`SFTP`、`FTP`、`OPDS`、`Calibre`、`Adobe`、`Android`。
5. 標點用全形：`，。：；？！（）「」、`；省略號用 `…`；引號用「」；不用英文句號結尾的動詞片語（選單項不加句號）。
6. 人稱：**不要「您」**，能省略主詞就省略。避免翻譯腔（「被」「使得」「進行」能不用就不用）。
7. 長度收斂：按鈕／選單項 ≤ 8 字；標題 ≤ 14 字；說明與提示句可完整成句。
8. 一句一行，**輸出不得含換行**（原文若含 `\n`，譯文在同樣位置放 `\n`）。
9. 原文若被雙引號包起來（Android 用來保留首尾空格，例：`"No app is installed... %1$s"`），
   譯文也要用一組雙引號把整句包起來：`"沒有安裝能開啟這類連結的應用程式。 %1$s"`。
10. 語氣：`Are you sure?` 類一律用「確定要…嗎？」；`Cancel` → `取消`；`OK` → `確定`。

## 詞彙表（一律照此，保持全檔一致）

| 英文 | 繁中 | 備註 |
|---|---|---|
| book / books | 書 / 書 | 集合概念也用「書」，不要用「書籍」 |
| library | 書庫 | |
| category | 分類 | |
| bookmark | 書籤 | |
| highlight | 螢光標記 | 動詞「加螢光標記」 |
| note / annotation | 筆記 / 註解 | |
| chapter | 章節 | |
| table of contents | 目錄 | |
| page | 頁 | |
| position / reading position | 位置 / 閱讀位置 | |
| progress | 閱讀進度 | |
| cover | 封面 | |
| author / title | 作者 / 書名 | |
| font | 字型；font size 字級 | 不要用「字體」指 size |
| line spacing / paragraph spacing | 行距 / 段落間距 | |
| text alignment | 對齊 | |
| hyphenation | 斷字 | |
| bold / italic | 粗體 / 斜體 | |
| theme | 主題；night theme 夜間主題 | |
| brightness | 亮度 | |
| keep screen awake | 保持螢幕喚醒 | |
| margin / padding | 頁邊 / 內距 | |
| columns | 欄數 | |
| color | 顏色；dark/light 深色/淺色；sepia 米色；accent 強調色 | |
| swipe / tap / double tap / long press | 滑動 / 輕觸 / 輕點兩下 / 長按 | |
| volume keys | 音量鍵 | |
| gesture | 手勢 | |
| left / right / top / bottom / edge | 左側 / 右側 / 上方 / 下方 / 邊緣 | |
| fullscreen / status bar / navigation bar | 全螢幕 / 狀態列 / 導覽列 | |
| scroll / continuous scroll | 捲動 / 連續捲動 | |
| portrait / landscape | 直向 / 橫向 | |
| settings / preferences | 設定 / 偏好設定 | |
| appearance / reading / behaviour | 外觀 / 閱讀 / 行為 | |
| storage | 儲存空間 | |
| folder / file | 資料夾 / 檔案 | 不要用「文件」「目錄」指 folder |
| permission | 權限 | |
| notification | 通知 | |
| import / export | 匯入 / 匯出 | |
| backup / restore | 備份 / 還原 | |
| sync | 同步 | |
| delete / rename / share | 刪除 / 重新命名 / 分享 | |
| open / close | 開啟 / 關閉 | |
| save / apply / done | 儲存 / 套用 / 完成 | |
| retry / error / warning | 重試 / 錯誤 / 警告 | |
| search / sort / filter | 搜尋 / 排序 / 篩選 | |
| recent | 最近閱讀 | |
| all / none / other | 全部 / 無 / 其他 | |
| custom / default / advanced | 自訂 / 預設 / 進階 | |
| about / version / license | 關於 / 版本 / 授權條款 | |
| help / tip | 說明 / 提示 | |
| dictionary | 字典 | |
| link / external link | 連結 / 外部連結 | |
| image / zoom | 圖片 / 縮放 | |
| unlock / purchase / trial | 解鎖 / 購買 / 試用 | |
| donate / pro | 贊助 / Pro（不譯） | |
| add / remove / edit | 新增 / 移除 / 編輯 | |
| yes / no / ok / cancel | 是 / 否 / 確定 / 取消 | |
| Off / On / Reversed | 關閉 / 開啟 / 反向 | 開關類選項 |
| Select a Color | 選取顏色 | |
| Transparency | 透明度 | |
| Presets | 預設顏色 | |
| Range start / Range end | 範圍起點 / 範圍終點 | |

## 範例

| 原文 | 正確譯文 |
|---|---|
| `Add bookmark` | `新增書籤` |
| `Delete %1$s?` | `確定要刪除 %1$s？` |
| `No books yet` | `還沒有任何書` |
| `Reading position saved` | `已儲存閱讀位置` |
| `Keep screen awake` | `保持螢幕喚醒` |
| `%1$d books were added to your library.` | `已將 %1$d 本書加入書庫。` |
| `com.google.android.material.appbar.AppBarLayout$ScrollingViewBehavior` | 照抄原文 |
| `Custom` | `自訂` |
| `Line 1\nLine 2` | `第 1 行\n第 2 行`（`\n` 原樣保留） |
