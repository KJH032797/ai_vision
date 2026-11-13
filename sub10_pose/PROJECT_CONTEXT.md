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
