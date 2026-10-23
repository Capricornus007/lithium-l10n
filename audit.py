#!/usr/bin/env python3
# Lithium 本地化一致性檢查（規則 33／34／35 逐條掃描）。
#
# 用法：
#   python3 audit.py <res 目錄> [--locales zh-rTW,zh-rHK,...] [--all]
#     <res 目錄> 例：build-0.25.2/app-patched/res
#     --all      連 WARN 一起列出（預設只列 ERROR 與 WARN 統計）
#
# 分級：
#   ERROR（一定要修，非零就 exit 1）
#     A 各語系 strings/plurals/arrays 與預設（英文）key 一一對應
#     B 佔位符 %s/%1$d/%%、HTML 標記 <b>/<a href>/<br/>、跳脫 \n \uXXXX 逐條一致
#     B2（2026-10-23 補）先把值解一層實體（＝Android 實際取到的文字）再比：
#        ・標記字元集合要逐條相同（&lt;b&gt; 這類「實體化標記」也一起比，舊 B 項比不到）
#        ・譯文不得殘留 &lt; &gt; &amp; &quot;（雙層跳脫；實機會印出字面實體）
#        ・原文以引號包住的真實換行（分段）數量要逐條相同
#     C 同檔重複 key（會造成編譯錯誤）
#     D 繁中（zh-rTW/zh-rHK）檔的簡體字殘留；app 字串出現「您」
#     E 未跳脫的單引號、錯誤的雙反斜線跳脫（\\+中日韓字，會顯示成多一個反斜線）
#     F app 字串漏翻（譯文與英文相同，且非專有名詞／技術字串）
#   WARN（人工判斷，可接受）
#     G 選單／按鈕類過長（可能被 UI 截斷，規則 37）
#     H 原文外層雙引號（保留首尾空格用）在譯文被拿掉
#
# 「library 字串」= Google AppCompat/Material/Play Services 自带的譯文，
# 一律不動（規則 14：對方有且更好就沿用），因此 D/F/G 只套在 app 自己的字串上。
# app 字串清單来自 app_strings.tsv（343 條）與 patch-strings.json（lithiumpatch 新增）。
import os, re, sys, json, html, xml.etree.ElementTree as ET
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SIMPLIFIED_MARKERS = set('图页关内里档设书库选开进变应导单体积阅听们说时这让从众严历温烟营卫产厂沪碱尘丑苏顾为办处辽执识记评谢议词语诉调点战贝负贩购储报届属帐币岁岂')  # 只收「簡體独有」字形（象/麼/序/液/租/空/置/自 等繁簡同形者不收）
PLACEHOLDER = re.compile(r'%(\d+\$)?[sdfic]')
PERCENT = re.compile(r'%%')
HTMLTAG = re.compile(r'</?(?:b|i|u|em|strong|small|big|br|a)\b[^>]*/?>')
# 解一層實體之後，值裡面真正的標記字元（含 &lt;b&gt; 這種「以實體存著的標記」，
# 對 Android 而言值就是 <b> 文字，app 若跑 Html.fromHtml 就會渲染成標記）
MARKUP_IN_VALUE = re.compile(r'</?[A-Za-z][^<>]*>')
# 解一層之後仍剩 &lt; / &gt; / &amp; / &quot; 者＝雙層跳脫（實機顯示成字面實體，屬錯誤）
DOUBLE_ESC = re.compile(r'&(?:lt|gt|amp|quot|apos);')
NEWLINE_ESC = re.compile(r'\\n')
UNICODE_ESC = re.compile(r'\\u[0-9a-fA-F]{4}')
# 譯文等於英文也屬正確的條目（專有名詞、純符號、技術值）
OK_COPY = {'URL:', '%1$s (Pro)', 'Lithium', 'Lithium Pro', 'Chrome OS', 'OK', ':', '%1$d/%2$d',
           'androidx.startup'}
# 這些 key 的值是技術字串（SVG path、behavior 類別名、資源參考），必須與原文相同
TECH_KEY_RE = re.compile(r'^(path_|.*_behavior$|androidx_|.*_svg$|mtrl_picker_(cancel|confirm)$|v7_preference_)')
# 保留 Google 原文「您」的條目（Google 自家繁中譯文，規則 14 沿用不修改）
GOOGLE_NIN_KEYS = ('common_google_play_services', 'common_signin_button', 'provider_name',
                   'status_bar_notification', 'permissions', 'request')


def is_app_key(k, appkeys):
    return k in appkeys


def inner(el):
    """取元素內部文字；空元素（例：<item quantity="one"></item>）回傳空字串，
    不然會把序列化後的標籤本身當成譯文，檢查與合併都會被污染。"""
    if len(el) == 0 and (el.text or '').strip() == '':
        return ''
    s = ET.tostring(el, encoding='unicode')
    m = re.match(r'^<[^>]*>(.*)</[^>]*>\s*$', s, re.S)
    if m:
        return m.group(1).strip()
    return ''.join(el.itertext()).strip()


def load(resdir, loc):
    d = os.path.join(resdir, 'values' if loc == 'default' else 'values-' + loc)
    out = {'strings': {}, 'plurals': {}, 'arrays': {}}
    if not os.path.isdir(d):
        return out
    for kind, fname in (('strings', 'strings.xml'), ('plurals', 'plurals.xml'), ('arrays', 'arrays.xml')):
        p = os.path.join(d, fname)
        if not os.path.exists(p):
            continue
        root = ET.fromstring(open(p, encoding='utf-8').read())
        for el in root:
            if el.tag == 'string' and kind == 'strings':
                out['strings'][el.get('name')] = inner(el)
            elif el.tag == 'plurals' and kind == 'plurals':
                out['plurals'][el.get('name')] = {i.get('quantity'): inner(i) for i in el.findall('item')}
            elif el.tag == 'string-array' and kind == 'arrays':
                out['arrays'][el.get('name')] = [inner(i) for i in el.findall('item')]
    return out


def raw_lines(resdir, loc):
    d = os.path.join(resdir, 'values' if loc == 'default' else 'values-' + loc)
    out = {}
    for fname in ('strings.xml', 'plurals.xml', 'arrays.xml'):
        p = os.path.join(d, fname)
        if os.path.exists(p):
            out[fname] = open(p, encoding='utf-8').read().splitlines()
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    resdir = os.path.expanduser(sys.argv[1])
    show_all = '--all' in sys.argv
    locales = ['zh-rTW', 'zh-rHK', 'zh-rCN', 'de', 'es', 'pl', 'pt-rBR', 'ru', 'tr']
    for i, a in enumerate(sys.argv):
        if a == '--locales':
            locales = sys.argv[i + 1].split(',')

    # app 自己的字串 key（其餘視為 Google 函式庫自带譯文，不动）
    appkeys = set()
    tsv = os.path.join(HERE, 'app_strings.tsv')
    if os.path.exists(tsv):
        for line in open(tsv, encoding='utf-8'):
            appkeys.add(line.split('\t')[0])
    pj = os.path.join(HERE, 'build-0.25.2', 'patch-strings.json')
    if os.path.exists(pj):
        appkeys |= set(json.load(open(pj, encoding='utf-8')))
    # 這輪新加的 17 個 lithiumpatch 介面字串（萬一 patch-strings.json 不在同一層）
    appkeys |= {k for k in load(resdir, 'default')['strings']
                if k.startswith(('pref_series', 'pref_dict', 'pref_hyphenation', 'pref_progress_badge',
                                 'pref_no_page', 'pref_fullscreen_bleed', 'pref_hide_', 'pref_disable_dict',
                                 'display_settings_content_invert', 'action_invert_rotation',
                                 'no_books_series', 'series_title', 'pref_category_dict'))}

    no_trans = {'dict_names', 'pref_screen_rotation_values', 'pref_volume_pagination_values'}
    default = load(resdir, 'default')
    errors, warns = [], []

    def tag(loc, key):
        return f'{loc}: {key}'

    for loc in locales:
        t = load(resdir, loc)
        # --- A. key 一一對應 ---
        for k in default['strings']:
            if k not in t['strings']:
                errors.append(f'{tag(loc,k)} 缺 key string/{k}')
        for k in t['strings']:
            if k not in default['strings']:
                errors.append(f'{tag(loc,k)} 多出 key（上游已無此條，應跟著刪）')
        for kind, sing in (('plurals', 'plurals'), ('arrays', 'array')):
            for k in default[kind]:
                if k in no_trans:
                    continue
                if k not in t[kind]:
                    errors.append(f'{tag(loc,k)} 缺 {sing}/{k}')
            for k in t[kind]:
                if k not in default[kind]:
                    errors.append(f'{tag(loc,k)} 多出 {sing}/{k}（上游已無此條）')

        # --- C. 重複 key ---
        for fname, lines in raw_lines(resdir, loc).items():
            seen = defaultdict(int)
            for line in lines:
                m = re.search(r'<(?:string|plurals|string-array) name="([^"]+)"', line)
                if m:
                    seen[m.group(1)] += 1
            for k, v in seen.items():
                if v > 1:
                    errors.append(f'{loc}/{fname}: {k} 重複 {v} 次')

        # 逐條比對
        pairs = [(k, default['strings'].get(k, ''), t['strings'].get(k, '')) for k in t['strings']]
        pairs += [(f'{k}[{i}]', v, (t['arrays'][k][i] if i < len(t['arrays'].get(k, [])) else ''))
                  for k in t['arrays'] if k not in no_trans for i, v in enumerate(default['arrays'].get(k, []))]

        # 複數句（plurals）另開一輪：各語言的複數形數量本來就不同
        # （中文只有 other、俄文有 one/few/many/other），所以
        #   · 佔位符用「交集⊆譯文⊆聯集」判定（譯文可以比某個英文形多/少用到數字，
        #     但不能用到該組根本沒有的位置參數，也不能漏掉每個形都有的參數）
        #   · HTML 標記與 \n 則對「同名的英文形（沒有就拿 other 當基準）」要求完全一致
        for k in t['plurals']:
            den = default['plurals'].get(k, {})
            if not den:
                continue
            ph_union = set()
            for v in den.values():
                ph_union |= set(PLACEHOLDER.findall(v))
            ph_all = None
            for v in den.values():
                s = set(PLACEHOLDER.findall(v))
                ph_all = s if ph_all is None else (ph_all & s)
            if 'other' not in t['plurals'][k]:
                errors.append(f'{loc}: plurals/{k} 缺 other 形（其他複數形會退回英文）')
            for q, tr in t['plurals'][k].items():
                if q not in ('zero', 'one', 'two', 'few', 'many', 'other'):
                    errors.append(f'{loc}: plurals/{k} quantity 名稱非法：{q}')
                en = den.get(q, den.get('other', ''))
                key = f'{k}[{q}]'
                ph = set(PLACEHOLDER.findall(tr))
                if not (ph_all <= ph <= ph_union):
                    errors.append(f'{tag(loc,key)} 佔位符不符（應介於 {sorted(ph_all)} ∪ … ⊆ {sorted(ph_union)}，實得 {sorted(ph)}）')
                for rx, label in ((HTMLTAG, 'HTML 標記'), (NEWLINE_ESC, r'\n'), (UNICODE_ESC, r'\u')):
                    a, b = sorted(rx.findall(en)), sorted(rx.findall(tr))
                    if a != b:
                        errors.append(f'{tag(loc,key)} {label}不一致：英文 {a} ≠ 譯文 {b}')
                # B2（複數句同样適用：解一層後比標記、查雙層跳脫、查分段換行）
                ven, vtr = html.unescape(en), html.unescape(tr)
                a, b = sorted(MARKUP_IN_VALUE.findall(ven)), sorted(MARKUP_IN_VALUE.findall(vtr))
                if a != b:
                    errors.append(f'{tag(loc,key)} 標記不一致（解一層後）：英文 {a} ≠ 譯文 {b}')
                if DOUBLE_ESC.findall(vtr):
                    errors.append(f'{tag(loc,key)} 雙層跳脫（實機顯示成字面實體）：{tr[:60]!r}')
                if en.count('\n') != tr.count('\n'):
                    errors.append(f'{tag(loc,key)} 分段換行數不符：英文 {en.count(chr(10))} ≠ 譯文 {tr.count(chr(10))}')
                if len(PERCENT.findall(en)) != len(PERCENT.findall(tr)):
                    errors.append(f'{tag(loc,key)} %% 數量不一致：{en!r} / {tr!r}')
                if tr == en and is_app_key(k, appkeys) and loc.startswith('zh') \
                   and not TECH_KEY_RE.match(k) and len(en.split()) > 1 and not en.startswith('%'):
                    errors.append(f'{tag(loc,key)} app 複數句未翻譯：{en!r}')

        basekey = lambda k: k.split('[')[0]
        for key, en, tr in pairs:
            k = basekey(key)
            app = is_app_key(k, appkeys)
            # --- B. 佔位符／標記／換行 ---
            for rx, label in ((PLACEHOLDER, '佔位符'), (HTMLTAG, 'HTML 標記'),
                              (NEWLINE_ESC, r'\n'), (UNICODE_ESC, r'\u')):
                a, b = sorted(rx.findall(en)), sorted(rx.findall(tr))
                if a != b:
                    errors.append(f'{tag(loc,key)} {label}不一致：英文 {a} ≠ 譯文 {b}')
            if len(PERCENT.findall(en)) != len(PERCENT.findall(tr)):
                errors.append(f'{tag(loc,key)} %% 數量不一致：{en!r} / {tr!r}')
            # --- B2. 標記／雙層跳脫／分段換行（2026-10-23 補：規則 34 的原始盲點）---
            # inner() 回傳的是「XML 原始形態」（實體仍是 &lt;、真標籤仍是 <b>），
            # 舊 B 項用 HTMLTAG 直接打這層文字，於是 &lt;b&gt; 這種「實體化標記」
            # 兩邊都匹配不到、永遠通過；而 &amp;lt;b&amp;gt;（多逃一層，實機會顯示
            # 出字面 &lt;b&gt;）也一樣漏網。下面先解一層（等同 Android 取到的值）再比。
            ven, vtr = html.unescape(en), html.unescape(tr)
            a, b = sorted(MARKUP_IN_VALUE.findall(ven)), sorted(MARKUP_IN_VALUE.findall(vtr))
            if a != b:
                errors.append(f'{tag(loc,key)} 標記不一致（解一層後）：英文 {a} ≠ 譯文 {b}')
            da = DOUBLE_ESC.findall(vtr)
            if da:
                errors.append(f'{tag(loc,key)} 雙層跳脫（實機顯示成字面實體）{sorted(set(da))}：{tr[:60]!r}')
            if en.count('\n') != tr.count('\n'):
                errors.append(f'{tag(loc,key)} 分段換行數不符：英文 {en.count(chr(10))} ≠ 譯文 {tr.count(chr(10))}（原文用引號保留的真實換行）')
            # --- E. 跳脫 ---
            if re.search(r'\\\\(?=[\u4e00-\u9fff])', tr):
                errors.append(f'{tag(loc,key)} 雙反斜線誤跳脫（會顯示出反斜線）：{tr!r}')
            if re.search(r'(?<!\\)[\'’]', tr) and not (tr.startswith('"') and tr.endswith('"')) \
               and re.search(r'[A-Za-z\u4e00-\u9fff][\'’]', tr):
                errors.append(f'{tag(loc,key)} 單引號未跳脫：{tr!r}')
            # --- D. 簡體殘留／您 ---
            if loc in ('zh-rTW', 'zh-rHK'):
                bad = sorted({c for c in tr if c in SIMPLIFIED_MARKERS})
                if bad:
                    errors.append(f'{tag(loc,key)} 簡體殘留「{ ''.join(bad)}」：{tr!r}')
                if '您' in tr and app:
                    errors.append(f'{tag(loc,key)} app 字串用了「您」：{tr!r}')
            # --- F. 漏翻 ---
            if tr == en and app and loc.startswith('zh'):
                tech = (en in OK_COPY or TECH_KEY_RE.match(k) or en.startswith('%')
                        or re.match(r'^(com\.|androidx\.|@|https?:)', en)
                        or len(en.split()) <= 1          # 單一 Token（含純符號、純佔位符）
                        or re.match(r'^[A-Z][A-Za-z0-9_.$ ]{0,15}[:%]?$', en))
                if not tech:
                    errors.append(f'{tag(loc,key)} app 字串未翻譯：{en!r}')
            # --- G. 過長（WARN）---
            if loc.startswith('zh') and re.search(r'_(title|action)$|^action_|^pref_', k) and len(tr) > 15 \
               and not re.search(r'[。？！…]$', tr):
                warns.append(f'{tag(loc,key)} 短文案偏長（{len(tr)} 字）：{tr!r}')
            # --- H. 外層雙引號（WARN）---
            # 只有「引號inside 真的有首尾空白」才是值得警示的情況：apktool 对任何
            # 含真實換行的值都會加引號，那種只是多段文字、不是首尾空格（2026-10-23 修正：
            # 舊寫法把這類全數當成問題，176 條 WARN 裡一大半是假陽性）。
            if (en.startswith('"') and en.endswith('"')) and not (tr.startswith('"') and tr.endswith('"')):
                inner_en = en[1:-1]
                if inner_en != inner_en.strip():
                    warns.append(f'{tag(loc,key)} 原文用雙引號保留首尾空格，譯文未沿用：{inner_en[:30]!r}')
    print('== 各語系條數（strings+plurals+arrays 的 key 數）==')
    for loc in locales:
        t = load(resdir, loc)
        print(f'  {loc:9s} {len(t["strings"])} + {len(t["plurals"])} + {len(t["arrays"])} = '
              f'{len(t["strings"]) + len(t["plurals"]) + len(t["arrays"])}')
    print(f'  default   {len(default["strings"])} + {len(default["plurals"])} + {len(default["arrays"])} = '
          f'{len(default["strings"]) + len(default["plurals"]) + len(default["arrays"])}  '
          f'（其中 {len(no_trans)} 個陣列是 entryValues，屬技術值刻意不進 locale 檔）')

    print(f'\nERROR {len(errors)} 件、WARN {len(warns)} 件')
    for e in errors:
        print('  [E]', e)
    if show_all:
        for w in warns:
            print('  [W]', w)
    else:
        for w in warns[:12]:
            print('  [W]', w)
        if len(warns) > 12:
            print(f'  [W] …（還有 {len(warns) - 12} 條，加 --all 看全部）')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
