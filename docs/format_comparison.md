# 포멧 비교

마크다운, HTML, DOCX, HWPX의 저장 형식을 비교한 문서이다.

## 1. 메타정보

### 1.1. 마크다운 메타정보

frontmatter 에 yaml 형식으로 저장한다.

```yaml
---
title: 제목
author: 
  - 저자1
  - 저자2
  - 저자3
---
```

### 1.2. DOCX 메타정보

`docProps/core.xml`에 저장한다.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>제목</dc:title>
  <dc:subject>주제</dc:subject>
  <dc:creator>저자1; 저자2; 저자3</dc:creator>
  <cp:keywords>키워드</cp:keywords>
  <dc:description>메모</dc:description>
  <cp:category>범주</cp:category>
</cp:coreProperties>
```

`docProps/core.xml`에서 `cp:coreProperties` 자식의 다음 태그는 삭제해도 무방하다.
- cp:lastModifiedBy 
- cp:revision
- dcterms:created
- dcterms:modified

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>제목</dc:title>
  <dc:subject>주제</dc:subject>
  <dc:creator>저자1; 저자2; 저자3</dc:creator>
  <cp:keywords>키워드</cp:keywords>
  <dc:description>메모</dc:description>
  <cp:lastModifiedBy>msjang</cp:lastModifiedBy>
  <cp:revision>4</cp:revision>
  <dcterms:created xsi:type="dcterms:W3CDTF">2025-12-13T00:18:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2025-12-13T00:32:00Z</dcterms:modified>
  <cp:category>범주</cp:category>
</cp:coreProperties>
```

### 1.3. HWPX 메타정보

`Contents/content.hpf` 에 저장한다.

```xml
<?xml ... ?>
<opf:package ... >
  <opf:metadata>
    <opf:title>제목</opf:title>
    <opf:language>ko</opf:language>
    <opf:meta name="creator" content="text">저자1; 저자2; 저자3</opf:meta>
    <opf:meta name="subject" content="text">주제</opf:meta>
    <opf:meta name="description" content="text">메모</opf:meta>
    <opf:meta name="keyword" content="text">키워드</opf:meta>
  </opf:metadata>
  ...
</opf:package>
```

`opf:metadata` 자식 중에서 다음을 `name` 값으로 가지는 `opf:meta` 태그는 삭제해도 무방하다.
- lastsaveby
- CreatedDate
- ModifiedDate
- date

## 2. 본문과 스타일시트

|      | body                  | stylesheet           |
|------|-----------------------|----------------------|
| HTML | html/body             | html/head/style, css |
| DOCX | word/document.xml     | word/styles.xml      |
| HWPX | Contents/section0.xml | Contents/header.xml  |

<table>
  <tr>
    <td>항목</td>
    <td>HTML</td>
    <td>DOCX</td>
    <td>HWPX</td>
    <td>비고</td>
  </tr>
  <tr>
    <td>문단</td>
    <td>p</td>
    <td>w:p</td>
    <td>hp:p</td>
    <td>p = paragraph, 단락, 문단</td>
  </tr>
  <tr>
    <td>구역</td>
    <td>span</td>
    <td>w:r (run)</td>
    <td>hp:run (run)</td>
    <td>r = run = sequence, 이어지는 문자열, 구역</td>
  </tr>
  <tr>
    <td>텍스트</td>
    <td></td>
    <td>w:t</td>
    <td>hp:t</td>
    <td></td>
  </tr>
  <tr>
    <td>문자속성</td>
    <td>
    </td>
    <td>
      1) run 속성 inline으로 지정<br/>
      2) run 속성 stylesheet로 지정<br/>
      3) p 속성
    </td>
    <td>
      run 속성 stylesheet로 지정
    </td>
    <td>
    </td>
  </tr>
</table>

## 3. 문자서식

### 3.1. 마크다운 문자서식

```
표준 **굵게** *기울임* ***굵고 기울게***
```

### 3.2. HTML 문자서식

#### 3.2.1. 예제 1 (서식태그)

```html
<html>
<body>
  <p>
    표준
    &nbsp;
    <b>굵게</b>
    &nbsp;
    <i>기울임</i>
    &nbsp;
    <u>밑줄</u>
    &nbsp;
    <b><i>굵고 기울임</i></b>
    &nbsp;
    <b><u>굵고 밑줄</u></b>
    &nbsp;
    <i><u>기울고 밑줄</u></i>
  </p>
  <p>
    <sup>표준 윗첨자</sup>
    &nbsp;
    <sup><b>윗첨자 굵게</b></sup>
    &nbsp;
    <sup><b><i>윗첨자 굵고 기울임</i></b></sup>
  </p>
  <p>
    <sub>표준 아래첨자</sub>
    &nbsp;
    <sub><b>아래첨자 굵게</b></sub>
    &nbsp;
    <sub><b><i>아래첨자 굵고 기울임</i></b></sub>
  </p>
  <p>
    <span>표준</span>
    &nbsp;
    <span style="font-size: 15pt;">15pt</span>
    &nbsp;
    <span style="font-size: 20pt;">20pt</span>
  </p>
```

#### 3.2.2. 예제 2 (inline css)

```html
<html>
<body>
  <p>
    <span style="font-weight: normal;">표준</span>
    &nbsp;
    <span style="font-weight: bold;">굵게</span>
    &nbsp;
    <span style="font-style: italic;">기울임</span>
    &nbsp;
    <span style="text-decoration: underline;">밑줄</span>
    &nbsp;
    <span style="font-weight: bold; font-style: italic;">굵고 기울임</span>
    &nbsp;
    <span style="font-weight: bold; text-decoration: underline;">굵고 밑줄</span>
    &nbsp;
    <span style="font-style: italic; text-decoration: underline;">기울고 밑줄</span>
  </p>
  <p>
    <span style="font-weight: normal; vertical-align: super; font-size: smaller;">표준 윗첨자</span>
    &nbsp;
    <span style="font-weight: bold; vertical-align: super; font-size: smaller;">윗첨자 굵게</span>
    &nbsp;
    <span style="font-weight: bold; font-style: italic; vertical-align: super; font-size: smaller;">윗첨자 굵고 기울임</span>
  </p>
  <p>
    <span style="font-weight: normal; vertical-align: sub; font-size: smaller;">표준 아래첨자</span>
    &nbsp;
    <span style="font-weight: bold; vertical-align: sub; font-size: smaller;">아래첨자 굵게</span>
    &nbsp;
    <span style="font-weight: bold; font-style: italic; vertical-align: sub; font-size: smaller;">아래첨자 굵고 기울임</span>
  </p>
  <p>
    <span style="font-weight: normal;">표준</span>
    &nbsp;
    <span style="font-size: 15pt;">15pt</span>
    &nbsp;
    <span style="font-size: 20pt;">20pt</span>
  </p>
</body>
</html>
```

#### 3.2.3. 예제 3 (css stylesheet, 객체에 다중 클래스 적용)

```html
<html>
<head>
  <style>
    .normal { }
    .bold { font-weight: bold; }
    .italic { font-style: italic; }
    .underline { text-decoration: underline; }
    .subscript { vertical-align: sub; font-size: smaller; }
    .superscript { vertical-align: super; font-size: smaller; }
    .pt15 { font-size: 15pt; }
    .pt20 { font-size: 20pt; }
  </style>
</head>
<body>
  <p>
    <span class="normal">표준</span>
    &nbsp;
    <span class="bold">굵게</span>
    &nbsp;
    <span class="italic">기울임</span>
    &nbsp;
    <span class="underline">밑줄</span>
    &nbsp;
    <span class="bold italic">굵고 기울임</span>
    &nbsp;
    <span class="bold underline">굵고 밑줄</span>
    &nbsp;
    <span class="italic underline">기울고 밑줄</span>
  </p>
  <p>
    <span class="normal superscript">표준 윗첨자</span>
    &nbsp;
    <span class="bold superscript">윗첨자 굵게</span>
    &nbsp;
    <span class="bold italic superscript">윗첨자 굵고 기울임</span>
  </p>
  <p>
    <span class="normal subscript">표준 아래첨자</span>
    &nbsp;
    <span class="bold subscript">아래첨자 굵게</span>
    &nbsp;
    <span class="bold italic subscript">아래첨자 굵고 기울임</span>
  </p>
  <p>
    <span class="normal">표준</span>
    &nbsp;
    <span class="pt15">15pt</span>
    &nbsp;
    <span class="pt20">20pt</span>
  </p>
</body>
</html>
```

#### 3.2.4. 예제 4 (css stylesheet, 객체에 단일 클래스 적용)

```html
<html>
<head>
  <style>
    .normal {  }
    .bold { font-weight: bold; }
    .italic { font-style: italic; }
    .underline { text-decoration: underline; }
    .bold-italic { font-weight: bold; font-style: italic; }
    .bold-underline { font-weight: bold; text-decoration: underline; }
    .italic-underline { font-style: italic; text-decoration: underline; }
    .subscript { vertical-align: sub; font-size: smaller; }
    .superscript { vertical-align: super; font-size: smaller; }
    .bold-subscript { font-weight: bold; vertical-align: sub; font-size: smaller; }
    .bold-italic-subscript { font-weight: bold; font-style: italic; vertical-align: sub; font-size: smaller; }
    .bold-superscript { font-weight: bold; vertical-align: super; font-size: smaller; }
    .bold-italic-superscript { font-weight: bold; font-style: italic; vertical-align: super; font-size: smaller; }
    .pt15 { font-size: 15pt; }
    .pt20 { font-size: 20pt; }
  </style>
</head>
<body>
  <p>
    <span class="normal">표준</span>
    &nbsp;
    <span class="bold">굵게</span>
    &nbsp;
    <span class="italic">기울임</span>
    &nbsp;
    <span class="underline">밑줄</span>
    &nbsp;
    <span class="bold-italic">굵고 기울임</span>
    &nbsp;
    <span class="bold-underline">굵고 밑줄</span>
    &nbsp;
    <span class="italic-underline">기울고 밑줄</span>
  </p>
  <p>
    <span class="superscript">표준 윗첨자</span>
    &nbsp;
    <span class="bold-superscript">윗첨자 굵게</span>
    &nbsp;
    <span class="bold-italic-superscript">윗첨자 굵고 기울임</span>
  </p>
  <p>
    <span class="subscript">표준 아래첨자</span>
    &nbsp;
    <span class="bold-subscript">아래첨자 굵게</span>
    &nbsp;
    <span class="bold-italic-subscript">아래첨자 굵고 기울임</span>
  </p>
  <p>
    <span class="normal">표준</span>
    &nbsp;
    <span class="pt15">15pt</span>
    &nbsp;
    <span class="pt20">20pt</span>
  </p>
</body>
</html>
```

### 3.3. DOCX 문자서식

HTML 문자서식 예제 2 (inline css)와 유사하다.

텍스트는  
HTML은 body → p → span 안에 저장하고,  
DOCX은 w:body → w:p → w:r → w:t 안에 저장한다.

크기, 폰트, 굵기 등의 문자속성은  
HTML은 예제 2에서는 span 태그 안에 속성으로 정의한다.  
DOCX는 본 예제에서는 w:r 안의 w:rPr 태그에 w:b, w:i 등의 태그로 정의한다.

공백은  
HTML에서 `&nbsp;`으로 표시하고  
DOCX에서는 `<w:t>`태그에 `xml:space="preserve"`속성을 주고 태그 안에 공백을 허용하여 공백을 나타낸다.

```xml
<!-- word/document.xml -->
<w:document ...>
  <w:body>
    <w:p>
      <w:r>
        <w:t>표준</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:b/><w:bCs/></w:rPr>
        <w:t>굵게</w:t>
      </w:r>
      
      <w:r><w:t xml:space="preserve"> </w:t></w:r>
      
      <w:r>
        <w:rPr><w:i/><w:iCs/></w:rPr>
        <w:t>기울임</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:u w:val="single"/></w:rPr>
        <w:t>밑줄</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:b/><w:bCs/><w:i/><w:iCs/></w:rPr>
        <w:t xml:space="preserve">굵고 기울임</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:b/><w:bCs/><w:u w:val="single"/></w:rPr>
        <w:t xml:space="preserve">굵고 밑줄</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:i/><w:iCs/><w:u w:val="single"/></w:rPr>
        <w:t xml:space="preserve">기울고 밑줄</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
        <w:t xml:space="preserve">표준 윗첨자</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:vertAlign w:val="superscript"/><w:b/><w:bCs/></w:rPr>
        <w:t xml:space="preserve">윗첨자 굵게</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:vertAlign w:val="superscript"/><w:b/><w:bCs/><w:i/><w:iCs/></w:rPr>
        <w:t xml:space="preserve">윗첨자 굵고 기울임</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:rPr><w:vertAlign w:val="subscript"/></w:rPr>
        <w:t xml:space="preserve">표준 아래첨자</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:vertAlign w:val="subscript"/><w:b/><w:bCs/></w:rPr>
        <w:t xml:space="preserve">아래첨자 굵게</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:vertAlign w:val="subscript"/><w:b/><w:bCs/><w:i/><w:iCs/></w:rPr>
        <w:t xml:space="preserve">아래첨자 굵고 기울임</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>표준</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <w:rPr><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr>
        <w:t>15pt</w:t>
      </w:r>

      <w:r><w:t xml:space="preserve"> </w:t></w:r>

      <w:r>
        <!--
          sz  : size    , 영미권 문자 폰트 크기
          szCs: CJK size, 한중일 문자 폰트 크기
        -->
        <w:rPr><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr>
        <w:t>20pt</w:t>
      </w:r>
    </w:p>
```

### 3.4. HWPX 문자서식

HTML 문자서식 예제 4 (css stylesheet, 객체에 단일 클래스 적용)과 유사하다.

텍스트는  
HTML은 body → p → span 안에 저장하고,  
HWPX은 hs:sec → hp:p → hp:run → hp:t 안에 저장한다.

크기, 폰트, 굵기 등의 문자속성은  
HTML은 예제 4에서는 `<span class="bold">`와 같이 span 태그에서 스타일시트를 지정하고, 스타일시트 안에서 속성으로 문자속성을 정의한다.
HWPX은 `<hp:run charPrIDRef="23">`와 같이 hp:run 태그에서 스타일시트를 지정하고, 스타일시트 안에서 `<hh:charPr id="23"`과 같이 동일 id를 같은 속성태그에 문자속성을 정의한다.

DOCX의 경우 바탕글 서식이 적용된 문장의 일부 단어에 bold나 italic을 적용할 때, 서식의 개수가 늘어나지 않는다.

HWPX의 경우 기본서식에 약간의 변형이 일어나기만 해도, 그 변형의 개수만큼 서식의 개수가 늘어난다. 아래의 경우 15개의 서식이 필요하다.

```xml
<!-- Contents/section0.xml -->
<hs:sec ...>
  <hp:p paraPrIDRef="1" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="7" ><hp:t>표준</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="23"><hp:t>굵게</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="8" ><hp:t>기울임</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="24"><hp:t>밑줄</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="25"><hp:t>굵고 기울임</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="26"><hp:t>굵고 밑줄</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="22"><hp:t>기울고 밑줄</hp:t></hp:run>
  </hp:p>
  <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="27"><hp:t>표준 윗첨자</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="28"><hp:t>윗첨자 굵게</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="29"><hp:t>윗첨자 굵고 기울임</hp:t></hp:run>
  </hp:p>
  <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="30"><hp:t>표준 아래첨자</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="31"><hp:t>아래첨자 굵게</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="32"><hp:t>아래첨자 굵고 기울임</hp:t></hp:run>
  </hp:p>
  <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="7" ><hp:t>표준</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="33"><hp:t>15pt</hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="7" ><hp:t> </hp:t></hp:run>
    <hp:run charPrIDRef="34"><hp:t>20pt</hp:t></hp:run>
  </hp:p>
```

```xml
<!-- Contents/header.xml -->
<hh:head ...>
  <hh:refList>
    <hh:fontfaces itemCnt="7">
      <hh:fontface lang="HANGUL" fontCnt="2">
        <hh:font id="0" face="맑은 고딕" type="TTF" isEmbedded="0"/>
        <hh:font id="1" face="함초롬돋움" type="TTF" isEmbedded="0"/>
      </hh:fontface>
      ...
    </hh:fontfaces>
    <hh:charProperties ...>
      ...
      <!-- 바탕글 / Normal -->
      <hh:charPr id="7" height="1000" textColor="#000000" ...>
        <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>
        ...
      </hh:charPr>
      <!-- 바탕글 + 굵게 -->
      <hh:charPr id="23" height="1000" textColor="#000000" ...>
        <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>
        ...
        <hh:bold/>
      </hh:charPr>
      <!-- 바탕글 + 굵고 기울임 -->
      <hh:charPr id="23" height="1000" textColor="#000000" ...>
        <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>
        ...
        <hh:bold/>
        <hh:italic/>
      </hh:charPr>
      ...
```

## 4. 제목단계

### 4.1. 마크다운 제목단계

`#` 개수로 제목단계 깊이 표현한다.

```
# 제목단계
# 제목1단계
## 제목2단계
### 제목3단계
...
본문(바탕글)
```

### 4.2. HTML 제목단계

제목단계를 위한 별도의 태그 h1~h6가 있다. 6단계를 넘어가는 단계는 태그가 없다.

```html
<html>
<body>
  <h1>제목단계</h1>
  <h1>제목1단계</h1>
  <h2>제목2단계</h2>
  <h3>제목3단계</h3>
  ...
  <p>본문(바탕글)</p>
```

### 4.3. DOCX 제목단계

HTML 문자서식 예제 4 (css stylesheet, 객체에 단일 클래스 적용)과 유사하다.

스타일시트는 문단인 w:p에 적용된다. 부분적인 스타일 적용은 run에 inline 방식으로 적용된다.

```xml
<!-- word/document.xml -->
<w:document ... >
  <w:body>
    <w:p><w:pPr><w:pStyle w:val="1" /></w:pPr><w:r><w:t>제목1단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="2" /></w:pPr><w:r><w:t>제목2단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="3" /></w:pPr><w:r><w:t>제목3단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="4" /></w:pPr><w:r><w:t>제목4단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="5" /></w:pPr><w:r><w:t>제목5단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="6" /></w:pPr><w:r><w:t>제목6단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="7" /></w:pPr><w:r><w:t>제목7단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="8" /></w:pPr><w:r><w:t>제목8단계</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="9" /></w:pPr><w:r><w:t>제목9단계</w:t></w:r></w:p>
    <w:p><w:r><w:t>본문(바탕글)</w:t></w:r></w:p>
    ...
```

제목단계는 스타일시트 안에서 `w:outlineLvl`로 표현한다. 제목1단계는 0부터 시작해서 단계가 높아질수록 1씩 커진다.

`w:pPr`안의 run 속성 `w:rPr`이 내용이 있는 경우, `w:style` 자식으로 있는 링크속성 `<w:link w:val="1Char"/>` 등을 없애고 연결된 스타일을 삭제해도 무방하다.

```xml
<!-- word/styles.xml -->
<w:styles ... >
  <w:style w:type="paragraph" w:styleId="1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:outlineLvl w:val="0"/>...</w:pPr>
    <w:rPr><w:sz w:val="36"/><w:szCs w:val="28"/><w:color w:val="2F5496" ...><w:b/><w:bCs/></w:rPr>
    ...
  </w:style>
  <w:style w:type="paragraph" w:styleId="2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:outlineLvl w:val="1"/>...</w:pPr>
    <w:rPr><w:sz w:val="32"/><w:szCs w:val="26"/><w:color w:val="4472C4" ...><w:b/><w:bCs/></w:rPr>
    ...
  </w:style>
  <w:style w:type="paragraph" w:styleId="3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:outlineLvl w:val="2"/>...</w:pPr>
    <w:rPr><w:sz w:val="28"/><w:color w:val="4472C4" ...><w:b/><w:bCs/></w:rPr>
    ...
  </w:style>
```

### 4.4. HWPX 제목단계

HTML 문자서식 예제 4 (css stylesheet, 객체에 단일 클래스 적용)과 유사하다.

문단 앞뒤 간격, 좌우 여백 등의 문단속성은 `hp:p`에 적용되고  
폰트, 크기, 색상, 자간 등 문자속성은 `hp:run`에 적용된다.

```xml
<!-- Contents/section0.xml -->
<hs:sec ...>
  <hp:p paraPrIDRef="0"  styleIDRef="0"  ...><hp:run charPrIDRef="7" ><hp:t>본문(바탕글)</hp:t></hp:run></hp:p>
  <hp:p paraPrIDRef="9"  styleIDRef="20" ...><hp:run charPrIDRef="13"><hp:t>제목1단계</hp:t></hp:run></hp:p>
  <hp:p paraPrIDRef="10" styleIDRef="21" ...><hp:run charPrIDRef="17"><hp:t>제목2단계</hp:t></hp:run></hp:p>
  <hp:p paraPrIDRef="11" styleIDRef="22" ...><hp:run charPrIDRef="18"><hp:t>제목3단계</hp:t></hp:run></hp:p>
```

스타일시트를 언듯 보면, `hh:style id="20" type="PARA"`인 스타일에 `charPrIDRef="13"`이 지정되어 있어, 본문(section0.xml)의 `<hp:run charPrIDRef="13">`에서 레퍼런스 속성을 삭제해도 되는 것처럼 보이지만, 지우면 문자속성이 적용이 되지 않는다.

개요수준은 `hh:heading`태그의 `level`값으로 설정한다. 제목1단계는 0, 단계가 높아질수록 1씩 늘어난다.

```xml
<!-- Contents/header.xml -->
<hh:head ...>
  <hh:refList>
    <hh:styles itemCnt="33">
      <hh:style id="0"  type="PARA" name="바탕글"  engName="Normal"   paraPrIDRef="1"  charPrIDRef="7"  ... />
      ...
      <hh:style id="20" type="PARA" name="제목 1" engName="Heading 1" paraPrIDRef="9"  charPrIDRef="13" ... />
      <hh:style id="21" type="PARA" name="제목 2" engName="Heading 2" paraPrIDRef="10" charPrIDRef="17" ... />
      <hh:style id="22" type="PARA" name="제목 3" engName="Heading 3" paraPrIDRef="11" charPrIDRef="18" ... />
      ...
    </hh:styles>

    <hh:charProperties ...>
      ...
      <!-- 바탕글 / Normal / 크기 10, 색상 검정 #000000 -->
      <hh:charPr id="7" height="1000" textColor="#000000" ...>
        <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>
        ...
      </hh:charPr>
      <!-- 제목 1 / Heading 1 / 크기 18, 색상 짙은 파랑 #2F5496 / 굵게 -->
      <hh:charPr id="13" height="1800" textColor="#2F5496" ...>
        <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>
        <hh:bold/>
        ...
      </hh:charPr>
      <!-- 제목 2 / Heading 2 / 크기 16, 색상 연한 파랑 #2F5496 / 굵게 -->
      <hh:charPr id="17" height="1600" textColor="#4472C4" ...>
        <hh:fontRef hangul="0" latin="0" hanja="0" japanese="0" other="0" symbol="0" user="0"/>
        <hh:bold/>
        ...
      </hh:charPr>
    </hh:charProperties>

    <hh:paraProperties itemCnt="26">
      <hh:paraPr id="1"  ...>...</hh:paraPr>
      <hh:paraPr id="9"  ...><hh:heading type="OUTLINE" idRef="0" level="1"/>...</hh:paraPr>
      <hh:paraPr id="10" ...><hh:heading type="OUTLINE" idRef="0" level="2"/>...</hh:paraPr>
      <hh:paraPr id="11" ...><hh:heading type="OUTLINE" idRef="0" level="3"/>...</hh:paraPr>
      ...
    </hh:paraProperties>
```

## 5. 표

HTML, DOCX, HWPX의 각 요소는 다음과 같이 대응된다.

| HTML  | DOCX  | HWPX   |
|-------|-------|--------|
| table | w:tbl | hp:tbl |
| tr    | w:tr  | hp:tr  |
| td    | w:tc  | hp:tc  |

### 5.1. HTML 표

```html
<table>
    <tr>
      <td>
        <p>
          Two roads diverged in a yellow wood,<br>
          And sorry I could not travel both<br>
          And be one traveler, long I stood<br>
          And looked down one as far as I could<br>
          To where it bent in the undergrowth;
        </p>
      </td>
      <td>
        <p>
          And both that morning equally lay<br>
          In leaves no step had trodden black.<br>
          Oh, I kept the first for another day!<br>
          Yet knowing how way leads on to way,<br>
          I doubted if I should ever come back.
        </p>
      </td>
    </tr>
    <tr>
      <td>
        <p>
          Then took the other, as just as fair,<br>
          And having perhaps the better claim,<br>
          Because it was grassy and wanted wear;<br>
          Though as for that the passing there<br>
          Had worn them really about the same,
        </p>
      </td>
      <td>
        <p>
          I shall be telling this with a sigh<br>
          Somewhere ages and ages hence:<br>
          Two roads diverged in a wood, and I—<br>
          I took the one less traveled by,<br>
          And that has made all the difference.
        </p>
      </td>
    </tr>
</table>
```

### 5.2. DOCX 표

너비는 다양하게 설정할 수 있음

* dxa: 1/20pt = 1/1440inch
* pct: 퍼센트, 10000는 100%를 의미함
* auto: 내용에 맞춤
* nil: 0

```xml
<!-- word/document.xml -->
<w:document ... >
  <w:body>
    <w:tbl>
      <w:tblPr>
        <w:tblStyle w:val="a6"/>
        <w:tblW w:type="auto"/>
      </w:tblPr>
      <w:tr>
        <!--
        w:tcW 태그 없애면 내용에 맞춰 너비가 결정된다
        <w:tc><w:p><w:r><w:t>1</w:t></w:r></w:p></w:tc>
        -->
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>1</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>2</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>3</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>4</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>5</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>6</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>7</w:t></w:r></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="2254" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>8</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>
```

### 5.3. HWPX 표

- [ ] 속성들 없어도 되나? 날려되 되는게 있나? 한땀한땀 테스트...

```xml
  <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="7">
      <hp:tbl id="2030483458" zOrder="1" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" rowCnt="2" colCnt="2" cellSpacing="0" borderFillIDRef="4" noAdjust="0">
        <hp:sz width="45080" widthRelTo="ABSOLUTE" height="22454" heightRelTo="ABSOLUTE" protect="0"/>
        <hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="COLUMN" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>
        <hp:outMargin left="0" right="0" top="0" bottom="0"/>
        <hp:inMargin left="510" right="510" top="141" bottom="141"/>
        <hp:tr>
          <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="4">
            <hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">
              <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
                <hp:run charPrIDRef="7"><hp:t>Two roads diverged in a yellow wood,<hp:lineBreak/>
And sorry I could not travel both<hp:lineBreak/>
And be one traveler, long I stood<hp:lineBreak/>
And looked down one as far as I could<hp:lineBreak/>
To where it bent in the undergrowth;</hp:t>
                </hp:run>
              </hp:p>
            </hp:subList>
            <hp:cellAddr colAddr="0" rowAddr="0"/>
            <hp:cellSpan colSpan="1" rowSpan="1"/>
            <hp:cellSz width="22540" height="282"/>
            <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
          </hp:tc>
          <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="4">
            <hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">
              <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
                <hp:run charPrIDRef="7"><hp:t>And both that morning equally lay<hp:lineBreak/>
In leaves no step had trodden black.<hp:lineBreak/>
Oh, I kept the first for another day!<hp:lineBreak/>
Yet knowing how way leads on to way,<hp:lineBreak/>
I doubted if I should ever come back.</hp:t>
                </hp:run>
              </hp:p>
            </hp:subList>
            <hp:cellAddr colAddr="1" rowAddr="0"/>
            <hp:cellSpan colSpan="1" rowSpan="1"/>
            <hp:cellSz width="22540" height="282"/>
            <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
          </hp:tc>
        </hp:tr>
        <hp:tr>
          <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="4">
            <hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">
              <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
                <hp:run charPrIDRef="7"><hp:t>Then took the other, as just as fair,<hp:lineBreak/>
And having perhaps the better claim,<hp:lineBreak/>
Because it was grassy and wanted wear;<hp:lineBreak/>
Though as for that the passing there<hp:lineBreak/>
Had worn them really about the same,</hp:t>
                </hp:run>
              </hp:p>
            </hp:subList>
            <hp:cellAddr colAddr="0" rowAddr="1"/>
            <hp:cellSpan colSpan="1" rowSpan="1"/>
            <hp:cellSz width="22540" height="282"/>
            <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
          </hp:tc>
          <hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="4">
            <hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="TOP" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">
              <hp:p paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
                <hp:run charPrIDRef="7"><hp:t>I shall be telling this with a sigh<hp:lineBreak/>
Somewhere ages and ages hence:<hp:lineBreak/>
Two roads diverged in a wood, and I—<hp:lineBreak/>
I took the one less traveled by,<hp:lineBreak/>
And that has made all the difference.</hp:t>
                </hp:run>
              </hp:p>
            </hp:subList>
            <hp:cellAddr colAddr="1" rowAddr="1"/>
            <hp:cellSpan colSpan="1" rowSpan="1"/>
            <hp:cellSz width="22540" height="282"/>
            <hp:cellMargin left="510" right="510" top="141" bottom="141"/>
          </hp:tc>
        </hp:tr>
      </hp:tbl>
      <hp:t/>
    </hp:run>
  </hp:p>
```

## 6. 이미지

### 6.1. HTML 이미지

```html
<img src=red.png width=500 />
```

### 6.2. DOCX 이미지

```xml
<!-- word/_rels/document.xml.rels -->
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image2.png"/>
  ...
</Relationships>
```

```xml
<!-- word/document.xml -->
    <w:p>
      <w:r>
        <w:drawing>
          <ns3:inline distT="0" distB="0" distL="0" distR="0">
            <ns3:extent cx="288000" cy="288000"/>
            <ns3:docPr id="465450021" name="그림 1"/>

            <ns3:cNvGraphicFramePr>
              <ns5:graphicFrameLocks noChangeAspect="1"/>
            </ns3:cNvGraphicFramePr>

            <ns5:graphic>
              <ns5:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <ns6:pic>
                  <ns6:nvPicPr>
                    <ns6:cNvPr id="465450021" name="그림 465450021"/><ns6:cNvPicPr/>
                  </ns6:nvPicPr>

                  <ns6:blipFill>
                    <ns5:blip ns2:embed="rId8">
                    </ns5:blip>

                    <ns5:stretch>
                      <ns5:fillRect/>
                    </ns5:stretch>
                  </ns6:blipFill>


                  <ns6:spPr>
                    <ns5:xfrm>
                      <ns5:off x="0" y="0"/>
                      <ns5:ext cx="288000" cy="288000"/>
                    </ns5:xfrm>

                    <ns5:prstGeom prst="rect">
                      <ns5:avLst/>
                    </ns5:prstGeom>
                  </ns6:spPr>
                </ns6:pic>
              </ns5:graphicData>
            </ns5:graphic>
          </ns3:inline>
        </w:drawing>
      </w:r>
    </w:p>
```

### 6.3. HWPX 이미지

```xml
<!-- Contents/content.hpf -->
<opf:package ...>
  ...
  <opf:manifest>
    ...
    <opf:item id="image1" href="BinData/image1.png" media-type="image/png" isEmbeded="1"/>
  </opf:manifest>
```

```xml
<!-- Contents/section0.hpf -->
  <hp:p id="0" paraPrIDRef="0" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="7">
      <hp:pic id="2030483461" zOrder="0" numberingType="NONE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="956741638" reverse="0">
        <hp:offset x="0" y="0"/>
        <hp:orgSz width="2267" height="2267"/>
        <hp:curSz width="0" height="0"/>
        <hp:flip horizontal="0" vertical="0"/>
        <hp:rotationInfo angle="0" centerX="1133" centerY="1133" rotateimage="1"/>
        <hp:renderingInfo>
          <hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>
          <hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>
          <hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>
        </hp:renderingInfo>
        <hc:img binaryItemIDRef="image1" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>
        <hp:imgRect>
          <hc:pt0 x="0" y="0"/>
          <hc:pt1 x="2267" y="0"/>
          <hc:pt2 x="2267" y="2267"/>
          <hc:pt3 x="0" y="2267"/>
        </hp:imgRect>
        <hp:imgClip left="0" right="0" top="0" bottom="0"/>
        <hp:inMargin left="0" right="0" top="0" bottom="0"/>
        <hp:imgDim dimwidth="0" dimheight="0"/>
        <hp:effects/>
        <hp:sz width="2267" widthRelTo="ABSOLUTE" height="2267" heightRelTo="ABSOLUTE" protect="0"/>
        <hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="1" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="COLUMN" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>
        <hp:outMargin left="0" right="0" top="0" bottom="0"/>
        <hp:shapeComment>그림입니다.
원본 그림의 이름: image2.png
원본 그림의 크기: 가로 10pixel, 세로 10pixel</hp:shapeComment>
      </hp:pic>
      <hp:t/>
    </hp:run>
    <hp:linesegarray>
      <hp:lineseg textpos="0" vertpos="15231" vertsize="2267" textheight="2267" baseline="2267" spacing="260" horzpos="0" horzsize="45128" flags="393216"/>
    </hp:linesegarray>
  </hp:p>
```
