# 🤬 Swear Words Filitering in Video 🤬

## 0. Quick Link

<div align="center">
<a href="https://www.youtube.com/watch?v=ydWShDVGubo&ab_channel=SuwonPabby">
 <img src="https://drive.google.com/uc?id=18aYk6BtLhNMqZ1X3_RKTX3w-B-cXkMXK" width="400" alt="최종발표 영상 보러가기">
</a>
<a href="https://github.com/SuwonPabby/Yok_Filtering/blob/main/Final/Grad_Model%E1%84%8B%E1%85%B4_%E1%84%89%E1%85%A1%E1%84%87%E1%85%A9%E1%86%AB.ipynb">
 <img src="https://drive.google.com/uc?id=1R8kMYYBEZjbEL4xqkMSZVj9OvC8cnI65" width="400" alt="모델 학습 코드 보러가기">
</a>
</div>
<div align="center">
<a href="https://github.com/SuwonPabby/Yok_Filtering/blob/main/Final/module.py">
 <img src="https://drive.google.com/uc?id=1HKoKibC0fZclA4sxob5YbO4M6_qdT6B_" width="400" alt="실제 동작 Module 보러가기">
</a>
<a href="https://github.com/SuwonPabby/Yok_Filtering/blob/main/Final/app.py">
 <img src="https://drive.google.com/uc?id=1osqIelK1xr2N8jseXIsAoxkcAkNK52bR" width="400" alt="Flask 서버 코드 보러가기">
</a>
</div>

## 1. What We Made

<div align="center">
<img src="https://drive.google.com/uc?id=16qQuVFXfK5DHG2nLj_J8CS97GqKKJChO" width="600" alt="개요 이미지">
</div>

### 🤬 최근 미디어 내에는 자극적인 워딩이 많이 등장합니다.

- 최근 유튜브, 틱톡과 같은 영상 매체 플랫폼이 우리 일상 속에 깊게 스며들었습니다.
- 그러나 생생한 영상을 위해서 영상에 욕설을 가감없이 넣는 등 자극적인 영상이 많이 등장하고 있습니다.
- 물론 다 큰 성인이라면 상관 없겠지만, 유튜브 영상은 누구에게나 노출되기에 아직 분별력이 없는 어린이나 어린 학생은 이로 인해 악영향을 미칠 수도 있습니다.

### 🤬 그래서 저희는 영상 미디어 내 욕설을 자동으로 감지해 Beep Sound를 입혀줍니다.

- 저희는 위와 같은 문제를 해결할 수 있는 하나의 수단으로 영상 내 욕설 감지기를 만들어보기로 하였습니다.
- 영상 데이터가 입력으로 들어오면 영상 내에 있는 욕설을 자동으로 감지하고 이 부분을 Beep Sound로 바꾸어줍니다.
- AI 를 이용하는 이유는, 문맥을 고려한 분류를 가능케하기 위함입니다.
  Ex. "이 역은 이 열차의 시발역이다." VS "시발놈아 정신차려"

## 2. System Structure

![10-08-2023-21 20 18](https://github.com/SuwonPabby/Yok_Filtering/assets/60493070/0eceb923-1b3a-4ee8-ad5b-bed1d793067c)

### 🤬 저희 시스템의 동작 과정은 다음과 같습니다.

1. 영상 데이터가 입력으로 들어옵니다.
2. CLOVA STT API를 이용해 영상 파일 내에서 텍스트와 해당 텍스트가 발화된 TimeStamp 정보를 얻습니다.
3. 각각의 Text를 학습된 인공지능 모델과 LIME Algorithm을 이용하여 해당 단어가 욕설인지 아닌지에 대한 Score 값을 얻어냅니다.
4. 여기에서 욕설로 분류된 Text의 TimeStamp 부분에 Beep Sound를 입혀 영상 파일에 병합합니다.
5. 병합된 최종 영상 파일을 출력합니다.

## 3. Collecting Data

- 저희는 욕설을 분류하는 문제를 푸는 것이므로 **욕설이 다수 포함된 한국어 데이터**가 많이 필요했습니다.
- 따라서 한글 위키피디아와 같은 데이터는 이용하기 어려웠습니다.
- 영상 미디어 내에서 텍스트를 추출해 데이터셋으로 사용하는 방법을 고안해보았으나, 유튜브 자동 추출은 한국어 성능이 매우 떨어졌고, CLOVA API를 이용하기에는 너무 많은 요금이 발생하는 상황이었습니다.
- 그래서 저희는 영상 미디어와 상황은 좀 다르지만, 욕설을 많이 확보할 수 있는 네이트판 **댓글 데이터**를 이용했습니다.
- 크롤링은 **Beautiful Soup**와 **Selenium** 등을 활용하여 수행하였습니다.
- 더불어 부족한 욕설 정보를 추가로 확보하기 위해 자주 사용되는 욕설 사전도 학습 데이터로 넣었습니다. 단, 이 데이터는 욕설 자체에 대한 감지에 영향을 미치지만 문맥을 고려한 욕설 판단에는 큰 영향을 미치지 못합니다.

## 4. Data Preprocessing

- 댓글 데이터는 보통 맞춤법이 제대로 지켜지지도 않고, "ㅋㅋ" 와 같은 용어를 사용하거나 자음만 사용하는 경우가 매우 많았습니다.
- 특히나 저희가 원하는 욕설 데이터의 경우 "시발" 이렇게 딱 원하는 단어가 들어가 있는 것이 아닌 "ㅅㅂ" 혹은 "시1발" 과 같이 변형된 형태로 많이 들어가 있는 상황이었습니다.
- 따라서 저희는 단어 단위 인덱싱, 형태소 단위 인덱싱, 음절 단위 인덱싱을 하기에는 적절하지 않은 상황이었습니다.
- 그래서 저희는 **음운 단위 인덱싱**을 이용했습니다. 하나의 음절은 3개의 각 음운을 나타내는 정수값으로 표현되게 됩니다.
- 만일 받침이 존재하지 않거나, 초성만 존재할 경우 없는 음운은 비어있다는 의미의 토큰을 넣어주게 됩니다.
- 워낙 오타도 많고, 맞춤법에 맞지 않는 데이터가 많기에 불용어 제거와 같은 처리는 하지 않았습니다.

## 5. 1DCNN Based Model Training & Testing

- 언어 데이터이기에 RNN을 생각할 수 있지만, 이 문제는 언어 내에 **욕설 패턴** 형태를 찾는 문제이기에 **1DCNN** 방식을 이용했습니다.
- 실제로 아래 첨부된 사진과 같이 LSTM 계열 모델보다 성능이 좋음을 확인할 수 있습니다.
  ![10-08-2023-22 52 23](https://github.com/SuwonPabby/Yok_Filtering/assets/60493070/177750c0-bfd3-4c7b-884e-dfb1a79e0a47)
- 사용된 모델 구조는 아래와 같습니다.
<div align="center"> 
<img src="https://github.com/SuwonPabby/Yok_Filtering/assets/60493070/bb8a5c37-7ec6-46ae-b602-2908e17e1887" width="600">
</div>

- 1DCNN 기반 모델로 **acc 89%** 의 성능을 확보했습니다.

## 6. Applying LIME Algorithm

- LIME Algorithm은 욕설로 의심되는 문장에서 단어를 하나씩 빼보면서 욕설일 확률을 가장 많이 떨어뜨리는 단어가 욕설이라고 판별하는 알고리즘입니다.
- 저희는 입력으로 들어오는 text를 4개 단어 단위로 쪼갠 뒤, 4개 단어 묶음을 1DCNN 모델을 통과시켜 4개 단어 묶음의 욕설 확률 값을 얻어냅니다. 저희는 이를 Group Score라고 정의했습니다.
- 이 묶음에 속한 모든 단어들의 Group Score의 값은 모두 동일합니다.
- 이어서 이 묶음에서 한 단어씩 없앴을 때 나머지 3개 단어 묶음이 욕설일 확률을 1DCNN 모델을 통과시켜 3개 단어의 욕설 확률 값을 얻어냅니다. 저희는 이를 Word Score라고 정의했습니다.
- Word Score는 제거시킨 단어에 대응되는 값입니다.
- 예를 들어 4개의 단어 A B C D 로 구성된 묶음이 있다면
  $groupScore(A) = groupScore(B) = groupScore(C) = groupScore(D)$ 입니다.
  한편 A를 제거한 B C D 문장을 1DCNN 모델에 넣어 얻은 값은 $wordScore(A)$ 입니다.
- 판별을 단어 단위로 하고 있으나, 모델은 음운별 인덱싱을 사용하고 있으므로 각 단어를 음운으로 나누어 인덱싱한 뒤 모델에 입력합니다.
- 각 단어에 대하여 아래의 조건식을 만족시키면 저희는 이 단어를 욕설로 판별했습니다.
  $wordScore(word) > 1.1 - globalScore(word)$

  ![10-08-2023-22 51 09](https://github.com/SuwonPabby/Yok_Filtering/assets/60493070/945ad2d3-9065-40a6-9008-892e6f9c3388)

## 7. Implementing Service Flow Pipeline

- 저희는 이렇게 만들어진 판별기를 이용해 실제 사용 플로우에 접목시 켰습니다.
- 영상 데이터 입력 -> CLOVA API를 통한 Text 추출 -> 판별기에 Text 입력 -> 욕설로 분류된 Word 리스트 확보 -> 해당 Word에 해당하는 타임스템프 부분을 Beep Sound 삽입 -> 영상 출력
  의 플로우로 제작하였습니다.

## 8. Implementing Simple Web Based Front-End

- Flask를 이용해 API를 개통하고, 간단히 시연이 가능한 Web Front End를 만들었습니다.

