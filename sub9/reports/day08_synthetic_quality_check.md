# Day08 Synthetic Quality Check

## 확인 대상

- broken_small 20장: outputs/day08/cutpaste/generated/
- contamination 5장: outputs/day08/mini_challenge/contamination/
- 전체 미리보기: outputs/day08/qa_review/contact_sheet.jpg

## 검수 상태

아래 평가는 생성 결과를 Contact Sheet와 대표 contamination 원본으로 비교한 AI의 사전 시각 검토다. 사람의 최종 Keep / Reject 검수는 아직 완료되지 않았다. 아래 후보를 사람이 확인한 뒤 확정해야 한다.

## broken_small 합성 이미지 20장 — AI 사전 분류

| 파일 | AI 사전 의견 | 관찰 |
|---|---|---|
| synthetic_000.png | Reject 후보 | 결함이 길고 넓게 퍼져 합성 흔적이 두드러짐 |
| synthetic_001.png | Reject 후보 | 긴 조각 형태로 병 입구를 가로지름 |
| synthetic_002.png | Reject 후보 | 결함이 길게 이어져 작은 파손보다 크게 보임 |
| synthetic_003.png | Reject 후보 | 결함 조각과 밝은 경계가 눈에 띔 |
| synthetic_004.png | Keep 후보 | 결함이 비교적 작고 한 영역에 모여 있음 |
| synthetic_005.png | Reject 후보 | 조각 형태가 분리되어 붙은 듯 보임 |
| synthetic_006.png | Reject 후보 | 결함이 크고 밝은 픽셀이 두드러짐 |
| synthetic_007.png | Reject 후보 | 결함이 길고 밝은 경계가 강함 |
| synthetic_008.png | Reject 후보 | 굽은 결함이 병 입구를 넓게 가로지름 |
| synthetic_009.png | Reject 후보 | 결함이 크게 퍼져 있음 |
| synthetic_010.png | Reject 후보 | 세로로 길게 뻗은 결함 조각이 눈에 띔 |
| synthetic_011.png | Reject 후보 | 큰 굽은 조각이 병 입구를 가로지름 |
| synthetic_012.png | Reject 후보 | 결함이 크고 제품 외곽 쪽으로 돌출됨 |
| synthetic_013.png | Keep 후보 | 결함이 비교적 작고 국소적임 |
| synthetic_014.png | Reject 후보 | 큰 굽은 조각이 제품 바깥쪽까지 이어짐 |
| synthetic_015.png | Reject 후보 | 결함이 넓고 길게 퍼짐 |
| synthetic_016.png | Reject 후보 | 결함이 길고 밝은 영역이 두드러짐 |
| synthetic_017.png | Keep 후보 | 결함이 비교적 작고 국소적으로 나타남 |
| synthetic_018.png | Reject 후보 | 세로로 길게 뻗어 작은 파손으로 보기 어려움 |
| synthetic_019.png | Reject 후보 | 넓은 결함 조각과 합성 경계가 보임 |

AI 사전 검토 제안은 Keep 후보 3장(synthetic_004, synthetic_013, synthetic_017), Reject 후보 17장이다. 이는 사람의 최종 판정이 아니다.

## contamination 합성 이미지 5장 — AI 사전 검토

- 생성 수: 5장
- 비교한 실제 Source: mini_challenge/defect_source/contamination/images/006.png, 008.png
- 가장 자연스러워 보이는 후보: synthetic_004.png — 작은 국소 얼룩 형태로 나타남
- 가장 어색해 보이는 후보: synthetic_003.png — 얼룩이 병의 안쪽 경계를 넘어 바깥쪽까지 걸쳐 보임
- 관찰: 큰 원형 얼룩은 실제 Source의 결함 형태와 비슷한 면도 있지만, 일부 합성물에서는 크기·위치가 부자연스럽고 경계가 분명하다.
- 사람 확인: 위 후보와 나머지 3장의 위치·크기·경계·결함 형태를 직접 확인한 뒤 확정 필요

## 결론과 한계

합성 파일과 Metadata 생성은 완료되었다. 이미지가 실제 결함을 충분히 닮았는지에 대한 최종 사람 검수는 남아 있다. 이 품질 검토는 합성 데이터의 외관만 살핀 것이며, 학습에 추가했을 때 모델 성능이 좋아지는지는 평가하지 않았다.
