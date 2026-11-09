from pathlib import Path

import cv2


image_path = Path("samples/day02/challenge.jpg")
output_dir = Path("outputs/day02/challenge")
output_dir.mkdir(parents=True, exist_ok=True)

image = cv2.imread(str(image_path))
if image is None:
    raise FileNotFoundError(f"이미지를 읽지 못했습니다: {image_path}")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 지역 대비를 개선합니다. clipLimit를 높이면 대비와 노이즈가 함께 강해질 수 있습니다.
clahe_clip_limit = 2.0
clahe = cv2.createCLAHE(
    clipLimit=clahe_clip_limit,
    tileGridSize=(8, 8),
)
enhanced = clahe.apply(gray)

# 노이즈를 줄입니다. 커널은 홀수여야 하고, 키울수록 작은 홈도 흐려질 수 있습니다.
median_kernel = 7
result = cv2.medianBlur(enhanced, median_kernel)

result_path = output_dir / "challenge_result.jpg"
cv2.imwrite(str(result_path), result)

# 현재 입력 ROI에서는 병뚜껑 면이 배경보다 어두워 역이진화를 사용합니다.
# 수업 문서의 '밝은 병뚜껑' 예시와 실제 입력의 명암 관계가 다릅니다.
threshold_type = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
original_threshold, original_otsu = cv2.threshold(
    gray,
    0,
    255,
    threshold_type,
)
result_threshold, result_otsu = cv2.threshold(
    result,
    0,
    255,
    threshold_type,
)

cv2.imwrite(
    str(output_dir / "challenge_original_otsu.jpg"),
    original_otsu,
)
cv2.imwrite(
    str(output_dir / "challenge_result_otsu.jpg"),
    result_otsu,
)

print("입력:", image_path)
print("전처리 결과:", result_path)
print("원본 Otsu 임계값:", original_threshold)
print("전처리 Otsu 임계값:", result_threshold)
print("Otsu 결과:", output_dir / "challenge_result_otsu.jpg")
