# ai_vision 프로젝트 컨텍스트

## 프로젝트 경로와 목적

- WSL 작업공간: `/home/user27/ai_vision`
- 교과 9 실제 프로젝트: `/home/user27/ai_vision/sub9`
- 목적: OpenCV로 ROI·전처리·Threshold·Morphology·Contour를 적용해 병뚜껑 유무를 측정하고, 규칙 기반 판정을 이미지/영상/스마트폰 실시간 입력에 연결하는 교육용 실습.
- 이 폴더는 Desktop `group2-project` 교과 7~8 복사본과 별개다. 그 복사본의 JPG/TXT 부재 제한을 이곳에 자동 적용하지 않는다. 사용자가 이 WSL 경로를 확인해 달라고 요청한 경우 실제 파일을 읽고 분석할 수 있다. 다만 이 경로에 적용되는 별도 보안 규칙이 있으면 그 지침을 따른다.

## 프로젝트 규칙

- 작업 전 이 파일과 `/home/user27/ai_vision/AGENTS.md`, 하위 프로젝트의 코드·설정·보고서를 확인한다.
- Obsidian 수업 문서가 주요 기준이다. 수업의 목표·예시 결과와 현재 코드/실험 결과를 구분한다. 교재 경로·샘플 이름이 현재 프로젝트와 다를 수 있으므로 실제 경로를 확인한다.
- 코드는 요청한 범위만 수정하고, 촬영·ROI·전처리 조건을 근거 없이 바꾸지 않는다. 미측정 수치나 반복 결과를 사후에 만들어 넣지 않는다.
- 이미지 파이프라인은 대체로 `입력/ROI → Gray/Otsu → Morphology → Contour/Feature → Rule → 출력`이다. 전처리·분리 품질 개선은 별도 요청이 없다면 기존 작업을 함부로 튜닝하지 말고 실패 조건부터 기록한다.
- 수업의 공통 코딩 규칙과 기존 AGENTS를 따른다. 경로는 `Path` 기반, 입력 존재 확인, 실행 로직은 `main()` 가드, 결과는 콘솔 외 파일에도 기록한다.
- 테스트는 사용자가 요청하거나 작업 지침에서 요구할 때 실행한다. 실행하지 않은 테스트를 통과했다고 말하지 않는다.
- 현재 확인된 `/home/user27/ai_vision` 및 `/home/user27/ai_vision/sub9`에는 Git 메타데이터가 없다. 작업 전 다시 확인하고, Git 초기화·commit은 요청 없이 하지 않는다.

## 수업 기준 요약 (교과 9)

| 일차 | 학습 범위 |
|---|---|
| 1 | 검사문제 설계, 이미지·영상·IP Webcam 입력, ROI 선택·저장 |
| 2 | 영상 품질 관찰, Color Space, 밝기·대비·Gamma·CLAHE·필터·Sharpen, Threshold/Otsu 비교 |
| 3 | 병뚜껑 Binary 정리, Morphology·Contour, Area/Area Ratio/Count/BBox/Center 측정, Candidate Rule, Batch Test와 Mini Challenge |
| 4~5 | 광천김 로고: Matching 방법 비교 후 별도 Calibration·Rule Freeze·Test·실패 분석 |
| 6 | 제조 문자 OCR·문자 형식 및 Expected 값 검사 |
| 7~8 | MVTec bottle Anomaly Detection, One-shot/Few-shot 비교 |
| 9 | 버전·재현성·실험·Drift·Hybrid 결과 관리 |
| 10 | 검증된 OCR Rule을 FastAPI/Web/다중기기에 연결 |

**병뚜껑 개선 범위 주의:** 1~3일차는 주어진 조건에서 방법을 적용하고 Candidate Rule을 시험하는 단계다. 뒤 수업의 4~5일차 보정은 광천김 로고 대상이며, 9일차에서 병뚜껑 Rule이 이력 관리 예로 언급되어도 병뚜껑 분리 품질을 튜닝하는 과정은 아니다. 이 프로젝트에서 더 좋은 캡 분리를 목표로 할 경우 별도 개선 실험으로 다룬다. 수업의 교재 성능 수치를 실제 휴대폰 입력 성능으로 간주하지 않는다.

## 확인된 실제 상태 (2026-10-27)

- `sub9/src`에 `00_check_env.py`~`22_cap_batch_test.py`, `cap_inspector.py`, `fastapi_cap_app.py`가 있다. `web/cap_inspection.html`이 있고 Day02/Day03 보고서와 출력물이 존재한다.
- 프로젝트에 `samples/day01`, `samples/day02`, `samples/day03` 자료와 `outputs`, `reports`가 있다. Day02 Challenge에는 CLAHE + Median Blur와 Otsu 비교/실패 기록이 있다. 이 결과는 로고 대상 4일차·5일차 Calibration과 별개다.
- `src/cap_inspector.py`는 Gray + Otsu 역이진화, 3x3 타원형 Opening/Closing, 면적 비율 0.001 미만 Contour 제외, 최대 Contour의 Area Ratio, `cap_on`/`cap_off` 기준 중간값으로 만든 규칙을 사용한다. 현재 값과 구현은 수정 전 다시 파일을 확인한다.
- `reports/day03_reference_features.csv`는 `cap_on`/`cap_off` 각 1장의 측정값, `reports/day03_inspection_results.csv`는 Batch 이미지별 결과를 기록한다. 현재 CSV에는 Batch 4개가 모두 맞은 것으로 기록되어 있으나, 적은 수의 해당 샘플 결과를 일반 성능 보장으로 확대 해석하지 않는다.
- `reports/day03_rule_analysis.md`에는 사용자가 확인한 아이폰 OctoStream RTSP → FastAPI/OpenCV → 브라우저 수동 ROI → Area Ratio Rule 실시간 확장 내용이 기록돼 있다. 수동 사각형은 자동 객체 검출 BBox가 아니다.
- 해당 실시간 시험에서 캡/병이 빠져도 OK가 남거나 캡이 있어도 NG가 유지되는 경우, 카메라/ROI 위치 조정 후 결과가 달라진 경우가 관찰됐다. 반복 횟수, ROI 비율, 지연 시간, 정확한 촬영 거리·각도 등의 정량 기록은 없다. 원인을 단정하지 말고 고정 촬영 조건에서 반복 기록을 추가한다.
- 보고서는 `python -m pytest tests/test_inspector.py -q`에서 2 passed라고 기록한다. 이는 현재 새로 실행한 테스트가 아니며, 실시간 카메라 동작과 구분한다.
- 현재 수업 프로젝트 상태는 1~3일차 및 실시간 확장까지 확인된 상태다. 4일차 이후 구현 완료 여부는 미확인이다.

## 실행·경로 참고

- 프로젝트 루트에서 실행: `cd /home/user27/ai_vision/sub9`
- 가상환경은 `/home/user27/ai_vision/.venv`를 사용 중인 것으로 확인됐다. 실행 직전 실제 Python/OpenCV 환경을 확인한다.
- FastAPI 실시간 코드와 스트림 URL은 실행 전 현재 사용자 설정을 확인한다. URL, IP, 포트는 네트워크 구성에 따라 달라지므로 문서에 본 적 있는 값을 임의로 복구하지 않는다.

## 자료 기준

- 주요 수업 자료: Obsidian `교과 9 openCV 규칙기반 머신비전/10일 수업/1일차~10일차` 문서
- 작업 지침: `/home/user27/ai_vision/AGENTS.md`
- 현재 프로젝트 README: `/home/user27/ai_vision/sub9/README.md`
- 현재 기준 보고서: `sub9/reports/day02_parameter_table.csv`, `day02_preprocess_reason.md`, `day03_reference_features.csv`, `day03_inspection_results.csv`, `day03_rule_analysis.md`


## Day07 확인 상태 (2026-11-03)

- 수업문서는 Obsidian의 교과 9/10일 수업/7일차_Anomaly_Detection_MVTec_bottle.md를 기준으로 확인했다.
- sub9/src/50~58 및 day07_anomaly_core.py, 분할된 MVTec bottle 이미지, Normal Reference, Frozen Rule, Test 점수·지표, FP/FN 이미지, 대표 Heatmap 결과가 이미 있었다.
- 이번 작업에서 문서에 있었으나 없던 src/59_day07_make_challenge_variants.py, src/60_day07_run_challenge.py, src/61_day07_mini_challenge.py를 작성하고 실행했다. Challenge/Mini Challenge 이미지와 CSV/Markdown 결과도 생성했다.
- 현재 실제 Rule은 configs/day07_anomaly_rules.json의 Threshold 0.067458이다. 수업문서 예시의 0.067469와 다르므로 프로젝트의 Frozen Rule을 사용하고 차이를 보고서에 기록했다. Test 결과는 Accuracy 0.9277, Precision 0.9672, Recall 0.9365, TP 59 / TN 18 / FP 2 / FN 4이다.
- Day07 결과는 sub9/README.md와 sub9/reports/day07_*를 참고한다. Mini Challenge의 실행 전 개인 예상은 기록되지 않아 사후에 만들어 넣지 않았다.
- /home/user27/ai_vision/sub9는 Git 저장소가 아니므로 수업문서의 Git 기록 단계는 수행할 수 없다. Git을 임의로 초기화하지 않는다.
- Day08 이후 진행 상태는 확인하지 않았다.


## Day08 확인 상태 (2026-11-03)

- 수업문서는 Obsidian의 교과 9/10일 수업/8일차_ZeroShot_OneShot_FewShot_DefectGeneration.md를 기준으로 확인했다. 현재 실제 파일과 결과가 있는 범위는 62~67번까지였고, 68~69번 및 Cut-Paste 공통 기능 파일은 없었다.
- 이번 작업에서 src/68_day08_compare_methods.py, src/day08_cutpaste_core.py, src/69_day08_make_cutpaste_defects.py를 작성하고 실행했다. 비교 CSV는 문서 예시와 같은 One-shot 85%, Few-shot 90% 결과를 냈다. 기존 Rule·Prototype·Query 결과는 수정하지 않았다.
- Mini Challenge 요구에 따라 src/70_day08_compare_support_counts.py와 src/71_day08_make_contamination_challenge.py를 추가했다. Support 1/3/5 결과는 Accuracy 0.70/0.80/0.90, FP 1/0/0, FN 5/4/2였다.
- broken_small Synthetic 20장과 contamination Synthetic 5장, 각각의 Metadata CSV를 생성했다. outputs/day08/qa_review/contact_sheet.jpg는 확인을 돕는 미리보기다.
- reports/day08_synthetic_quality_check.md의 후보 분류는 AI의 사전 시각 검토이며 사람의 최종 QA가 아니다. 사람은 Keep/Reject 후보 및 contamination의 자연스러운/어색한 예시를 직접 확인해 확정해야 한다. Mini Challenge의 실행 전 개인 예상도 기록이 없어 사후에 작성하지 않았다.
- 수업문서는 PART7이 46~50 이후 PART9가 56~63으로 이어져 51~55번의 제목·내용이 보이지 않는다. 누락 내용을 임의로 만들어 넣지 않았다.
- reports/day08_method_comparison.csv, day08_support_count_comparison.csv, day08_defect_metadata.csv, day08_mini_challenge_contamination_metadata.csv 및 README의 Day08 절을 확인한다.
- /home/user27/ai_vision/sub9는 Git 저장소가 아니어서 Git commit/push 단계는 하지 않았다. Git을 임의로 초기화하지 않는다.
- Day09 이후 진행 상태는 확인하지 않았다.
