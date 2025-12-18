# HWPX 참고사항

## HWPX 호환모드

`Contents/header.xml` 파일 안의 `hh:compatibleDocument` 태그가 있으면 MS워드 호환모드로 표시된다.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<hh:head ... >
  ...
  <hh:compatibleDocument targetProgram="MS_WORD">
    <hh:layoutCompatibility>
      <hh:applyFontWeightToBold/>
      <hh:useInnerUnderline/>
      <hh:useLowercaseStrikeout/>
      <hh:extendLineheightToOffset/>
      <hh:treatQuotationAsLatin/>
      <hh:doNotAlignWhitespaceOnRight/>
      <hh:doNotAdjustWordInJustify/>
      <hh:baseCharUnitOnEAsian/>
      <hh:baseCharUnitOfIndentOnFirstChar/>
      <hh:adjustLineheightToFont/>
      <hh:adjustBaselineInFixedLinespacing/>
      <hh:applyPrevspacingBeneathObject/>
      <hh:applyNextspacingOfLastPara/>
      <hh:adjustParaBorderfillToSpacing/>
      <hh:connectParaBorderfillOfEqualBorder/>
      <hh:adjustParaBorderOffsetWithBorder/>
      <hh:extendLineheightToParaBorderOffset/>
      <hh:applyParaBorderToOutside/>
      <hh:applyMinColumnWidthTo1mm/>
      <hh:applyTabPosBasedOnSegment/>
      <hh:breakTabOverLine/>
      <hh:adjustVertPosOfLine/>
      <hh:doNotAlignLastForbidden/>
      <hh:adjustMarginFromAdjustLineheight/>
      <hh:baseLineSpacingOnLineGrid/>
      <hh:applyCharSpacingToCharGrid/>
      <hh:doNotApplyGridInHeaderFooter/>
      <hh:applyExtendHeaderFooterEachSection/>
      <hh:doNotApplyLinegridAtNoLinespacing/>
      <hh:doNotAdjustEmptyAnchorLine/>
      <hh:overlapBothAllowOverlap/>
      <hh:extendVertLimitToPageMargins/>
      <hh:doNotHoldAnchorOfTable/>
      <hh:doNotFormattingAtBeneathAnchor/>
      <hh:adjustBaselineOfObjectToBottom/>
    </hh:layoutCompatibility>
  </hh:compatibleDocument>`
```

## HWPX에서 변환기를 만들 때 삭제해도 무방한 태그

`Contents/section0.xml` 안에서 다음은 제거하여도 문서의 열림과 편집에 지장을 주지 않는다.

* `hp:p` 태그의 `id` 속성은 문서의 변환과정을 추적하기 위해 생성하는 속성으로 제거하여도 무방하다.
* `hp:linesegarray`와 하위 태그도 제거하여도 무방하다. 줄바꿈이 일어날 때, 렌더링 될 위치를 지정하는 것처럼 보인다. 제거하여도 문서는 잘 열리며, 다시 생성된다.
