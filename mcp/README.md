# pypandoc-hwpx MCP 서버

[pypandoc-hwpx](../README.md)를 활용하여 `.docx` 문서를 `.hwpx` 문서로 변환하는 도구를 제공하는 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 서버입니다.

## 요구 사항

- Python 3.12+
- 시스템에 [Pandoc](https://pandoc.org/)이 설치되어 있어야 합니다
- [uv](https://docs.astral.sh/uv/) 패키지 매니저
- [Docker Desktop](https://docs.docker.com/desktop/) 또는 동등한 컨테이너 런타임

## 설치

```bash
cd mcp
uv sync
```

## 서버 실행 (VS Code 기준)

### `stdio` 전송 (기본값)

1. MCP 서버 설정을 복사합니다.

    ```bash
    mkdir -p .vscode
    cp mcp/.vscode/mcp.local.stdio.json .vscode/mcp.json
    ```

1. MCP 서버를 실행합니다.

### Streamable HTTP 전송

1. MCP 서버를 실행합니다.

    ```bash
    cd mcp
    uv run server.py --http --port 8000
    ```

   > 포트 번호는 원하는 값으로 설정할 수 있습니다.

1. MCP 서버 설정을 복사합니다.

    ```bash
    mkdir -p .vscode
    cp mcp/.vscode/mcp.local.http.json .vscode/mcp.json
    ```

1. MCP 서버를 실행합니다.

### 컨테이너 내 `stdio` 전송

1. 컨테이너 이미지를 빌드합니다.

    ```bash
    docker build -f Dockerfile -t pypandoc-hwpx-mcp:latest .
    ```

1. MCP 서버 설정을 복사합니다.

    ```bash
    mkdir -p .vscode
    cp mcp/.vscode/mcp.container.stdio.json .vscode/mcp.json
    ```

1. MCP 서버를 실행합니다.

### 컨테이너 내 Streamable HTTP 전송

1. 컨테이너 이미지를 빌드합니다.

    ```bash
    docker build -f Dockerfile -t pypandoc-hwpx-mcp:latest .
    ```

1. MCP 서버를 실행합니다.

    ```bash
    docker run -i --rm -p 8000:8000 -v $HOME:$HOME pypandoc-hwpx-mcp:latest --http --port 8000
    ```

   > 포트 번호는 원하는 값으로 설정할 수 있습니다.

1. MCP 서버 설정을 복사합니다.

    ```bash
    mkdir -p .vscode
    cp mcp/.vscode/mcp.container.http.json .vscode/mcp.json
    ```

1. MCP 서버를 실행합니다.

## 제공 도구

| 도구           | 설명                                                  |
|----------------|-------------------------------------------------------|
| `docx_to_hwpx` | 워드(`.docx`) 파일을 아래아 한글(`.hwpx`) 파일로 변환 |
| `html_to_hwpx` | HTML 파일을 아래아 한글(`.hwpx`) 파일로 변환          |
| `md_to_hwpx`   | 마크다운 파일을 아래아 한글(`.hwpx`) 파일로 변환      |

### 도구 매개변수

세 도구 모두 동일한 매개변수를 사용합니다:

| 매개변수         | 타입   | 필수 여부 | 설명                                                                               |
|------------------|--------|-----------|------------------------------------------------------------------------------------|
| `input_path`     | string | 예        | 원본 파일 경로                                                                     |
| `output_path`    | string | 예        | `.hwpx` 출력 파일이 저장될 경로                                                    |
| `reference_hwpx` | string | 아니오    | 스타일 참조용 `.hwpx` 파일 경로 (지정하지 않으면 내장된 `blank.hwpx`를 사용합니다) |
