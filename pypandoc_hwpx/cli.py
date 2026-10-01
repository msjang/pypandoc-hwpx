import argparse
import json
import os
import sys
import tempfile

import pypandoc

from .HwpxToPandoc import HwpxToPandoc
from .PandocToHtml import PandocToHtml
from .PandocToHwpx import PandocToHwpx

# These formats are binary packages. They need -o; stdout would mix badly
# with the writer's own log lines and with a terminal.
_FILE_ONLY_FORMATS = {'hwpx', 'docx', 'pdf', 'epub', 'odt', 'pptx'}

_FORMAT_ALIASES = {
    'txt': 'plain',
    'text': 'plain',
    'md': 'markdown',
    'htm': 'html',
}


def main():
    parser = argparse.ArgumentParser(
        description="Convert documents using custom Pandoc parsers (pypandoc-hwpx)."
    )
    parser.add_argument("input_files", nargs="+", help="Input files")
    parser.add_argument(
        "-o", "--output",
        help="Output file. Omit to write text to stdout.",
    )
    parser.add_argument(
        "-t", "--to",
        help="Output format (plain, markdown, html, json, hwpx, docx, ...). "
             "Defaults to plain on stdout; otherwise taken from the -o extension.",
    )
    parser.add_argument(
        "--reference-doc",
        default=None,
        help="Reference HWPX (default: built-in blank.hwpx)",
    )
    our_argv, pandoc_args = _split_pandoc_passthrough()
    args = parser.parse_args(our_argv)
    fmt = _resolve_format(args.to, args.output)
    if not fmt:
        print("Error: pass -t or an -o path with an extension.", file=sys.stderr)
        sys.exit(1)
    if not args.output and fmt in _FILE_ONLY_FORMATS:
        print(f"Error: format '{fmt}' writes a file. Pass -o.", file=sys.stderr)
        sys.exit(1)

    input_file = args.input_files[0]
    input_ext = os.path.splitext(input_file)[1].lower()

    if input_ext == ".hwpx" and not args.output:
        with tempfile.TemporaryDirectory(prefix="pypandoc-hwpx-") as tmp:
            json_path = os.path.join(tmp, "ast.json")
            HwpxToPandoc.write_json(input_file, json_path, media_dirname="media")
            _convert(json_path, fmt, None, tmp, args.reference_doc, pandoc_args)
        return

    temp_json = None
    resource_dir = None
    try:
        if input_ext == ".hwpx":
            out_dir = os.path.dirname(os.path.abspath(args.output)) or os.getcwd()
            os.makedirs(out_dir, exist_ok=True)
            stem = os.path.splitext(os.path.basename(args.output))[0]
            media_dirname = stem + "_media"
            if fmt == "json":
                if pandoc_args:
                    print("Warning: pandoc arguments are ignored when reading HWPX into JSON.", file=sys.stderr)
                HwpxToPandoc.write_json(input_file, args.output, media_dirname=media_dirname)
                print(f"Successfully created {args.output}")
                return
            fd, temp_json = tempfile.mkstemp(prefix=".", suffix=".json", dir=out_dir)
            os.close(fd)
            HwpxToPandoc.write_json(input_file, temp_json, media_dirname=media_dirname)
            input_file = temp_json
            resource_dir = out_dir

        _convert(input_file, fmt, args.output, resource_dir, args.reference_doc, pandoc_args)
    finally:
        if temp_json and os.path.exists(temp_json):
            os.remove(temp_json)


def _resolve_format(to_arg, output_path):
    if to_arg:
        return _normalize_format(to_arg)
    if output_path:
        ext = os.path.splitext(output_path)[1].lower().lstrip('.')
        if not ext:
            return None
        return _normalize_format(ext)
    return 'plain'


def _normalize_format(fmt):
    fmt = fmt.lower().lstrip('.')
    return _FORMAT_ALIASES.get(fmt, fmt)


def _split_pandoc_passthrough(argv=None):
    """Arguments after a lone -- are forwarded to pandoc unchanged."""
    if argv is None:
        argv = sys.argv[1:]
    if '--' in argv:
        idx = argv.index('--')
        return argv[:idx], argv[idx + 1:]
    return list(argv), []


def _convert(input_file, fmt, output_path, resource_dir, ref_doc, pandoc_args=None):
    pandoc_args = list(pandoc_args or [])
    if fmt == "hwpx":
        if pandoc_args:
            print("Warning: pandoc arguments are ignored for HWPX output.", file=sys.stderr)
        ref_doc = _reference_doc(ref_doc)
        PandocToHwpx.convert_to_hwpx(input_file, output_path, ref_doc)
        return

    # The built-in HTML preview does not accept Pandoc writer options.
    # Any arguments after -- use Pandoc's own HTML writer.
    if fmt == "html" and not pandoc_args:
        _convert_html(input_file, output_path)
        return

    if fmt == "json":
        _convert_json(input_file, output_path, pandoc_args)
        return

    extra = [f"--reference-doc={ref_doc}"] if ref_doc else []
    if resource_dir:
        extra.append(f"--resource-path={resource_dir}")
    extra.extend(pandoc_args)
    if output_path:
        pypandoc.convert_file(input_file, fmt, outputfile=output_path, extra_args=extra)
    else:
        text = pypandoc.convert_file(input_file, fmt, extra_args=extra)
        _write_stdout(text)


def _convert_html(input_file, output_path):
    if output_path:
        PandocToHtml.convert_to_html(input_file, output_path)
        return
    with tempfile.TemporaryDirectory(prefix="pypandoc-hwpx-") as tmp:
        html_path = os.path.join(tmp, "out.html")
        PandocToHtml.convert_to_html(input_file, html_path, announce=False)
        with open(html_path, encoding="utf-8") as handle:
            _write_stdout(handle.read())


def _convert_json(input_file, output_path, pandoc_args=None):
    json_str = pypandoc.convert_file(input_file, 'json', extra_args=pandoc_args or [])
    ast = json.loads(json_str)
    rendered = json.dumps(ast, indent=2, ensure_ascii=False) + "\n"
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as handle:
            handle.write(rendered)
    else:
        sys.stdout.write(rendered)


def _reference_doc(ref_doc):
    if ref_doc:
        return ref_doc
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    default_ref = os.path.join(pkg_dir, "blank.hwpx")
    if os.path.exists(default_ref):
        return default_ref
    print("Error: --reference-doc is required and no default 'blank.hwpx' found in package.", file=sys.stderr)
    sys.exit(1)


def _write_stdout(text):
    if text and not text.endswith("\n"):
        text += "\n"
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
