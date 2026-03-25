# pypandoc-hwpx MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that exposes document-to-HWPX conversion tools powered by [pypandoc-hwpx](../README.md).

## Prerequisites

- Python 3.12+
- [Pandoc](https://pandoc.org/) installed on your system
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

```bash
cd mcp
uv sync
```

## Running the Server

### stdio transport (default)

```bash
uv run server.py
```

### Streamable HTTP transport

```bash
uv run server.py --http
```

## Available Tools

| Tool | Description |
|------|-------------|
| `docx_to_hwpx` | Convert a `.docx` file to a `.hwpx` file |
| `html_to_hwpx` | Convert an HTML file to a `.hwpx` file |
| `md_to_hwpx` | Convert a Markdown file to a `.hwpx` file |

### Tool Parameters

All three tools accept the same parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input_path` | string | Yes | Path to the source file |
| `output_path` | string | Yes | Path where the `.hwpx` output will be written |
| `reference_hwpx` | string | No | Path to a reference `.hwpx` file for styles (defaults to built-in `blank.hwpx`) |
