"""Read an HWPX package into a Pandoc JSON AST.

PandocToHwpx builds XML strings and cannot run backwards. This module walks
the HWPX zip instead: header.xml for style, numbering, and outline maps;
Contents/section*.xml for the body; BinData/ for images.
"""

import json
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

_LUNIT_PER_MM = 283.465
_NUM_STYLE = {
    'DIGIT': 'Decimal',
    'LATIN_SMALL': 'LowerAlpha',
    'LATIN_CAPITAL': 'UpperAlpha',
    'ROMAN_SMALL': 'LowerRoman',
    'ROMAN_CAPITAL': 'UpperRoman',
}


def _local(tag):
    if not tag:
        return ''
    return tag.rsplit('}', 1)[-1]


def _children(el, name):
    return [child for child in list(el) if _local(child.tag) == name]


def _child(el, name):
    for child in list(el):
        if _local(child.tag) == name:
            return child
    return None


def _as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _norm_color(value):
    if not value:
        return None
    text = value.strip().lower()
    if text in ('none', 'auto', ''):
        return None
    if not text.startswith('#'):
        text = '#' + text
    if len(text) == 4:
        text = '#' + ''.join(ch * 2 for ch in text[1:])
    return text.upper()


def _attr():
    return ["", [], []]


def text_to_inlines(text):
    inlines = []
    buf = []

    def flush():
        if buf:
            inlines.append({"t": "Str", "c": ''.join(buf)})
            buf.clear()

    for ch in text or '':
        if ch == ' ':
            flush()
            inlines.append({"t": "Space"})
        elif ch == '\n':
            flush()
            inlines.append({"t": "LineBreak"})
        elif ch == '\t':
            flush()
            inlines.extend([{"t": "Space"}] * 4)
        elif ch == '\r':
            continue
        else:
            buf.append(ch)
    flush()
    return inlines


def _pandoc_api_version():
    try:
        raw = subprocess.check_output(
            ['pandoc', '-t', 'json'],
            input=b'',
            stderr=subprocess.DEVNULL,
        )
        return json.loads(raw.decode('utf-8'))['pandoc-api-version']
    except Exception:
        return [1, 23, 1]


class _InlineAcc:
    """Collect inlines, including hyperlinks that open and close across runs."""

    def __init__(self):
        self.top = []
        self.stack = []

    def _target(self):
        if self.stack:
            return self.stack[-1]['inlines']
        return self.top

    def add(self, inlines):
        if inlines:
            self._target().extend(inlines)

    def begin(self, url):
        # url is None for a field that should pass its inner text through.
        self.stack.append({'url': url, 'inlines': []})

    def end(self):
        if not self.stack:
            return
        frame = self.stack.pop()
        inner = frame['inlines']
        if frame['url'] is None:
            self.add(inner)
        else:
            self.add([{"t": "Link", "c": [_attr(), inner, [frame['url'], ""]]}])

    def close_all(self):
        while self.stack:
            self.end()

    @property
    def in_link(self):
        return bool(self.stack) and self.stack[-1]['url'] is not None


class HwpxToPandoc:
    def __init__(self, hwpx_path, media_dir, media_dirname):
        self.hwpx_path = hwpx_path
        self.media_dir = media_dir
        self.media_dirname = media_dirname
        self.para_heads = {}
        self.numberings = {}
        self.styles = {}
        self.char_props = {}
        self.manifest = {}
        self.title = None
        self._images = {}
        self.zf = None
        self.names = set()

    @staticmethod
    def write_json(hwpx_path, json_path, media_dirname=None):
        json_path = os.path.abspath(json_path)
        json_dir = os.path.dirname(json_path) or os.getcwd()
        if not media_dirname:
            stem = os.path.splitext(os.path.basename(json_path))[0]
            media_dirname = stem + '_media'
        reader = HwpxToPandoc(
            hwpx_path,
            os.path.join(json_dir, media_dirname),
            media_dirname,
        )
        ast = reader.build()
        os.makedirs(json_dir, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as handle:
            json.dump(ast, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
        if os.path.isdir(reader.media_dir) and not os.listdir(reader.media_dir):
            os.rmdir(reader.media_dir)
        return ast

    def build(self):
        if not os.path.exists(self.hwpx_path):
            raise FileNotFoundError(f"HWPX file not found: {self.hwpx_path}")
        try:
            zip_file = zipfile.ZipFile(self.hwpx_path)
        except zipfile.BadZipFile as exc:
            raise ValueError(f"Not a valid HWPX (zip) file: {self.hwpx_path}") from exc

        with zip_file as zf:
            self.zf = zf
            self.names = set(zf.namelist())
            self._load_header()
            self._load_package_meta()
            sections = self._section_names()
            if not sections:
                raise ValueError(f"No Contents/section*.xml in {self.hwpx_path}")
            blocks = []
            for name in sections:
                root = ET.fromstring(zf.read(name))
                blocks.extend(self._blocks_from_container(root))

        meta = {}
        if self.title:
            meta['title'] = {"t": "MetaInlines", "c": text_to_inlines(self.title)}
        return {
            "pandoc-api-version": _pandoc_api_version(),
            "meta": meta,
            "blocks": blocks,
        }

    def _load_header(self):
        if "Contents/header.xml" not in self.names:
            return
        root = ET.fromstring(self.zf.read("Contents/header.xml"))
        for el in root.iter():
            name = _local(el.tag)
            if name == 'charPr' and el.get('id') is not None:
                self.char_props[el.get('id')] = self._read_char_pr(el)
            elif name == 'paraPr' and el.get('id') is not None:
                heads = []
                for heading in _children(el, 'heading'):
                    heads.append({
                        'type': (heading.get('type') or 'NONE').upper(),
                        'level': _as_int(heading.get('level'), 0),
                        'idRef': heading.get('idRef') or '0',
                    })
                self.para_heads[el.get('id')] = heads
            elif name == 'numbering' and el.get('id') is not None:
                heads = []
                for para_head in _children(el, 'paraHead'):
                    heads.append({
                        'level': _as_int(para_head.get('level'), 1),
                        'numFormat': para_head.get('numFormat') or '',
                        'text': ''.join(para_head.itertext()),
                        'start': para_head.get('start'),
                    })
                self.numberings[el.get('id')] = {
                    'start': el.get('start'),
                    'heads': heads,
                }
            elif name == 'style' and el.get('id') is not None:
                self.styles[el.get('id')] = {
                    'charPr': el.get('charPrIDRef') or '0',
                    'name': el.get('name') or '',
                    'engName': el.get('engName') or '',
                }

    def _read_char_pr(self, el):
        flags = set()
        for child in list(el):
            name = _local(child.tag)
            marker = (child.get('type') or child.get('shape') or '').upper()
            if name == 'bold' and marker != 'NONE':
                flags.add('bold')
            elif name == 'italic' and marker != 'NONE':
                flags.add('italic')
            elif name == 'underline' and marker not in ('', 'NONE'):
                flags.add('underline')
            elif name == 'supscript' and marker != 'NONE':
                flags.add('superscript')
            elif name == 'subscript' and marker != 'NONE':
                flags.add('subscript')
        color = None
        for child in list(el):
            if _local(child.tag) == 'textColor':
                color = _norm_color(child.get('value'))
        if color is None:
            color = _norm_color(el.get('textColor'))
        return {'flags': flags, 'color': color}

    def _load_package_meta(self):
        if "Contents/content.hpf" not in self.names:
            return
        root = ET.fromstring(self.zf.read("Contents/content.hpf"))
        for el in root.iter():
            name = _local(el.tag)
            if name == 'title' and not self.title:
                text = ''.join(el.itertext()).strip()
                if text:
                    self.title = text
            elif name == 'item':
                item_id = el.get('id')
                href = el.get('href')
                if item_id and href:
                    self.manifest[item_id] = href

    def _section_names(self):
        found = []
        for name in self.names:
            match = re.fullmatch(r'Contents/section(\d+)\.xml', name)
            if match:
                found.append((int(match.group(1)), name))
        found.sort()
        return [name for _, name in found]

    def _winning_head(self, para_pr_id):
        heads = self.para_heads.get(str(para_pr_id), [])
        for kind in ('NUMBER', 'OUTLINE'):
            for head in heads:
                if head['type'] == kind:
                    return head
        return {'type': 'NONE', 'level': 0, 'idRef': '0'}

    def _header_level_from_style(self, style_id):
        style = self.styles.get(str(style_id or ''))
        if not style:
            return None
        label = f"{style.get('engName', '')} {style.get('name', '')}"
        match = re.search(r'(?:heading|제목)\s*(\d+)', label, re.IGNORECASE)
        if not match:
            return None
        return _as_int(match.group(1), 1)

    def _role(self, paragraph):
        head = self._winning_head(paragraph.get('paraPrIDRef'))
        if head['type'] == 'NUMBER':
            level = head['level']
            num_id = str(head['idRef'])
            return {
                'kind': 'list',
                'level': level,
                'num_id': num_id,
                'bullet': self._is_bullet(num_id, level),
            }
        if head['type'] == 'OUTLINE':
            # blank.hwpx stores 제목 1 as outline level 0.
            return {'kind': 'header', 'header_level': head['level'] + 1}
        named = self._header_level_from_style(paragraph.get('styleIDRef'))
        if named:
            return {'kind': 'header', 'header_level': named}
        return {'kind': 'para'}

    def _para_head(self, num_id, level):
        numbering = self.numberings.get(str(num_id))
        if not numbering:
            return {}
        want = level + 1  # paraHead levels in the template are 1-based
        for head in numbering['heads']:
            if head['level'] == want:
                return head
        if numbering['heads']:
            return numbering['heads'][0]
        return {}

    def _is_bullet(self, num_id, level):
        text = (self._para_head(num_id, level).get('text') or '').strip()
        if not text or '^' in text:
            return False
        return not any(ch.isdigit() for ch in text)

    def _ordered_spec(self, num_id, level):
        numbering = self.numberings.get(str(num_id), {})
        start = _as_int(numbering.get('start'), 1)
        if start < 1:
            start = 1
        head = self._para_head(num_id, level)
        style = _NUM_STYLE.get(head.get('numFormat') or '', 'Decimal')
        text = (head.get('text') or '').strip()
        if '(' in text and text.endswith(')'):
            delim = 'TwoParens'
        elif text.endswith(')'):
            delim = 'OneParen'
        else:
            delim = 'Period'
        return start, style, delim

    def _base_char_id(self, paragraph):
        style = self.styles.get(str(paragraph.get('styleIDRef') or ''))
        if not style:
            return '0'
        return str(style.get('charPr') or '0')

    def _extra_flags(self, char_id, base_id, in_link):
        if str(char_id) == str(base_id):
            return set()
        current = self.char_props.get(str(char_id), {}).get('flags', set())
        base = self.char_props.get(str(base_id), {}).get('flags', set())
        flags = set(current) - set(base)
        # The HWPX writer paints link text blue and underlined. Those marks
        # are link chrome, not separate AST inlines.
        if in_link:
            flags.discard('underline')
        return flags

    def _wrap(self, inlines, flags):
        if not inlines or not flags:
            return inlines
        if 'subscript' in flags:
            inlines = [{"t": "Subscript", "c": inlines}]
        elif 'superscript' in flags:
            inlines = [{"t": "Superscript", "c": inlines}]
        if 'underline' in flags:
            inlines = [{"t": "Underline", "c": inlines}]
        if 'italic' in flags:
            inlines = [{"t": "Emph", "c": inlines}]
        if 'bold' in flags:
            inlines = [{"t": "Strong", "c": inlines}]
        return inlines

    def _blocks_from_container(self, container):
        if container is None:
            return []
        paragraphs = _children(container, 'p')
        return self._blocks_from_paragraphs(paragraphs)

    def _blocks_from_paragraphs(self, paragraphs):
        blocks = []
        index = 0
        while index < len(paragraphs):
            role = self._role(paragraphs[index])
            if role['kind'] == 'list':
                block, index = self._consume_list(paragraphs, index, role['level'])
                blocks.append(block)
            else:
                blocks.extend(self._paragraph_blocks(paragraphs[index], role))
                index += 1
        return blocks

    def _consume_list(self, paragraphs, index, base_level):
        role = self._role(paragraphs[index])
        num_id = role['num_id']
        bullet = role['bullet']
        items = []
        while index < len(paragraphs):
            role = self._role(paragraphs[index])
            if role['kind'] != 'list' or role['level'] < base_level:
                break
            if role['level'] == base_level and role['num_id'] != num_id:
                break
            if role['level'] > base_level:
                break
            item_blocks = self._paragraph_blocks(paragraphs[index], {'kind': 'para'})
            index += 1
            while index < len(paragraphs):
                nested_role = self._role(paragraphs[index])
                if nested_role['kind'] == 'list' and nested_role['level'] > base_level:
                    nested, index = self._consume_list(paragraphs, index, nested_role['level'])
                    item_blocks.append(nested)
                else:
                    break
            if not item_blocks:
                item_blocks = [{"t": "Para", "c": []}]
            items.append(item_blocks)
        if bullet:
            return {"t": "BulletList", "c": items}, index
        start, style, delim = self._ordered_spec(num_id, base_level)
        return {
            "t": "OrderedList",
            "c": [[start, {"t": style}, {"t": delim}], items],
        }, index

    def _paragraph_blocks(self, paragraph, role):
        acc = _InlineAcc()
        base_id = self._base_char_id(paragraph)
        chunks = []
        buf = []
        buf_flags = None

        def flush_buf():
            nonlocal buf_flags
            if not buf:
                return
            acc.add(self._wrap(buf[:], buf_flags or set()))
            buf.clear()
            buf_flags = None

        def push_text(inlines, flags):
            nonlocal buf_flags
            if not inlines:
                return
            frozen = frozenset(flags)
            if buf and frozen != buf_flags:
                flush_buf()
            if not buf:
                buf_flags = frozen
            buf.extend(inlines)

        for run in _children(paragraph, 'run'):
            char_id = run.get('charPrIDRef') or '0'
            flags = self._extra_flags(char_id, base_id, acc.in_link)
            for child in list(run):
                name = _local(child.tag)
                if name in ('secPr', 'linesegarray'):
                    continue
                if name == 'tbl':
                    flush_buf()
                    if not acc.stack and acc.top:
                        chunks.append(('inlines', acc.top))
                        acc.top = []
                    chunks.append(('block', self._table(child)))
                elif name == 't':
                    push_text(self._t_inlines(child), flags)
                elif name == 'tab':
                    push_text([{"t": "Space"}], flags)
                elif name == 'pic':
                    flush_buf()
                    acc.add(self._wrap(self._image_inline(child), flags))
                elif name == 'equation':
                    flush_buf()
                    script = self._equation_script(child)
                    if script:
                        acc.add([{"t": "Code", "c": [_attr(), script]}])
                elif name == 'ctrl':
                    flush_buf()
                    self._apply_ctrl(child, acc)
        flush_buf()
        acc.close_all()
        if acc.top:
            chunks.append(('inlines', acc.top))
        return self._chunks_to_blocks(chunks, role)

    def _chunks_to_blocks(self, chunks, role):
        blocks = []
        used_header = False
        for kind, payload in chunks:
            if kind == 'block':
                blocks.append(payload)
                continue
            if role.get('kind') == 'header' and not used_header:
                level = role.get('header_level') or 1
                blocks.append({"t": "Header", "c": [level, _attr(), payload]})
                used_header = True
            else:
                blocks.append({"t": "Para", "c": payload})
        return blocks

    def _t_inlines(self, el):
        inlines = []
        if el.text:
            inlines.extend(text_to_inlines(el.text))
        for child in list(el):
            name = _local(child.tag)
            if name == 'lineBreak':
                inlines.append({"t": "LineBreak"})
            elif name == 'tab':
                inlines.append({"t": "Space"})
            if child.tail:
                inlines.extend(text_to_inlines(child.tail))
        return inlines

    def _apply_ctrl(self, ctrl, acc):
        for child in list(ctrl):
            name = _local(child.tag)
            if name == 'fieldBegin':
                if (child.get('type') or '').upper() == 'HYPERLINK':
                    acc.begin(self._field_url(child))
                else:
                    acc.begin(None)
            elif name == 'fieldEnd':
                acc.end()
            elif name in ('footNote', 'endNote'):
                sub = _child(child, 'subList')
                note_blocks = self._blocks_from_container(sub) if sub is not None else []
                if not note_blocks:
                    note_blocks = [{"t": "Para", "c": []}]
                acc.add([{"t": "Note", "c": note_blocks}])

    def _field_url(self, field):
        path = None
        command = None
        for el in field.iter():
            if _local(el.tag) != 'stringParam':
                continue
            value = ''.join(el.itertext())
            if el.get('name') == 'Path':
                path = value
            elif el.get('name') == 'Command':
                command = value
        if path:
            return path
        if not command:
            return ''
        command = re.sub(r';\d+;\d+;-?\d+;?\s*$', '', command)
        return command.replace(r'\:', ':').replace(r'\?', '?')

    def _equation_script(self, equation):
        parts = []
        for el in equation.iter():
            if _local(el.tag) == 'script':
                parts.append(''.join(el.itertext()))
        return ''.join(parts).strip()

    def _image_inline(self, pic):
        img_el = None
        for el in pic.iter():
            if _local(el.tag) == 'img':
                img_el = el
                break
        if img_el is None:
            return []
        bin_id = img_el.get('binaryItemIDRef') or 'image'
        path = self._extract_image(bin_id)
        pairs = []
        org = _child(pic, 'orgSz')
        if org is not None:
            width = self._hwp_mm(org.get('width'))
            height = self._hwp_mm(org.get('height'))
            if width:
                pairs.append(["width", f"{width:.2f}mm"])
            if height:
                pairs.append(["height", f"{height:.2f}mm"])
        return [{"t": "Image", "c": [["", [], pairs], [], [path, ""]]}]

    def _hwp_mm(self, value):
        number = _as_int(value, 0)
        if number <= 0:
            return None
        return number / _LUNIT_PER_MM

    def _extract_image(self, bin_id):
        if bin_id in self._images:
            return self._images[bin_id]
        href = self.manifest.get(bin_id)
        candidates = []
        if href:
            href = href.lstrip('/')
            candidates.append(href)
            candidates.append('BinData/' + os.path.basename(href))
        for name in self.names:
            stem = os.path.splitext(os.path.basename(name))[0]
            if stem == bin_id and 'BinData/' in name:
                candidates.append(name)
        data = None
        ext = '.bin'
        for cand in candidates:
            if cand in self.names:
                data = self.zf.read(cand)
                ext = os.path.splitext(cand)[1] or ext
                break
        safe = re.sub(r'[^A-Za-z0-9._-]+', '_', bin_id) or 'image'
        filename = safe + ext
        rel = self.media_dirname + '/' + filename
        if data is None:
            print(f"[Warn] Image not found in HWPX: {bin_id}", file=sys.stderr)
        else:
            os.makedirs(self.media_dir, exist_ok=True)
            with open(os.path.join(self.media_dir, filename), 'wb') as handle:
                handle.write(data)
        self._images[bin_id] = rel
        return rel

    def _table(self, tbl):
        origins = {}
        max_row = 0
        max_col = 0
        for tr in _children(tbl, 'tr'):
            for tc in _children(tr, 'tc'):
                addr = _child(tc, 'cellAddr')
                span = _child(tc, 'cellSpan')
                size = _child(tc, 'cellSz')
                row = _as_int(addr.get('rowAddr') if addr is not None else 0, 0)
                col = _as_int(addr.get('colAddr') if addr is not None else 0, 0)
                row_span = _as_int(span.get('rowSpan') if span is not None else 1, 1) or 1
                col_span = _as_int(span.get('colSpan') if span is not None else 1, 1) or 1
                origins[(row, col)] = {
                    'tc': tc,
                    'row_span': row_span,
                    'col_span': col_span,
                    'header': tc.get('header') == '1',
                    'width': _as_int(size.get('width') if size is not None else 0, 0),
                }
                max_row = max(max_row, row + row_span)
                max_col = max(max_col, col + col_span)

        row_cnt = _as_int(tbl.get('rowCnt'), 0) or max_row
        col_cnt = _as_int(tbl.get('colCnt'), 0) or max_col
        if row_cnt <= 0 or col_cnt <= 0:
            return {"t": "Para", "c": []}

        covered = set()
        for (row, col), info in origins.items():
            for rr in range(info['row_span']):
                for cc in range(info['col_span']):
                    covered.add((row + rr, col + cc))

        rows = []
        header_flags = []
        for row in range(row_cnt):
            cells = []
            flags = []
            col = 0
            while col < col_cnt:
                if (row, col) not in origins:
                    if (row, col) in covered:
                        col += 1
                        continue
                    cells.append(self._empty_cell())
                    flags.append(False)
                    col += 1
                    continue
                info = origins[(row, col)]
                cells.append(self._cell_json(info))
                flags.append(info['header'])
                col += info['col_span']
            rows.append([_attr(), cells])
            header_flags.append(bool(flags) and all(flags))

        head_count = 0
        for flag in header_flags:
            if not flag:
                break
            head_count += 1
        head_rows = rows[:head_count]
        body_rows = rows[head_count:]

        widths = [0] * col_cnt
        for (row, col), info in origins.items():
            if row != 0 or info['width'] <= 0:
                continue
            share = info['width'] / float(info['col_span'])
            for offset in range(info['col_span']):
                if col + offset < col_cnt:
                    widths[col + offset] = share
        if widths and all(width > 0 for width in widths):
            total = sum(widths)
            colspecs = [
                [{"t": "AlignDefault"}, {"t": "ColWidth", "c": widths[i] / total}]
                for i in range(col_cnt)
            ]
        else:
            colspecs = [
                [{"t": "AlignDefault"}, {"t": "ColWidthDefault"}]
                for _ in range(col_cnt)
            ]

        return {
            "t": "Table",
            "c": [
                _attr(),
                [None, []],
                colspecs,
                [_attr(), head_rows],
                [[_attr(), 0, [], body_rows]],
                [_attr(), []],
            ],
        }

    def _cell_json(self, info):
        sub = _child(info['tc'], 'subList')
        blocks = self._blocks_from_container(sub) if sub is not None else []
        if len(blocks) == 1 and blocks[0].get('t') == 'Para':
            blocks = [{"t": "Plain", "c": blocks[0].get('c') or []}]
        elif not blocks:
            blocks = [{"t": "Plain", "c": []}]
        return [
            _attr(),
            {"t": "AlignDefault"},
            info['row_span'],
            info['col_span'],
            blocks,
        ]

    def _empty_cell(self):
        return [_attr(), {"t": "AlignDefault"}, 1, 1, [{"t": "Plain", "c": []}]]
