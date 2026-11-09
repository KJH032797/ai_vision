# Day08 Mini Challenge

## 1. Support Count 비교

같은 Few-shot Support 집합에서 앞의 1장, 3장, 5장을 사용하고, Common Query 20장은 고정했다. 실행 전 개인 예상은 기록되지 않아 사후에 채우지 않았다.

| Support (클래스별) | Accuracy | FP | FN |
|---:|---:|---:|---:|
| 1 | 0.7000 | 1 | 5 |
| 3 | 0.8000 | 0 | 4 |
| 5 | 0.9000 | 0 | 2 |

세 결과 모두 이 실험에서는 Support 수가 많아질수록 정확도가 높아지고 FN이 줄었다. 이 결과만으로 Support 수 증가가 항상 성능을 높인다고 일반화하지 않는다.

세부 결과: reports/day08_support_count_comparison.csv
실행 코드: python src/70_day08_compare_support_counts.py

## 2. contamination Synthetic Defect

- 생성 수: 5장
- 조건: scale 0.6~1.0, rotation -10°~+10°, seed 42
- 이미지: outputs/day08/mini_challenge/contamination/
- Metadata: reports/day08_mini_challenge_contamination_metadata.csv
- AI 사전 검토상 가장 자연스러운 후보: synthetic_004.png
- AI 사전 검토상 가장 어색한 후보: synthetic_003.png
- 사람 최종 검수: 미완료, 직접 이미지 확인 후 후보를 확정해야 함

## 3. 상황별 방법 선택

- 정상 데이터 충분 / 불량 0장: Anomaly Detection을 먼저 고려. 정상 패턴을 기준으로 이상을 찾는 방식이므로 불량 예제가 없어도 시작할 수 있다.
- Normal Reference 1장 중심, 정상 Calibration 데이터 보유: One-shot을 고려. 기준 이미지와 정상 Calibration으로 유사도 Threshold를 정한다.
- Normal / Anomaly 예제가 각각 소수 있음: Few-shot을 고려. 두 그룹의 Support로 Prototype을 만든다.
- 불량 데이터 자체가 부족함: Defect Generation을 보조 수단으로 고려하고, 합성 이미지의 품질 확인 및 실제 불량 데이터 추가 수집을 함께 계획한다.

## 오늘의 한 줄 결론

이번 Support 집합과 고정 Query에서는 Support 수가 1에서 5로 늘 때 판정이 좋아졌지만, 소수의 예제 구성에 따라 결과가 달라질 수 있으므로 같은 Query와 지표로 비교해야 한다.
