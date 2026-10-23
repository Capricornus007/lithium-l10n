#!/usr/bin/env python3
# 把 lithiumpatch 寫死在 XML 裡的英文介面字串，改成年源資源（@string/...），
# 好讓所有語系都能覆蓋（規則 33：倉庫支持的每個語系都要翻、不留餘地）。
# 只做「引用替換＋新增字串」，不改任何 smali，因此不影響 patch 的逻辑。
import os, re, sys, json

BASE = os.path.expanduser('~/Downloads/lithium-l10n/build-0.25.2')
RES = os.path.join(BASE, 'app-patched/res')

# key -> (英文原文, [(檔案, 寫死的字串), ...])
NEW = {
    'pref_category_dict':            ('Dictionary', [('res/xml/preferences.xml', 'Dictionary')]),
    'pref_disable_dictionaries_title': ('Disable dictionaries', [('res/xml/preferences.xml', 'Disable dictionaries')]),
    'pref_dict_examples_title':      ('Show examples', [('res/xml/preferences.xml', 'Show examples')]),
    'pref_dict_word_info_title':     ('Show word info', [('res/xml/preferences.xml', 'Show word info')]),
    'pref_dict_small_font_title':    ('Use smaller font size', [('res/xml/preferences.xml', 'Use smaller font size')]),
    'pref_no_page_animation_title':  ('Disable page turn animation', [('res/xml/preferences.xml', 'Disable page turn animation')]),
    'pref_fullscreen_bleed_title':   ('Fullscreen reading full-bleed', [('res/xml/preferences.xml', 'Fullscreen reading full-bleed')]),
    'pref_hide_library_footer_title': ('Hide footer (grid view)', [('res/xml/preferences.xml', 'Hide footer (grid view)')]),
    'pref_hide_reader_footer_title': ('Hide footer slider (reader)', [('res/xml/preferences.xml', 'Hide footer slider (reader)')]),
    'pref_hyphenation_title':        ('Use hyphenation', [('res/xml/preferences.xml', 'Use hyphenation')]),
    'pref_progress_badge_title':     ('Show reading progress badge', [('res/xml/preferences.xml', 'Show reading progress badge')]),
    'pref_series_in_drawer_title':   ('Show series in drawer', [('res/xml/preferences.xml', 'Show series in drawer')]),
    'pref_series_metadata_title':    ('Show series metadata', [('res/xml/preferences.xml', 'Show series metadata')]),
    'display_settings_content_invert': ('Invert', [('res/layout/fragment_display_settings.xml', 'Invert'),
                                                    ('res/layout-v17/fragment_display_settings.xml', 'Invert')]),
    'action_invert_rotation':        ('Invert Rotation', [('res/menu/reader.xml', 'Invert Rotation')]),
    'no_books_series':               ('No books in series', [('res/layout/empty_series.xml', 'No books in series')]),
    'series_title':                  ('Series', [('res/layout/series_list_header.xml', 'Series')]),
}


def add_strings():
    p = os.path.join(RES, 'values/strings.xml')
    s = open(p, encoding='utf-8').read()
    lines = s.rstrip('\n').split('\n')
    for key, (en, _) in NEW.items():
        if f'name="{key}"' in s:
            continue
        entry = f'    <string name="{key}">{en}</string>'
        # 依字母順序插入（apktool 產出就是排序過的，維持一致性）
        idx = len(lines) - 1
        for i, l in enumerate(lines):
            m = re.match(r'\s*<string name="([^"]+)"', l)
            if m and m.group(1) > key:
                idx = i
                break
        lines.insert(idx, entry)
        s = '\n'.join(lines) + '\n'
    open(p, 'w', encoding='utf-8').write(s)
    return s


def rewrite_refs():
    done = {}
    for key, (en, files) in NEW.items():
        for rel, literal in files:
            # NEW 表里的路徑是相對 res/ 的上層（與 patch diff 一致），這裡要減掉開頭的 res/
            p = os.path.join(RES, rel[len('res/'):] if rel.startswith('res/') else rel)
            if not os.path.exists(p):
                print(f'  ！找不到 {rel}（略過 {key}）')
                continue
            s = open(p, encoding='utf-8').read()
            old = f'"{literal}"'
            new = f'"@string/{key}"'
            # 只換 android:title=／android:text= 裡正好等於該英文的屬性，避免誤傷
            pat = re.compile(r'(android:(?:title|text))=' + re.escape(old))
            n = len(pat.findall(s))
            if n == 0:
                print(f'  ！{rel} 中找不到 {key} 的寫死字串 {literal!r}')
                continue
            s2 = pat.sub(lambda m: m.group(1) + '=' + new, s)
            open(p, 'w', encoding='utf-8').write(s2)
            done.setdefault(rel, []).append((key, n))
    for rel, xs in sorted(done.items()):
        print(f'  {rel}: ' + ', '.join(f'{k}×{n}' for k, n in xs))


def main():
    if os.path.exists(os.path.join(RES, 'xml/preferences.xml.bak')):
        print('已經轉換過了，重跑請先從新的 lithiumpatch 輸出重新解包。')
        sys.exit(1)
    add_strings()
    rewrite_refs()
    json.dump({k: v[0] for k, v in NEW.items()},
              open(os.path.join(BASE, 'patch-strings.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'\n新增 {len(NEW)} 個字串資源並改寫引用完成。')


if __name__ == '__main__':
    main()
