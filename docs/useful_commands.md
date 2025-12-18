# 유용한 명령어

DOCX, HWPX 분석과 개발에 활용하였던 명령어들

## pandoc 변환 명령어

```sh
IN=sample.md
R=template.docx
OUT=sample.docx
pandoc --reference-doc=$R $IN -o $OUT
```

## 압축 해제

```sh
mkdir blank
unzip blank.hwpx -d blank
```

```
$ unzip 001_blank.hwpx -d blank
Archive:  01_blank.hwpx
 extracting: blank/mimetype
 extracting: blank/version.xml
  inflating: blank/Contents/header.xml
  inflating: blank/Contents/section0.xml
  inflating: blank/Preview/PrvText.txt
  inflating: blank/settings.xml
 extracting: blank/Preview/PrvImage.png
  inflating: blank/META-INF/container.rdf
  inflating: blank/Contents/content.hpf
  inflating: blank/META-INF/container.xml
  inflating: blank/META-INF/manifest.xml
```

## prettify

```sh
find . -type f \( -name '*.xml' -o -name '*.rels' -o -name '*.hpf' -o -name '*.rdf' \) | while read -r file; do
    xmllint --format "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
```

## 재압축

```sh
cd blank
# some modification
zip -r ../blank2.hwpx *
```
