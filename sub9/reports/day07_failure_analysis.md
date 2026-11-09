# Day07 Failure Analysis

사용한 Rule은 `day07-anomaly-v1.0`, Threshold는 `configs/day07_anomaly_rules.json`의 `0.067458`이다. 아래 원인은 Score와 파이프라인을 바탕으로 한 추정이며, 원인을 분리하는 추가 실험으로 확인한 결론은 아니다.

## Test FP

- File: `samples/day07/test/normal/006.png`
- Score: `0.069446` (Threshold `0.067458` 초과)
- 결과: 실제 Normal을 Anomaly로 판정 (FP)
- 원인 추정: 정상 이미지의 특징 거리가 정상 Validation에서 정한 기준보다 조금 높았다. 어떤 영상 특징이 차이를 만들었는지는 이 집계 Score만으로 특정할 수 없다.

## Test FN

- File: `samples/day07/test/anomaly/broken_small/000.png`
- Score: `0.053315` (Threshold 이하)
- 결과: 작은 파손 이미지를 Normal로 판정 (FN)
- 원인 추정: 이 이미지의 파손 특징이 현재 ResNet18 `layer3` 평균 특징과 비교하는 점수에서 충분히 크게 나타나지 않았을 가능성이 있다. 결함의 크기나 위치가 원인인지는 별도 Heatmap/원본 확인 없이는 확정할 수 없다.

## Challenge FP

- 변형: `normal_dark.png` (Dark, alpha `0.60`)
- Score: `0.123438` (Threshold `0.067458` 초과)
- 결과: 실제 Normal 이미지를 Anomaly로 판정 (FP)
- 관찰: 입력의 밝기를 낮춘 변형에서 Score가 Threshold를 넘었다. 밝기 변화가 특징 표현에 영향을 준 것으로 해석할 수 있지만, 다른 조건과 분리한 추가 실험은 수행하지 않았다.

## 기준값 참고

수업문서의 예시 결과에는 Threshold `0.067469`가 적혀 있지만 현재 프로젝트의 `configs/day07_anomaly_rules.json` 및 `reports/day07_threshold_compare.csv`는 `0.067458`을 사용한다. 이번 Challenge와 Mini Challenge는 이미 Freeze된 프로젝트 설정값 `0.067458`을 사용했다. 수업문서 예시와 현재 산출물의 차이는 임의로 수정하지 않았다.

## 수업문서 예시와 실제 Challenge 실행값

수업문서 예시 Score 순서는 Blur/Bright/Dark/Rotation/Shift 기준 0.065173, 0.104318, 0.123422, 0.054642, 0.076099이다. 이번 실행에서는 같은 순서로 0.065153, 0.104316, 0.123438, 0.054645, 0.076092가 나왔다. 소수점 아래 값에는 작은 차이가 있지만 Normal/Anomaly 및 PASS/FP 분류는 모두 같다. 차이의 원인은 확인되지 않았으며, 고정 Threshold는 변경하지 않았다.

## 한 줄 정리

현재 기준은 큰 파손·오염을 잘 구분했지만, 작은 파손을 놓치는 FN과 정상 Test/촬영 조건 변화에서의 FP가 남아 있다. Threshold를 Test/Challenge 결과에 맞춰 바꾸지 않았다.
