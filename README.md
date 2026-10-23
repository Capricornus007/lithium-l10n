# Lithium 繁中／簡中補齊 — 交付說明（2026-10-23，第 3 版）

> 第 3 版＝上游 `0.25.1(106)` 更新 + `pgaskin/lithiumpatch` 補丁 + 全語系翻譯對齊，
> 版本號升 **0.25.2 / versionCode 107**，同一把金鑰重簽（v1+v2+v3）。
> 第 2 版（0.25.0 / build 102）的內容保留在本檔下方「歷史」節。

## 成品（第 3 版）
- APK：`~/Downloads/Lithium-Pro-v0.25.2_build_107-zhTW補齊-lithiumpatch-重簽名.apk`
  - 位元組數 **28,291,261**（27 MB；比 102 版大很多是因為 lithiumpatch 塞進了字典與字型資產）
  - MD5 **`0445ce889ac87bce9c26acf61d5cf533`**
  - 已用 kdeconnect 寄到 RMX3366（裝置 id `3542135c9e7e4ed4832881805487071c`，
    命令 `kdeconnect-cli -d <id> --share <apk>`；注意本機 kdeconnect 26.08.2 的選項叫
    `--share`，**沒有** `--send-file`）
  - `package name='com.faultexception.reader' versionCode='107' versionName='0.25.2'`
  - minSdk 26／targetSdk 35（lithiumpatch 的 `minsdk` 補丁把 16 抬到 26）
  - 金鑰：`~/.android/lithium-l10n.keystore`，alias `lithium-l10n`
    （金鑰密碼**不入倉**：存在本地未追蹤的 `KEYSTORE-PASS.local`，內容為單一行純文字；
    下面所有命令以 `$LITH_KS_PASS` 代表它，用法 `export LITH_KS_PASS="$(cat KEYSTORE-PASS.local)"`。
    本倉是公開倉，憑證密碼跟著譯文一起放上去沒有意義、只會多一個洩漏面。）
    - 憑證 SHA-256 `8D:D7:29:E1:42:CA:12:E1:61:50:82:70:8B:0B:C1:86:38:2B:8E:3D:B9:5C:8B:30:49:2B:4F:C2:0A:87:50:ED`
      —— 與第 2 版（build 102）**完全相同**，所以从 102 可以直接覆蓋安裝、資料不丟。

## 這個倉庫放了什麼／本地多出來的是什麼
倉庫只放**可編輯的工作成果**（腳本、補丁、譯文、詞彙表、對照表、審計與建置日誌）；
862 MB 的 `build-0.25.2/`（apktool 解包樹、上游與產出 APK、lithiumpatch 的 git clone）
是可重現的中間產物，**一律 `.gitignore` 排除**，交付完就在本地清掉。

| 進倉 | 內容 |
|---|---|
| `README.md` | 本檔 |
| `merge-l10n.py` `audit.py` `localize-patch-strings.py` | 合併／審計／補丁字串資源化三個工具 |
| `translations-0.25.2.json` | 本輪新寫與改寫的譯文表（9 語系，186 條 override） |
| `values-default/` + 9 個 `values-<語系>/` | 最終成品資源檔（各 `strings.xml`、`plurals.xml`、`arrays.xml`；475 條／default 478） |
| `app_strings.tsv` `other-locales-fill.tsv` | 英文原文＋原簡中對照表（343 條）、其他 6 語系補齊來源表 |
| `lith-glossary.md` | 術語表與硬規則 |
| `lithiumpatch-0.25.1-compat.patch` | lithiumpatch 相容 0.25.1 的完整改動（10 檔 +325/−82） |
| `lithiumpatch-cmd-patchdir.go.txt` `lithiumpatch-cmd-scanline.py.txt` | 本輪自寫的 lithiumpatch 輔助工具原始碼（`.txt` 結尾是刻意不讓它被 `go build .` 捲進去） |
| `patch-strings.json` | lithiumpatch 硬編碼字串清單（`audit.py` 判定 app 字串要用） |
| `logs/` | 實測證據：`audit-report-0.25.2.txt`（ERROR 0／WARN 21 全文）、`run1–4.log`（30 補丁逐步）、`build-107*.log`、`apktool-*.log`、`patch-diff-106.diff`（補丁套到 app 的實際 smali／資源差異）、`lithiumpatch-meta.json` |
| **不進倉** | `build-0.25.2/`（含 `app-patched/` `prev-102/` `ref-102/` `app-106/` `upstream-res/` `lithiumpatch/` 解包樹與 `*.apk`）、`KEYSTORE-PASS.local` |

APK 本體走 **GitHub Release 資產**（不進 git 歷史）：
`https://github.com/Capricornus007/lithium-l10n/releases/tag/v0.25.2-build107`
→ 資產檔名 `Lithium-Pro-v0.25.2_build_107-zhTW-lithiumpatch-resigned.apk`
（顯示標籤「Lithium Pro 0.25.2 build 107（繁中補齊 + lithiumpatch + 重簽名）」；
**GitHub 會把資產檔名裡的非 ASCII 字元洗掉**，所以檔名用純半形，中文只放標籤；
本地對應檔名仍是 `~/Downloads/Lithium-Pro-v0.25.2_build_107-zhTW補齊-lithiumpatch-重簽名.apk`）
- 28,291,261 bytes｜MD5 `0445ce889ac87bce9c26acf61d5cf533`｜SHA-256 `a108839e8594d1fc641fa1ccf68ac6093c7f1b58dd2b550e49d46b3694649d67`
- 已實測把資產**從 GitHub 下載回來**比對：MD5／SHA-256 與本地交付檔逐字相同，
  且 `apksigner verify -v --min-sdk-version 21` 對下載件一樣回 v1／v2／v3 全 true（驗的是產物，不是配置）。
取回命令：
```sh
gh release download v0.25.2-build107 --repo Capricornus007/lithium-l10n --clobber
```

**新克隆重跑前要做的起手式**（腳本寫死讀 `build-0.25.2/` 下的工作檔）：
```sh
git clone git@github.com:Capricornus007/lithium-l10n.git && cd lithium-l10n
mkdir -p build-0.25.2
cp audit.py merge-l10n.py localize-patch-strings.py translations-0.25.2.json patch-strings.json build-0.25.2/
git clone https://github.com/pgaskin/lithiumpatch build-0.25.2/lithiumpatch   # HEAD c31bd53
cd build-0.25.2/lithiumpatch && git apply ../../../lithiumpatch-0.25.1-compat.patch
# 上游 APK 需自行取得（apkmirror 的 com.faultexception.reader 0.25.1 build 106），
# 放到 build-0.25.2/upstream-106.apk，再照下方「重跑步驟」走。
```

## 驗證輸出（全部是「產物」實測，不是配置）
```
$ apksigner verify -v --min-sdk-version 21 <apk>
Verifies
Verified using v1 scheme (JAR signing): true
Verified using v2 scheme (APK Signature Scheme v2): true
Verified using v3 scheme (APK Signature Scheme v3): true
```
（`--min-sdk-version 21` 不能省：本包 minSdk=26，省略時 apksigner 會跳過 v1 檢查、
直接把好包報成 `v1: false`。）
```
$ zipalign -c 4 <apk>            → OK（回傳碼 0）
$ aapt2 dump resources <apk> 各語系實數（string+plurals+array，逐語系完全對齊）
  zh-rTW 475｜zh-rHK 475｜zh-rCN 475｜de 475｜es 475｜pl 475｜pt-rBR 475｜ru 475｜tr 475
  （各為 string 465 + plurals 8 + array 2；default 另含 3 個 entryValues 技術陣列＝478）
$ keytool -printcert -jarfile <apk> → CN=Lithium l10n (local rebuild), OU=home, O=avatar, C=TW
```
`audit.py` 最終結果：**ERROR 0 件、WARN 21 件**（21 條全是「短文案偏長」與
「原文引號內有真空白」類的人工判斷項，詳見下方第 3 版審計節）。

## lithiumpatch 與 0.25.1 的相容性（改了什麼）
倉庫：`~/Downloads/lithium-l10n/build-0.25.2/lithiumpatch/`（`git clone pgaskin/lithiumpatch`，
HEAD `c31bd53`）。沒有頂層 Makefile，建置 `go build .`（root 的 `main.go`；
`cmd/` 是本轮自寫的輔助工具，不是建置目標）。
完整差異存檔：`~/Downloads/lithium-l10n/lithiumpatch-0.25.1-compat.patch`（10 檔、+325/−82）。

0.25.1 重新編譯後 smali 有三種「非語意漂移」，讓 30 個補丁裡的 7 個原樣失效（逐字比對找不到就整組 aborted）：
`.line` 行號位移、d8 暫存器配置改變（v0→v2、v3/v5→v2/v4）、匿名內部類別編號改變
（`ReaderActivity$7`→`$8`）與合成取用器改變（`access$1000`→`access$1100`）。

| 檔案 | 位置 | 改動 |
|---|---|---|
| `patches/patchdef/patch.go` | 第 248 行起新增 210 行 | 加容錯 helper：`smaliPattern`（`.line NN` 放成萬用）、`MustContainSmali`、`ReplaceStringSmali`、`ReplaceStringPrependSmali`、`ReplaceStringAppendSmali`、`MustContainRe`、`ReplaceStringRePrepend`、`ReplaceStringReLiteral`、`spliceAll`（手動拼接，避免 smali 內容的 `$id`／`$ScrollingViewBehavior` 被當成正規群組參照吃掉）、`PatchInnerClass`（動態定位匿名內部類別與合成取用器）。**只放寬「比對」，不放寬「取代內容」**；找不到就老實報錯，不會默默插錯碼 |
| `patches/invertcontent.go` | 第 7、322–330、351–364、451–463 行 | 改用 `PatchInnerClass`＋`MustContainRe`（$7→$8、access$1000→$1100 不再寫死）；插入的 smali 模板從 raw 反引號字串改成直譯字串——raw 字串裡的 `\n` 是「反斜線+n」兩個字元，會讓 smali 組譯器報 `Error for input '\'：Invalid text`（實測踩過兩次：`ReaderActivity$8.smali[286,70] Invalid text`、`HtmlContentWebView.smali[1910,53]`）；暫存器改用捕获群跟隨原文 |
| `patches/hyphenation.go` | 第 7、146–158 行 | 同上：`ReplaceStringRePrepend`＋捕获群（v3/v5→v2/v4），不再寫死暫存器名（寫死會蓋掉別人正在用的值） |
| `patches/fullbleed.go` | 第 7–11、24–32 行 | `MustContainRe` 匹配 `const/4 v[0-9]+, 0x1` 與 desugar 產出的 `LogTime$$ExternalSyntheticApiModelOutline[0-9]+`（類別序號與暫存器都會漂移） |
| `patches/moretoolbaractions.go` | 第 7–18、26–33 行 | 上游 0.25.1 自己已把「搜尋」改成 `showAsAction="always"`，原 patch 整段失效；改成 `(?:ifRoom|always)` 兩種來源值一律換成 `always`（0.25.0／0.25.1 都正確、可重跑） |
| `patches/coversize.go` | 第 27–30、109 行 | `MustContain`→`MustContainSmali`（`.line` 168→169） |
| `patches/extrathemes.go` | 第 49 行 | `ReplaceString`→`ReplaceStringSmali` |
| `patches/pseudomat3.go` | 第 70、82、112 行 | 同上（`.line` 漂移） |
| `patches/seriesdrawer.go` | 第 610 行 | `ReplaceStringPrepend`→`ReplaceStringPrependSmali` |
| `main.go` | 第 217–227 行 | 簽名從固定 `--min-sdk-version 26` 改成 `--min-sdk-version 21 --max-sdk-version 10000 --v1/v2/v3-signing-enabled true`（AI_RULES 規則 71：自家公開發布包一律 v1+v2+v3；原本的 26 讓 apksigner **不產生** v1 簽章） |

30 個補丁全跑成功（`build-0.25.2/run4.log`），產出 `patched-106.apk`；
之後才做翻譯合併與 107 版重建，順序是
`upstream-106.apk` →（lithiumpatch 30 補丁）→ `patched-106.apk` →（apktool 解包 `app-patched/`
→ `localize-patch-strings.py` 把補丁硬編碼的英文介面字串轉成 `@string` 資源
→ `merge-l10n.py` 合併全語系翻譯）→ `apktool b` → `zipalign` → `apksigner`。

## 本轮修掉的翻譯層缺陷（第 3 版重點）
接手時盤上已經有「合併＋簽名完成」的成品，但檢查後發現 4 類真問題，全部修完才重建重簽：

1. **雙層跳脫（最嚴重）**：`merge-l10n.py` 的 `esc()` 對「已經是 XML 原始形態」的值又逃一次
   `&`→`&amp;`，於是 `&lt;b&gt;` 變成 `&amp;lt;b&amp;gt;`。Android 取到的值就成了字面
   `&lt;b&gt;`，app 跑 `Html.fromHtml` 後畫面直接顯示 `<b>` 這幾個字（`pro_welcome_message`、
   `book_not_found_error_message`、`theme_preview_text` 全中，9 個語系各 3 條）。
   修法：`esc()` 不再逃 `&`/`<`（只逃單引號），另加 `normalize()` 把多逃的那一層壓回去。
2. **真標籤 vs 實體被混用**：英文原文一律用「實體」`&lt;b&gt;`（值就是含 `<b>` 字元的純字串，
   給 fromHtml 用）；上游若干語系的 Crowdin 譯文卻是「真標籤」`<b>`——兩者在 Android 語意不同
   （真標籤會讓 `getString` 回 Spanned，app 再跑 fromHtml 時標籤文字已經消失，粗體就掉了）。
   修法：新增 `align_markup()`，**以英文原文的形態為準**逐條對齊。
3. **分段換行被壓平**：英文有 6 條用引號包住、內部含真實換行的多段文字（錯誤訊息、同步摘要），
   繁中／簡中把它們壓成一整句，段落感整個不見。修法：`translations-0.25.2.json` 加 16 條
   override 補回 `\n\n`（zh-rTW 5、zh-rHK 5、zh-rCN 6）。
4. **上游 pl／pt-rBR 自己寫壞**：`pro_welcome_message` 的 pl 少了一組 `<br/><br/>`、
   pt-rBR 的標記被寫破成 `&lt;br/&lt;br/&gt;`、pl 有 `Synchronizacja::` 雙冒號、
   pt-rBR 句號後缺空格、pt-rBR 的 `Sync:` 沒翻、pl 把產品名翻成 `Dysk Google`
   （全部語系裡只有 pl 這樣，pt-rBR/es/tr/de/ru 都保留 `Google Drive`）——
   依規則 34／35 一併修正，並補進 override 表（pl 4 條）。

另外把 `audit.py` 補了三項它原本查不到的檢查（這正是上一条能藏這麼久的原因）：
- **B2 標記逐條一致**：先把值「解一層」（等同 Android 實際取到的文字）再比對標記集合，
  這樣 `&lt;b&gt;` 這類「實體化標記」才會進入比較（舊 B 項只打 XML 原始文字，兩邊都匹配不到、永遠綠）。
- **雙層跳脫偵測**：解一層之後還殘留 `&lt; &gt; &amp; &quot;` 就直接判 ERROR。
- **分段換行數比對**：原文引號內的真實換行數量要逐條相同。
同時擄正了 `merge-l10n.py` 的「上游來源」路徑：原本 `ups` 直接讀輸出目錄
`app-patched/res/values-<語系>`，重跑第二次會把自己上一次的成品當成上游，缺漏檢查就此變假綠燈；
現在改成讀 pristine 快照 `build-0.25.2/upstream-res/res`（`apktool d -s -o upstream-res patched-106.apk`）。

## 重跑步驟（下次補翻照這走，別手改 APK）
```sh
# 【只改譯文】從步驟 4) 開始即可；步驟 1)~3) 只在需要重打 lithiumpatch 補丁時才跑。
cd ~/Downloads/lithium-l10n

# 1) 打 lithiumpatch 補丁（上游來源＝build-0.25.2/upstream-106.apk）
#    注意：--apktool / --apksigner 的預設值是相對路徑 lib/*.jar，所以必須在 lithiumpatch 目錄裡跑。
export LITH_KS_PASS="$(cat ~/Downloads/lithium-l10n/KEYSTORE-PASS.local)"   # 金鑰密碼不入倉
cd build-0.25.2/lithiumpatch && go build -o bin/lithiumpatch .        # 建置（無頂層 Makefile；走 justfile）
./bin/lithiumpatch -k ~/.android/lithium-l10n.keystore \
  --keystore-alias lithium-l10n --keystore-passphrase "$LITH_KS_PASS" \
  --add-fonts fonts -d ../patch-diff-106.diff \
  -o ../patched-106.apk ../upstream-106.apk                            # 30 個補丁全跑，成功日誌見 run4.log

# 2) 解包（app-patched＝完整解包、會改；upstream-res＝只解資源，當「上游基準」用）
cd .. && apktool d -f -o app-patched patched-106.apk
apktool d -f -s -o upstream-res patched-106.apk

# 3) 把補丁硬編碼的英文介面字串轉成 @string 資源（只動 values/，會覆寫 res/values/strings.xml）
python3 localize-patch-strings.py

# 4) 合併全語系翻譯（先報缺漏、再寫入；有缺漏 --report 會 exit 1）
cd .. && python3 merge-l10n.py --report
python3 merge-l10n.py --write                  # 寫入 build-0.25.2/app-patched/res/values-<語系>/

# 5) 審計：ERROR 必須 0（WARN 屬人工判斷項）
python3 audit.py build-0.25.2/app-patched/res

# 6) 重建 → 對齊 → 簽名（v1+v2+v3）→ 驗收
cd build-0.25.2 && apktool b -o unaligned-107.apk app-patched
zipalign -f 4 unaligned-107.apk aligned-107.apk
apksigner sign --ks ~/.android/lithium-l10n.keystore --ks-key-alias lithium-l10n \
  --ks-pass pass:"$LITH_KS_PASS" --key-pass pass:"$LITH_KS_PASS" \
  --min-sdk-version 21 --max-sdk-version 10000 \
  --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
  --out "Lithium-Pro-v0.25.2_build_107-zhTW補齊-lithiumpatch-重簽名.apk" aligned-107.apk
apksigner verify -v --min-sdk-version 21 <apk>   # v1/v2/v3 必須三個 true（min-sdk-version 21 不能省）
aapt2 dump resources <apk> | grep -c '(zh-rTW) ' # 各語系條數要相同（本輪 475）
rm -f aligned-107.apk                             # 對齊後的中間檔可丟；unaligned 留著可重簽
```
譯文來源：`translations-0.25.2.json`（本輪新寫／改寫，186 條）→ `prev-102/res`（上一版成品，
僅在英文未變動時沿用）→ `upstream-res/res`（上游 0.25.1 自帶）。術語依 `lith-glossary.md`。
**兩份 `translations-0.25.2.json`（頂層與 `build-0.25.2/`）必須同步**，`merge-l10n.py` 讀的是
`build-0.25.2/` 那一份；改完頂層記得 `cp` 過去（兩份是同一份副本，目前 MD5 相同）。
lithiumpatch 編好的執行檔放在 `build-0.25.2/lithiumpatch/bin/`（`lithiumpatch`、`patchdir`）。

## ⚠️ 安裝注意事項（第 3 版）
- **金鑰與 102 版相同**（SHA-256 完全一致，已實測比對），所以：
  - 手機上裝的是我们上一版（build 102）→ **直接覆蓋安裝**即可，書單／進度／書籤／註解會保留。
  - 手機上還是别人那個 `CN=蓝鲨` 簽的 0.25.0 名人版 → **簽章不同，不能覆蓋**，Android 會報
    `INSTALL_FAILED_UPDATE_INCOMPATIBLE`。此時只能：
    1. 先在 app 內「設定 → 備份／匯出註解」把註解匯出（書檔本身是檔案，不會不見）；
    2. 解除安裝舊版（app 資料庫會被清掉：書單、閱讀進度、書籤、註解）；
    3. 安裝這次的 107 版，再匯回註解。
- 不能「降版」安裝：107 之後若又拿到 106／102 的包，要先卸再裝。
- 本包是 lithiumpatch 重組包，`Google Drive` 同步要用**自行建立的 Google APIs 專案**：
  簽名指紋 `1B:B4:C8:F4:D6:6F:12:89:F4:7C:E2:34:94:7B:BE:0A:D4:A9:DA:3F` 需要被加進
  有 Drive API 權限的 Google API 專案，否則同步會登不進去（lithiumpatch 執行日誌有提示）。
- minSdk 被抬到 26：Android 8.0 以下的機器裝不了（RMX3366 不受影響）。

## 尚未驗證（需要真機）
- 切到「中國台灣／中國港澳」後介面是否全繁中；pl/pt-rBR 等 6 語系的 rendering。
- `pro_welcome_message`／`book_not_found_error_message` 的粗體與斷行是否如預期（本輪是把
  「多逃一層／真標籤」修回「實體」，離線已驗證值與英文逐條相同，但沒有真機截圖佐證）。
- 複數句（1 本／3 本）顯示。

---

# 歷史：第 2 版（2026-10-22，0.25.0 / build 102）

## 成品
- APK：`~/Downloads/Lithium-Pro-v0.25.0_build_102-zhTW補齊-重簽名.apk`
  - 大小 7,976,644 bytes，MD5 `5f3aa9f3e8a61d0edef6a16a878f906f`（已用 kdeconnect 寄到 RMX3366）
  - 封裝：v1 + v2 + v3 簽章皆通過驗證
  - 簽章者：`CN=Lithium l10n (local rebuild), OU=home, O=avatar, C=TW`
  - 金鑰：`~/.android/lithium-l10n.keystore`，alias `lithium-l10n`（密碼同第 3 版，見上方「金鑰」說明，不入倉）
    （之後要再補翻，務必用同一把金鑰重簽，否則每次都要先資料清空重安裝）
- 翻譯原始檔（可直接編輯後重組）：`~/Downloads/lithium-l10n/`
  - `values-zh-rTW/` `values-zh-rHK/` `values-zh-rCN/` 各含 `strings.xml`、`plurals.xml`、`arrays.xml`
    （第 3 版已把這 9 個 `values-*` 目錄同步成 0.25.2 的最新成品）
  - `app_strings.tsv`＝343 條 app 字串的「英文原文＋原簡中譯文」對照表
  - `lith-glossary.md`＝術語與硬規則（下次改稿照著它就不會跑偏）


## 改了什麼
| 語系 | 改前 | 改後 |
|---|---|---|
| zh-rTW 台灣繁中 | 105 條（全是 AndroidX 圖示庫字串，app 介面整片英文） | **448 條全覆蓋** |
| zh-rHK 港澳繁中 | 105 條 | **448 條全覆蓋**（用詞改「導入／導出」） |
| zh-rCN 簡中 | 424 條（缺 24 條） | **448 條全覆蓋**，並修正 102 條（含 10 條真錯譯） |
| 複數句 plurals | 繁中完全沒有 | 7 組全部補上（書加入分類、刪除確認、搜尋結果數等） |
| 選單陣列 arrays | 繁中完全沒有 | 螢幕旋轉：關閉/直向/橫向；音量鍵翻頁：關閉/開啟/反向 |

修正過的 10 條簡中錯譯（值得留意）：
`backups_notice`（原譯漏掉「備份不含書籍本身」）、`goto_paper_page_dialog_count`、
`annotations_text_unavailable`、`export_failed_annotations_need_upgrade`、
`intent_launch_cant_open_book_invalid_stream`、`library_update_failed_details_malformed`、
`pref_book_wide_pages_title`、`theme_builtin_name_sepia`（「棕褐色」誤成「sepia」）、
`pref_licenses_title`、`pro_welcome_message`。

## ⚠️ 安裝前必讀（會有資料損失）
原 APK 是 `CN=蓝鲨`（www.bsh.me）簽的名人版重組包，我們沒有他那把私鑰，
所以**簽章不同 → 不能直接覆蓋安裝**，Android 會回報 `INSTALL_FAILED_UPDATE_INCOMPATIBLE`。

流程只能這樣：
1. 先在 app 內把註記／_highlight_ 匯出（設定 → 備份／匯出註解），書檔本身是檔案、不會丟。
2. 解除安裝舊的 Lithium Pro（app 資料庫會被清掉：書單、閱讀進度、書籤、註解）。
3. 安裝本次的 APK。

如果你想保留目前的閱讀進度與註解，我可以先用 adb 把
`/data/data/com.faultexception.reader` 整份備出來（需要手機連線、且已 root 或 app 允許 adb backup），
裝好新版再還原。要做的話說一聲，我寫好腳本再跑。

## 尚未驗證（需要手機）
- 實際在 Android 上切到「中國台灣／中國港澳」介面是否全部顯示繁中。
- 佔位符與 HTML 標記（`<b>`、`<a href>`、`<br/>`）在 UI 上渲染是否正常。
- 多複數句（1 本／3 本）顯示是否正確。
我已在離線層面驗證：448 條 ID 一一對應、佔位符 0 條不符、無簡體殘留、無 `您`
（僅 Google 服務原生库的 4 條仍用 `您`，那是 Google 自家繁中譯文，刻意沒動）。

## 第 2 版追加（依 AI_RULES 規則 33／34／35 逐條審計後修正）
審計工具：`audit.py`（已跑三份中文＋9 語系），規則 34 十項全查。查出的 7 類問題與修法：

| 規則 | 問題 | 處理 |
|---|---|---|
| 33 全語言＋地區變體 | `de/es/pl/pt-rBR/ru/tr` 各缺 19–24 條（上游有支持卻漏） | 全部補滿 448/448；用詞取自 Material Components AAR、ColorPickerView 上游庫、AOSP 各語系 strings.xml（見 `other-locales-fill.tsv`） |
| 34 術語不一致 | 繁中 `Send feedback` 有「傳送意見回饋／送出回饋」兩種 | 統一「傳送意見回饋」 |
| 34 術語不一致 | 繁中 `Create category` 有「建立／新增分類」 | 統一「建立分類」 |
| 34 術語不一致 | 簡中 `Search` 有「搜索／查找」 | 統一「搜索」 |
| 34 非專有名詞漏翻 | `chip_text` 繁中留英文「Chip text」 | 改「標籤文字」，簡中改「标签文字」 |
| 35／規則4 專有名詞 | 簡中 4 條把 Google Drive 翻成「Google 云端硬盘」 | 改回 `Google Drive` 並補中英間空格 |
| 34 語系互串 | 繁中檔查簡體字 | 以「簡體 exclusively 用字」清單复查，0 筆殘留（`者/建/升` 等屬繁簡同形，非誤） |

未支持語系（`fr/ja/ko/it/pt` 等 80 個）：上游 Lithium 本身就沒有任何 app 字串譯文，
只有圖示庫字串，所以切到那些語言介面仍是英文。要一併補（例如日文 343 條）跟我說，
我照同一套術語表派子代理做。

自檢結果（最終 APK 二進位資源表實測）：
`zh-rTW 457｜zh-rHK 457｜zh-rCN 458｜de/es/pl/pt-rBR/ru/tr 各 458` 條資源（字串＋複數＋陣列）。

> 以上為 0.25.0／build 102 當時的數字，已被第 3 版（0.25.2／107，9 語系各 475）取代。
> 第 2 版兩處漏網，第 3 版已補查：
> 1. 當時的 `audit.py` 查不到「雙層跳脫」與「真標籤 vs 實體」，所以 `&amp;lt;b&amp;gt;`
>    這類會讓實機顯示出字面 `<b>` 的問題整批過了關（也含 102 版自己的成品）；
>    另外 `merge-l10n.py` 當時把「上游來源」指向自己的輸出目錄，重跑會拿上次成品當基準，
>    缺漏檢查變假綠燈。兩處都已修正（見上方「本轮修掉的翻譯層缺陷」）。
> 2. 規則 35 的專有名詞只查了簡中（`Google 云端硬盘`），**波蘭語 `Dysk Google` 沒查**——
>    第 3 版已把 pl 的 4 處統一成 `Google Drive`（其他 5 個非英文語系本來就保留原名）。
