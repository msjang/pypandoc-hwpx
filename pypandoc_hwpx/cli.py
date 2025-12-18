import argparse
import sys
import pypandoc
import json
import os
import io
import shutil
import zipfile
import xml.etree.ElementTree as ET
from .PandocToHtml import PandocToHtml
from .PandocToHwpx import PandocToHwpx

def main():
    parser = argparse.ArgumentParser(
        description="Convert documents using custom Pandoc Parsers (pypandoc-hwpx)."
    )

    parser.add_argument("input_files", nargs="+", help="Input files")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--reference-doc", required=False, default=None, help="Reference HWPX (default: uses built-in blank.hwpx)")

    args = parser.parse_args()
    input_file = args.input_files[0]
    output_ext = os.path.splitext(args.output)[1].lower()

    # Determine Reference Doc
    ref_doc = args.reference_doc
    if not ref_doc and output_ext == ".hwpx":
        # Check package resource
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        default_ref = os.path.join(pkg_dir, "blank.hwpx")
        if os.path.exists(default_ref):
            ref_doc = default_ref
            # print(f"[Info] Using default reference doc: {ref_doc}")
        else:
             print("Error: --reference-doc is required and no default 'blank.hwpx' found in package.", file=sys.stderr)
             sys.exit(1)

    if output_ext == ".hwpx":
        PandocToHwpx.convert_to_hwpx(input_file, args.output, ref_doc)

    elif output_ext in [".htm", ".html"]:
        PandocToHtml.convert_to_html(input_file, args.output)

    elif output_ext == ".json":
        json_str = pypandoc.convert_file(input_file, 'json')
        json_ast = json.loads(json_str)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(json_ast, f, indent=2, ensure_ascii=False)
            
    else:
        # Native Pandoc Fallback
        extra = [f"--reference-doc={ref_doc}"] if ref_doc else []
        pypandoc.convert_file(input_file, output_ext.strip('.'), outputfile=args.output, extra_args=extra)

if __name__ == "__main__":
    main()