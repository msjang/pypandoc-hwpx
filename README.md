# pypandoc-hwpx

**pypandoc-hwpx**는 Pandoc AST를 사이에 두고 아래아 한글(`.hwpx`)과 다른 문서 형식을 변환합니다.

- 워드(`.docx`), 마크다운(`.md`), HTML 등 → `.hwpx`
- `.hwpx` → Pandoc JSON AST → `.md`, `.docx`, `.html`, `.pdf`, `.txt` 등

## 주요 기능

- **입력 형식**: [Pandoc](https://pandoc.org)이 지원하는 모든 문서형식 - 워드(`.docx`), 마크다운(`.md`), HTML(`.html`, `.htm`) 등
- **출력 형식**: 아래아 한글문서(`.hwpx`)
- **이미지 처리**: 로컬 이미지를 참조하는 HTML이나 마크다운의 경우 이미지를 포함하여 hwpx 생성
- **고급 레이아웃**:
    - 워드나 HTML의 셀 병합(rowspan/colspan)이 포함된 복잡한 표를 지원합니다.
    - 참조용 HWPX 파일(`blank.hwpx`)의 스타일과 페이지 설정(여백 등)을 복제하여 사용합니다.

## 요구 사항

- **Python 3.6+**
- **Pandoc**: 시스템에 [Pandoc](https://pandoc.org)이 설치되어 있어야 합니다.
- **Python 라이브러리**: Pandoc의 파이썬 래퍼인 pypandoc 이 필요합니다.

## 설치

### PyPI 설치 (권장)

```bash
pip install pypandoc-hwpx
```

### 소스 설치

```bash
git clone https://github.com/msjang/pypandoc-hwpx.git
cd pypandoc-hwpx
pip install -e .
```

## 사용방법

커맨드 라인 도구(`pypandoc-hwpx`)를 사용하여 변환합니다.

```sh
# DOCX -> HWPX
pypandoc-hwpx test.docx --reference-doc=custom.hwpx -o test-from-docx.hwpx

# HTML -> HWPX
pypandoc-hwpx test.html --reference-doc=custom.hwpx -o test-from-html.hwpx

# MD -> HWPX
pypandoc-hwpx test.md   --reference-doc=custom.hwpx -o test-from-md.hwpx

# JSON AST -> HWPX
pypandoc-hwpx test.json --reference-doc=custom.hwpx -o test-from-json.hwpx
```

* `--reference-doc`: (선택) 스타일(글자 모양, 문단 모양, 용지 설정 등)을 가져올 기준 HWPX 파일. 지정하지 않으면 패키지에 내장된 기본 파일(`blank.hwpx`)을 사용합니다.

HWPX를 다른 형식으로 보낼 때는, 패키지를 Pandoc JSON AST로 읽은 뒤 그 JSON을 위와 같은 기존 변환 경로에 넘깁니다.

```sh
# HWPX -> Markdown / DOCX / HTML / plain text / JSON AST
pypandoc-hwpx test.hwpx -o test.md
pypandoc-hwpx test.hwpx -o test.docx
pypandoc-hwpx test.hwpx -o test.html
pypandoc-hwpx test.hwpx -o test.txt
pypandoc-hwpx test.hwpx -o test.json
```

`-o`를 생략하면 결과를 stdout으로 보냅니다. 형식을 지정하지 않으면 `plain`입니다. `-t`는 Pandoc의 `-t`와 같이 출력 형식을 고릅니다. `hwpx`, `docx`, `pdf`처럼 바이너리 형식은 `-o`가 필요합니다.

```sh
pypandoc-hwpx test.hwpx -t plain
pypandoc-hwpx test.hwpx -t markdown | head
pypandoc-hwpx test.hwpx -t json > test.json

# Pandoc에 넘길 옵션은 -- 뒤에 둡니다.
pypandoc-hwpx test.hwpx -t pdf -o test.pdf -- --pdf-engine=xelatex -H header.tex
pypandoc-hwpx test.hwpx -t latex -- --toc -V documentclass=article
```

`-o`로 파일을 만들 때 이미지는 출력 파일 옆 `{이름}_media/`에 풀립니다. stdout으로 보낼 때는 그 파일을 남기지 않습니다. AST가 담지 못하는 서식(장평, 자간, 글꼴 등)과 코드 블록처럼 HWPX에 구분 정보가 없는 구조는 왕복에서 사라집니다.

## 설명 및 제약사항

[Pandoc](https://pandoc.org)은 문서를 내부적으로 [JSON AST(Abstract Syntax Tree)](https://pandoc.org/using-the-pandoc-api.html) 형식으로 변환한 뒤, 이를 대상 포맷으로 다시 변환하는 방식을 사용합니다. 여러 문서 형식을 아우르기 위해, AST는 공통적으로 지원 가능한 최소한의 서식 정보만을 포함합니다.

**pypandoc-hwpx**는 이 과정을 활용하여 워드(`.docx`), 마크다운(`.md`), HTML(`.html`,`.htm`) 등의 문서를 AST로 변환하고, 이를 다시 아래아 한글(`.hwpx`) 규격에 맞춰 생성합니다. 따라서 AST가 표현하지 못하는 복잡한 서식(장평, 자간, 정교한 스타일 등)은 변환 과정에서 제외될 수 있습니다.

디버깅 및 개발 편의를 위해 중간 단계인 JSON AST 변환과 HTML 변환 기능도 제공합니다.

```sh
# 디버깅용 JSON 출력
pypandoc-hwpx test.docx -o test-from-docx.json

# 확인용 HTML 출력
pypandoc-hwpx test.docx -o test-from-docx.html
```

## 예제 (Examples)

프로젝트 내 `tests/` 디렉토리에서 변환된 결과물(`*.hwpx`, `*.html`)과 원본 테스트 파일들을 확인할 수 있습니다.

## 프로젝트 구조

- `pypandoc_hwpx/cli.py`: 메인 실행 스크립트. `.hwpx` 입력이면 AST JSON을 만든 뒤 기존 출력 경로에 넘깁니다.
- `pypandoc_hwpx/PandocToHwpx.py`: AST → HWPX (XML 생성, Zip 처리).
- `pypandoc_hwpx/HwpxToPandoc.py`: HWPX → AST. `header.xml`의 스타일·개요·번호 매핑과 `section*.xml` 본문을 읽어 Pandoc JSON을 만듭니다.
- `pypandoc_hwpx/PandocToHtml.py`: HTML 변환 핵심 로직 (이미지 추출, HTML 템플릿).
- `pypandoc_hwpx/blank.hwpx`: HWPX 변환에 필수적인 참조용 템플릿 파일.
    - *참고: Mac용 Word 16.73에서 생성한 DOCX를 Mac용 한글 12.30.0에서 HWPX로 변환한 뒤, XML을 수동 최적화하여 제작했습니다.*

## 라이선스 (License)

MIT License. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
