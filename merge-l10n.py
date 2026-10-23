#!/usr/bin/env python3
# 上游 0.25.1 + lithiumpatch 的字串資源，與既有翻譯（上一版交付的 0.25.0 全語系成果）逐 key 合併。
#
# 取用順序（每個 key）：
#   1. OVERRIDES（translations-0.25.2.json：這輪新寫／改寫的譯文，含 lithiumpatch 新增的介面字串）
#   2. 上一版已交付的譯文——但只有在「英文原文沒有變動」時才沿用（變動的要重翻）
#   3. 上游 0.25.1 該語系自己帶的譯文
#   4. 以上都沒有 → 列入缺漏清單並讓腳本失败（規則 33：不留餘地，不准默默退回英文）
#
# 上游已刪除的 key 不會出現在輸出裡（因為輸出是以新的英文 key 集合為準）→ 自動跟著刪。
#
# 用法：
#   python3 merge-l10n.py --report     只報告缺漏與變動
#   python3 merge-l10n.py --write      寫入 app-patched/res/values-<語系>/
import os, re, sys, json, xml.etree.ElementTree as ET

BASE = os.path.expanduser('~/Downloads/lithium-l10n/build-0.25.2')
NEWDIR = os.path.join(BASE, 'app-patched/res')
PREVDIR = os.path.join(BASE, 'prev-102/res')
# 上游 0.25.1（已打 lithiumpatch）的**乾淨**資源快照：apktool d -s -o upstream-res patched-106.apk
# 2026-10-23 修正：原本 ups 直接讀 NEWDIR/values-<語系>，而 NEWDIR 同時是輸出目錄——
# 重跑時會把「上一次的成品」當上游來源，缺漏檢查就此失效（假綠燈）。
UPSDIR = os.path.join(BASE, 'upstream-res/res')
TABLE = os.path.join(BASE, 'translations-0.25.2.json')
LOCALES = ['zh-rTW', 'zh-rHK', 'zh-rCN', 'de', 'es', 'pl', 'pt-rBR', 'ru', 'tr']
# 只當值用、翻了會壞設定的技術性陣列（同時是 MultiSelectListPreference 的 entryValues）
NO_TRANSLATE_ARRAYS = {'dict_names', 'pref_screen_rotation_values', 'pref_volume_pagination_values'}


def inner(el):
    """取元素「內部」的文字（保留 XML 標記原樣）。空元素回傳空字串。"""
    if len(el) == 0 and (el.text or '').strip() == '':
        return ''
    s = ET.tostring(el, encoding='unicode')
    m = re.match(r'^<[^>]*>(.*)</[^>]*>\s*$', s, re.S)
    if m:
        return m.group(1).strip()
    return ''.join(el.itertext()).strip()


def load(resdir):
    out = {'strings': {}, 'plurals': {}, 'arrays': {}}
    for kind, fname in (('strings', 'strings.xml'), ('plurals', 'plurals.xml'), ('arrays', 'arrays.xml')):
        p = os.path.join(resdir, fname)
        if not os.path.exists(p):
            continue
        for el in ET.parse(p).getroot():
            if el.tag == 'string' and kind == 'strings':
                out['strings'][el.get('name')] = inner(el)
            elif el.tag == 'plurals' and kind == 'plurals':
                out['plurals'][el.get('name')] = {i.get('quantity'): inner(i) for i in el.findall('item')}
            elif el.tag == 'string-array' and kind == 'arrays':
                out['arrays'][el.get('name')] = [inner(i) for i in el.findall('item')]
    return out


def normalize(s):
    # 值在記憶體裡已經是「XML 內部原始文字」形態（inner() 用 ET.tostring 取得：
    # 實體保留成 &lt; / &amp;，真正的標籤保留成 <b>）。上一版交付檔與上游若干語系
    # 把 &lt;b&gt; 又多逃了一层成 &amp;lt;b&amp;gt;，實機顯示會跑出「&lt;b&gt;」字面字元
    # （規則 34「HTML 標記逐條一致」）。這裡壓回一层，只動實體、不動真正的標籤。
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r'&amp;(?=(?:lt|gt|amp|quot|apos)\b)', '&', s)
    return s


TAG_RE = re.compile(r'</?[A-Za-z][^<>]*>')
ENTITY_TAG_RE = re.compile(r'&lt;(/?[A-Za-z][^&<>]*?)&gt;|&lt;(/?[A-Za-z][^&<>]*?)>')


def align_markup(val, en_raw):
    # Android 資源裡「真標籤 <b>」與「實體 &lt;b&gt;」是兩件不同的事：
    #   真標籤 → getString 得到 Spanned（span 化的粗體），app 再跑 fromHtml 時標籤文字已不在；
    #   實體   → getString 得到含 `<b>` 字元的純字串，app 跑 fromHtml 才真的渲染成粗體。
    # Lithium 的 pro_welcome_message / book_not_found_error_message 等一律是「實體」形態，
    # 但上游各語系（Crowdin 譯者）常改成真標籤、或多逃一層成 &amp;lt;——兩種都會讓實機顯示跑掉。
    # 這裡以**英文原文的形態**為準逐條對齊（規則 34：標記逐條一致）。
    if not isinstance(en_raw, str):
        return val
    en_entity = bool(ENTITY_TAG_RE.search(en_raw))
    en_real = bool(TAG_RE.search(en_raw))
    if en_entity and not en_real:
        return TAG_RE.sub(lambda m: m.group(0).replace('<', '&lt;').replace('>', '&gt;'), val)
    if en_real and not en_entity:
        return ENTITY_TAG_RE.sub(lambda m: '<' + (m.group(1) or m.group(2)) + '>', val)
    return val


def esc(s, en_raw=None):
    # 輸出到 Android 資源檔：值已是 XML 原始形態，故 **不得**再逃 & 與 <
    # （2026-10-23 修正：原本的 .replace('&','&amp;') 就是 &amp;lt; 雙層跳脫的根因）。
    # 單引號仍要用反斜線跳脫（未跳脫的 ' 會造成 aapt 編譯錯誤）。
    if en_raw is not None:
        s = align_markup(s, en_raw)
    return normalize(s).replace("'", "\\'")


def dump(resdir, data, ref):
    os.makedirs(resdir, exist_ok=True)
    for kind, fname in (('strings', 'strings.xml'), ('plurals', 'plurals.xml'), ('arrays', 'arrays.xml')):
        if not data[kind]:
            continue
        lines = ['<?xml version="1.0" encoding="utf-8"?>', '<resources>']
        for name, v in data[kind].items():
            if kind == 'strings':
                lines.append(f'    <string name="{name}">{esc(v, ref["strings"].get(name))}</string>')
            elif kind == 'plurals':
                lines.append(f'    <plurals name="{name}">')
                for q, t in v.items():
                    enq = ref['plurals'].get(name, {}).get(q) or ref['plurals'].get(name, {}).get('other')
                    lines.append(f'        <item quantity="{q}">{esc(t, enq)}</item>')
                lines.append('    </plurals>')
            else:
                lines.append(f'    <string-array name="{name}">')
                for i, t in enumerate(v):
                    lines.append(f'        <item>{esc(t, (ref["arrays"].get(name) or [""] * (i + 1))[i])}</item>')
                lines.append('    </string-array>')
        lines.append('</resources>')
        open(os.path.join(resdir, fname), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


def main():
    write_mode = '--write' in sys.argv
    new_def = load(os.path.join(NEWDIR, 'values'))
    prev_def = load(os.path.join(PREVDIR, 'values'))
    overrides = json.load(open(TABLE, encoding='utf-8')) if os.path.exists(TABLE) else {}

    stats = {}
    problems = []
    for loc in LOCALES:
        prev = load(os.path.join(PREVDIR, 'values-' + loc))
        ups = load(os.path.join(UPSDIR, 'values-' + loc))
        ov = overrides.get(loc, {})
        merged = {'strings': {}, 'plurals': {}, 'arrays': {}}
        reused = rewritten = fromupstream = 0

        for k, en in new_def['strings'].items():
            if k in ov:
                merged['strings'][k] = ov[k]
                rewritten += 1
            elif k in prev['strings'] and prev_def['strings'].get(k) == en:
                merged['strings'][k] = prev['strings'][k]
                reused += 1
            elif k in ups['strings']:
                merged['strings'][k] = ups['strings'][k]
                fromupstream += 1
            else:
                problems.append(f'{loc}: 缺譯 string/{k}（英文：{en}）')

        for k, ens in new_def['plurals'].items():
            unchanged = prev_def['plurals'].get(k) == ens
            if k in ov:
                merged['plurals'][k] = ov[k]
                rewritten += 1
            elif unchanged and k in prev['plurals']:
                merged['plurals'][k] = prev['plurals'][k]
                reused += 1
            elif k in ups['plurals']:
                merged['plurals'][k] = ups['plurals'][k]
                fromupstream += 1
            else:
                problems.append(f'{loc}: 缺譯 plurals/{k}')

        for k, ens in new_def['arrays'].items():
            if k in NO_TRANSLATE_ARRAYS:
                continue  # 技術識別用，故意不進 locale 檔
            unchanged = prev_def['arrays'].get(k) == ens
            if k in ov:
                merged['arrays'][k] = ov[k]
                rewritten += 1
            elif unchanged and k in prev['arrays']:
                merged['arrays'][k] = prev['arrays'][k]
                reused += 1
            elif k in ups['arrays']:
                merged['arrays'][k] = ups['arrays'][k]
                fromupstream += 1
            else:
                problems.append(f'{loc}: 缺譯 array/{k}')

        stats[loc] = (len(merged['strings']) + len(merged['plurals']) + len(merged['arrays']),
                      reused, rewritten, fromupstream)
        if write_mode:
            dump(os.path.join(NEWDIR, 'values-' + loc), merged, new_def)

    print(f"語系        條數  沿用舊譯  本輪新寫  取上游")
    for loc, (n, r, w, u) in stats.items():
        print(f'{loc:9s} {n:5d} {r:9d} {w:9d} {u:7d}')

    # 上游被刪掉的 key（舊譯文有、新英文沒有）→ 報告，不寫入就等于跟著刪
    for kind in ('strings', 'plurals', 'arrays'):
        gone = [k for k in prev_def[kind] if k not in new_def[kind]]
        if gone:
            print(f'\n上游/patch 已移除的 {kind}（自動跟著刪）：{gone}')

    if problems:
        print(f'\n!! 缺漏 {len(problems)} 條：')
        for p in problems[:200]:
            print('   ', p)
        sys.exit(1)
    print('\n無缺漏。' + ('  已寫入 ' + NEWDIR if write_mode else '（僅報告）'))


if __name__ == '__main__':
    main()
