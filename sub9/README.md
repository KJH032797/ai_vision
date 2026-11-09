# 교과 9 2일차 — 전처리와 Otsu Challenge

## Day02 진행 기록

- **입력:** `samples/day02/challenge.jpg`
- **문제:** 병뚜껑 면과 주변 배경의 명암 차이가 작아 Otsu만으로 안정적으로 분리되지 않음
- **전처리:** CLAHE (`clipLimit=2.0`, `tileGridSize=(8, 8)`) + Median Blur (`median_kernel=7`)
- **이진화:** crop 전체에 Otsu 역이진화 적용. 원본 임계값 `110`, 전처리 결과 임계값 `103`
- **판정:** 전처리로 잔점과 표면 질감은 줄었지만 병뚜껑 전체가 배경에서 완전히 분리되지 않음. 2일차에서는 이 한계를 기록하고, 3일차 추가 확인 대상으로 남김.
- **실패 기록:** CLAHE 뒤 Unsharp Mask를 적용했을 때 병뚜껑 홈뿐 아니라 표면 무늬와 노이즈도 강조되어 최종 방법으로 채택하지 않음.
- **결과 이미지:** `outputs/day02/compare/preprocess_compare.png`, `outputs/day02/challenge/challenge_result.jpg`
- **판정 한계:** 3일차 실습은 이 Challenge 결과를 그대로 입력으로 쓰지 않고 `cap_on_reference`와 `cap_off_reference`에서 다시 시작함.

자세한 매개변수 비교와 선택 근거는 `reports/day02_parameter_table.csv`, `reports/day02_preprocess_reason.md`를 참고한다.

---

## Day 07 — MVTec AD Bottle Anomaly Detection

- Dataset 분할: Normal Train 167장, Normal Validation 42장, Test 83장 (Normal 20장, Anomaly 63장)
- Baseline: 사전학습 ResNet18, `layer3` 특징, Normal Train 평균 Reference
- Frozen Rule: `day07-anomaly-v1.0`, Validation 95th percentile, Threshold `0.067458`
- Test 결과: Accuracy `0.9277`, Anomaly Precision `0.9672`, Anomaly Recall `0.9365`; TP 59 / TN 18 / FP 2 / FN 4
- Test 세부 결과: `reports/day07_anomaly_scores.csv`, `reports/day07_test_metrics.md`
- Heatmap: 대표 Test 8장의 Heatmap/Overlay와 Ground Truth 비교 파일은 `outputs/day07/heatmap/`에 저장
- Challenge: 고정 Rule로 Dark/Bright/Blur/Shift/Rotation을 평가했다. Dark/Bright/Shift는 FP, Blur/Rotation은 PASS (`reports/day07_challenge_results.csv`)
- Mini Challenge: 두 번째 Normal Test 이미지에 Dark/Blur/Rotation을 적용했다. Dark는 FP, Blur/Rotation은 PASS (`reports/day07_mini_challenge.md`)
- 실패 분석: `reports/day07_failure_analysis.md`

Test와 Challenge 결과로 Threshold를 다시 조정하지 않았다. 이미지와 파생 데이터는 `samples/day07/`, `artifacts/day07/`, `outputs/day07/`에 둔다.

---

## Day 08 — Low-Data Inspection

### One-shot
- Normal Reference: 1장
- Common Query: Normal 10장 + Anomaly 10장
- Accuracy: 85%; FP 1, FN 2

### Few-shot
- Normal Support: 5장; Anomaly Support: 5장
- Common Query: One-shot과 동일
- Accuracy: 90%; FP 0, FN 2

### Comparison
Few-shot에서 이번 Query의 정상 오탐은 줄었지만, 불량 미검출은 두 방법 모두 2건이었다. 세부 지표는 reports/day08_method_comparison.csv에 있다.

### Support Count Mini Challenge
Support 1/3/5 결과 Accuracy는 각각 70%/80%/90%, FN은 5/4/2였다. 이번 선택 Support에서 관찰한 값이며 일반적인 성능 보장은 아니다.

### Defect Generation
- broken_small Source와 Ground Truth Mask 기반 Cut-Paste로 20장 생성
- contamination 조건으로 Mini Challenge 5장 생성
- 생성 기록은 reports/day08_defect_metadata.csv 및 reports/day08_mini_challenge_contamination_metadata.csv에 저장
- 합성 외관의 AI 사전 검토는 완료, 사람의 최종 품질 검수는 확인 대기

### 핵심
데이터 수와 종류에 맞춰 One-shot/Few-shot/Anomaly Detection/Defect Generation을 선택하고, 동일 Query에서 결과를 비교한다. Synthetic Data는 생성만으로 충분하지 않으며 품질 확인이 필요하다.
