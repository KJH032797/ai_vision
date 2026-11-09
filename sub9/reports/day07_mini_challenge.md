# Day07 Mini Challenge

- Source: `samples/day07/test/normal/001.png`
- Rule: `day07-anomaly-v1.0`
- Frozen threshold: `0.067458` (`configs/day07_anomaly_rules.json`)
- 사전 예상: 실행 전에 기록된 예상이 없어 비교할 수 없음

| 변형 | 적용한 값 | 사전 예상 | 실제 Score | 판정 | 결과 |
|---|---:|---|---:|---|---|
| Dark | alpha = 0.75 | 미기록 | 0.089038 | Anomaly | FP |
| Blur | kernel = 7 | 미기록 | 0.050097 | Normal | PASS |
| Rotation | angle = 10° | 미기록 | 0.046322 | Normal | PASS |

- 가장 높은 Score: Dark (`0.089038`)
- 예상과 실제 비교: 사전 예상이 기록되지 않아 비교 불가
- 한 줄 정리: 고정 Rule에서는 이번 설정의 Dark만 Threshold를 넘어 FP가 되었고, Blur와 Rotation은 Normal로 통과했다.

실행 코드: `python src/61_day07_mini_challenge.py`
변형 이미지는 `samples/day07/mini_challenge/variants/`에 저장했다.
