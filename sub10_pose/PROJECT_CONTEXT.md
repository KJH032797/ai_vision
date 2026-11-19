# 교과 10 Pose 프로젝트 컨텍스트

## 위치·목표
- 프로젝트: /home/user27/ai_vision/sub10_pose. 사용자가 말한 sub10의 실제 폴더명은 sub10_pose다.
- 목적: YOLO Pose COCO17로 이미지·영상·웹캠의 관절을 추출하고 입력 품질을 확인해 이후 관절각도·Frame Feature·Action Sequence에 연결한다.
- Obsidian 수업자료: 교과 10 자세추정/교과10_자세추정.md 및 10일 수업 1·2일차 문서.
- /home/user27/ai_vision/AGENTS.md와 PROJECT_CONTEXT.md는 교과9 중심이다. 교과9 세부 요구사항을 교과10의 기준으로 간주하지 않는다.

## 코드 구조
- configs/project.json: yolo11n-pose.pt, imgsz=640, person_confidence=.25, keypoint_confidence=.50, device=auto.
- src/common.py: JSON 설정 로드, GPU/CPU 선택.
- src/pose_utils.py: COCO17 관절명·Skeleton 연결, keypoint confidence 상태(>=.50 VALID, >=.30 WARNING, 그 미만 LOW).
- scripts/06_check_day02_data.py: 필수 이미지 6개 존재·읽기 확인.
- scripts/07_pose_image_detail.py: 단일 이미지 추론, 표시 이미지 저장, 관절별 pixel/이미지 정규화 좌표/confidence/상태 CSV 저장.
- scripts/08_draw_skeleton_quality.py: threshold 이상 관절만 Skeleton으로 그려 저장.
- scripts/09_compare_pose_images.py: 이미지별 인원, 대표 BBox 비율, 평균 관절 confidence, 저신뢰 관절 수를 비교 CSV로 저장.
- scripts/10_pose_video_quality.py: 영상별 frame 추론, 표시 영상과 frame·관절 CSV 저장.
- 입력 6장: front, arms_up, side, partial_body, occlusion, distance_far. 비디오: data/day02/videos/pose_quality_demo.mp4.

## 확인 상태 (2026-11-13)
- 06~10 소스 파일이 존재한다. reports/day02의 front_keypoints.csv(17행), image_quality_summary.csv(6행), pose_quality_demo_frame_quality.csv(60행), pose_quality_demo_keypoints.csv로 07·09·10 결과 저장을 확인했다. 06 실행은 저장 결과만으로 확인할 수 없다.
- 6장 모두 사람 1명. front 평균 관절 confidence .9754/저신뢰 0개; distance_far BBox 이미지 비율 .1489/평균 .9710/저신뢰 0개; side 평균 .7541/저신뢰 4개; partial_body 평균 .9073/저신뢰 2개; occlusion 평균 .9533인데도 저신뢰 1개.
- 비디오 산출물은 60 frames(약 1.97초). 전 frame에서 사람 1명, 전 frame에서 기준 미달 관절 1개 이상. 평균 confidence 최저 frame24(약 .767초) .7787; 최저 관절 left_eye .2467.
- 70/90/95 threshold별 이미지, 6장 비교 이미지, 결과 mp4 파일은 존재하나 미디어 자체는 열어보지 않았다. CSV만 확인했다. 코드를 실행하거나 테스트하지 않았다.
- Confidence는 모델이 낸 추정 신뢰도이지 ground-truth 좌표 정확도가 아니다. BBox confidence(사람 검출)와 keypoint confidence(관절별 추정)를 구분한다. x/이미지너비, y/이미지높이 정규화는 사람 BBox 기준 정규화가 아니다. threshold는 표시·분류 기준이지 모델 개선값이 아니다.
- Day02는 모델 학습이 아니라 입력 조건별 Pose 품질을 수치로 읽는 수업이다. Day03 각도·Feature 전에 불안정한 관절을 찾는다.

## 교과12와 사용자 촬영정보
- 교과12는 VICON 기반 3D Bone 좌표 JSON 흐름이고, 교과10은 RGB의 YOLO 2D COCO17 흐름이다. 직접 붙는 코드는 아니다. 연결하려면 관절 매핑, 카메라 좌표 투영, 시간/FPS 정렬이 필요하다.
- 사용자는 육아 상황의 올바른 동작·자세를 시도한 스튜디오 촬영 데이터가 D:\dev\1001~\Obsidian\2조\모션\Motion_VIsol에 있다고 알려줬다. 파일 정리·구성·코드 연결은 미확인이고 원본은 열지 않았다.
- WSL group2-project의 이미지는 물론 같은 이름의 txt도 열지 않는다.

## 다음에 확인할 사항
1. 실제 결과 이미지를 보며 70/90/95 기준 차이를 확인한다.
2. frame24 부근을 영상에서 검토해 left_eye 저신뢰 원인을 확인한다.
3. Day02 팀 Mini Challenge 수행 여부를 사용자에게 확인하고 수행 사실을 임의로 가정하지 않는다.
4. Day03 코드에서 저신뢰 관절을 각도·Feature 계산에 어떻게 처리하는지 확인한다.

## Latest handoff (2026-11-19)

- **작업:** 교과 10 4~6일차 파이프라인 그림을 위한 프로젝트 진행 상태를 실제 파일과 대조하고, 누락된 Day06 비교·최종평가 코드를 보완했다.
- **교과 요구사항:** Day05는 18개 Clip의 Keypoint 추출, 자동 QA와 Human Review, 승인 Manifest, Subject-wise Split 및 누수 확인을 수행한다. Day06은 Keypoint를 Sequence Feature로 변환하고 Baseline 학습·Validation·비교·최종 Test를 수행한다. 파이프라인 그림에는 실제 코드와 입력·출력 관계를 근거로 사용한다.
- **Day05 확인:** scripts/25_check_day05_data.py를 실행해 18개 MP4 모두 읽기 성공을 확인하고 reports/day05/tables/video_inventory.csv를 갱신했다. 기존 QA 검토표는 18행이며 AUTO_PASS/PASS 13개, CHECK/PASS 5개다. approved_clip_manifest.csv와 Train/Validation/Test는 각각 18개 승인 Clip, 6개 Clip씩이며 S01/S02/S03로 분리되어 있다. scripts/31_check_split_leakage.py 실행에서 Subject overlap, Clip overlap 없음 및 Action Coverage 확인으로 통과했다.
- **Day06 입력·Baseline 확인:** scripts/33_check_day06_inputs.py 통과; reports/day06/tables/day06_input_check.csv 갱신. 34번 Sequence CSV는 Train/Validation/Test 각 6행이고, rf_training_info.json의 설정(30 Step, 1,140 Feature, n_estimators=300, max_depth=null, random_state=42)이 현재 configs/day06_baseline.json과 일치한다. 35~37번 Baseline 학습·Validation·오분류 산출물이 존재한다. 현재 Validation은 Accuracy 0.5000, Macro F1 0.4444다.
- **이번에 복원·실행한 코드:** Obsidian 6일차 수업 문서에서 해당 코드 블록을 가져와 scripts/38_compare_static_vs_sequence.py, scripts/39_compare_feature_sets.py, scripts/40_evaluate_test.py를 만들고 실행했다. 38번 S02 Validation 결과: Static 38-D Accuracy 0.6667 / Macro F1 0.5556, Sequence 1,140-D 0.5000 / 0.4444. 39번: Coordinates+Angles 1,140-D 0.5000 / 0.4444, Coordinates Only 1,020-D 1.0000 / 1.0000. Test는 튜닝에 쓰지 않았다.
- **최종 Test:** 40번은 수업 문서대로 기존 Baseline 모델을 S03 Test에 적용했다. 6/6 정답, Accuracy 1.0000, Macro F1 1.0000. Test는 각 Action당 1 Clip뿐인 소규모 교육 데이터 결과이며 일반화 성능으로 해석하지 않는다.
- **변경·생성 파일:** scripts/38_compare_static_vs_sequence.py, scripts/39_compare_feature_sets.py, scripts/40_evaluate_test.py; reports/day06/experiments/static_vs_sequence.csv, reports/day06/experiments/feature_set_comparison.csv, reports/day06/metrics/test_metrics.txt, reports/day06/metrics/test_predictions.csv, reports/day06/confusion/test_confusion_matrix.png; Day05 inventory 및 Day06 input-check CSV 갱신.
- **미완료/범위:** 이 작업에서는 파이프라인 그림 자체, Day05의 별도 frame-split leakage 시연(32번), 학생이 직접 가설을 정하는 Mini Challenge 및 수업 마무리 문서를 작성하지 않았다. 이들은 이번 파이프라인 그림의 필수 실행 경로와 구분한다. 5일차 Challenge 영상이 원본 A006 영상과 동일하다는 기존 확인 사항도 유지한다.
- **다음 단계:** 이 handoff와 4~6일차 수업 문서를 근거로 파이프라인 순서를 정리하고, 사용자가 요청한 그림을 만든다. 먼저 확인할 파일은 scripts/25_check_day05_data.py, scripts/26_extract_keypoint_dataset.py, scripts/27_keypoint_qa.py~scripts/31_check_split_leakage.py, scripts/33_check_day06_inputs.py~scripts/40_evaluate_test.py, src/sequence_utils.py다.
