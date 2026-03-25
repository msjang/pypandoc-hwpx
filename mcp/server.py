import argparse
import json
import os
import sys
import tempfile

import pypandoc
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Resolve the reference HWPX file bundled with pypandoc-hwpx.
# ---------------------------------------------------------------------------
_PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BLANK_HWPX = os.path.join(_PACKAGE_ROOT, "pypandoc_hwpx", "blank.hwpx")

# Add the parent package to sys.path so that pypandoc_hwpx can be imported.
if _PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, _PACKAGE_ROOT)

from pypandoc_hwpx.PandocToHwpx import PandocToHwpx  # noqa: E402

# ---------------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------------
mcp = FastMCP("pypandoc-hwpx")


def _resolve_reference(reference_hwpx: str | None = None) -> str:
    """Return the path to the reference HWPX file to use for conversion."""
    if reference_hwpx and os.path.isfile(reference_hwpx):
        return reference_hwpx
    if os.path.isfile(_BLANK_HWPX):
        return _BLANK_HWPX
    raise FileNotFoundError(
        "No reference HWPX file found.  Pass an explicit path via "
        "'reference_hwpx' or ensure 'pypandoc_hwpx/blank.hwpx' exists."
    )


def _convert(input_path: str, output_path: str, reference_hwpx: str | None = None) -> str:
    """Run the conversion and return the absolute output path."""
    ref = _resolve_reference(reference_hwpx)
    PandocToHwpx.convert_to_hwpx(input_path, output_path, ref)
    return os.path.abspath(output_path)


# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------

@mcp.tool()
def docx_to_hwpx(
    input_path: str,
    output_path: str,
    reference_hwpx: str | None = None,
) -> str:
    """Convert a .docx file to a .hwpx file.

    Args:
        input_path: Path to the source .docx file.
        output_path: Path where the resulting .hwpx file will be written.
        reference_hwpx: Optional path to a reference .hwpx file for styles.

    Returns:
        The absolute path of the generated .hwpx file.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    return _convert(input_path, output_path, reference_hwpx)


@mcp.tool()
def html_to_hwpx(
    input_path: str,
    output_path: str,
    reference_hwpx: str | None = None,
) -> str:
    """Convert an HTML file to a .hwpx file.

    Args:
        input_path: Path to the source HTML file.
        output_path: Path where the resulting .hwpx file will be written.
        reference_hwpx: Optional path to a reference .hwpx file for styles.

    Returns:
        The absolute path of the generated .hwpx file.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    return _convert(input_path, output_path, reference_hwpx)


@mcp.tool()
def md_to_hwpx(
    input_path: str,
    output_path: str,
    reference_hwpx: str | None = None,
) -> str:
    """Convert a Markdown file to a .hwpx file.

    Args:
        input_path: Path to the source Markdown (.md) file.
        output_path: Path where the resulting .hwpx file will be written.
        reference_hwpx: Optional path to a reference .hwpx file for styles.

    Returns:
        The absolute path of the generated .hwpx file.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    return _convert(input_path, output_path, reference_hwpx)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="pypandoc-hwpx MCP server")
    parser.add_argument(
        "--http",
        action="store_true",
        default=False,
        help="Run the server using Streamable HTTP transport instead of stdio",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for the Streamable HTTP transport (default: 8000)",
    )
    args = parser.parse_args()

    transport = "streamable-http" if args.http else "stdio"
    kwargs: dict = {"transport": transport}
    if args.http:
        kwargs["host"] = "0.0.0.0"
        kwargs["port"] = args.port
    mcp.run(**kwargs)


if __name__ == "__main__":
    main()
