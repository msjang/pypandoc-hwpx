# pypandoc-hwpx

**pypandoc-hwpx**는 워드(`.docx`), 마크다운(`.md`), HTML(`.html`,`.htm`)을 아래아 한글(`.hwpx`)로 변환해주는 파이썬 도구입니다.

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

## 프로젝트 구조

- `pypandoc_hwpx/cli.py`: 메인 실행 스크립트.
- `pypandoc_hwpx/PandocToHwpx.py`: HWPX 변환 핵심 로직 (AST 파싱, XML 생성, Zip 처리).
- `pypandoc_hwpx/PandocToHtml.py`: HTML 변환 핵심 로직 (이미지 추출, HTML 템플릿).
- `pypandoc_hwpx/blank.hwpx`: HWPX 변환에 필수적인 참조용 템플릿 파일.
    - *참고: Mac용 Word 16.73에서 생성한 DOCX를 Mac용 한글 12.30.0에서 HWPX로 변환한 뒤, XML을 수동 최적화하여 제작했습니다.*

## 라이선스 (License)

MIT License. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
