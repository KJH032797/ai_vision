"""다른 정상 Test 한 장을 직접 정한 조건으로 변형하고 Frozen Rule로 검사한다."""
import json
from pathlib import Path

import cv2

from day07_anomaly_core import (
    anomaly_score,
    create_backbone,
    extract_features,
    load_reference,
)


ROOT = Path(__file__).resolve().parents[1]
NORMAL_DIR = ROOT / "samples/day07/test/normal"
OUTPUT_ROOT = ROOT / "samples/day07/mini_challenge"
VARIANT_DIR = OUTPUT_ROOT / "variants"
REFERENCE_PATH = ROOT / "artifacts/day07/normal_reference.npz"
RULE_PATH = ROOT / "configs/day07_anomaly_rules.json"

# 수업 예시의 Mini Challenge 조건
DARK_ALPHA = 0.75
BLUR_KERNEL = 7
ROTATION_ANGLE = 10.0


def save_image(path: Path, image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise OSError(f"이미지를 저장하지 못했습니다: {path}")


def main() -> None:
    normal_files = sorted(NORMAL_DIR.glob("*.png"))
    if len(normal_files) < 2:
        raise FileNotFoundError("Mini Challenge용 Normal Test 이미지가 2장 필요합니다.")
    if not REFERENCE_PATH.exists() or not RULE_PATH.exists():
        raise FileNotFoundError("Normal Reference 또는 Frozen Rule 파일이 없습니다.")

    source_path = normal_files[1]
    image = cv2.imread(str(source_path))
    if image is None:
        raise OSError(f"이미지를 읽지 못했습니다: {source_path}")
    height, width = image.shape[:2]

    VARIANT_DIR.mkdir(parents=True, exist_ok=True)
    variants = {
        "mini_dark.png": cv2.convertScaleAbs(image, alpha=DARK_ALPHA, beta=0),
        "mini_blur.png": cv2.GaussianBlur(
            image, (BLUR_KERNEL, BLUR_KERNEL), 0
        ),
    }
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, ROTATION_ANGLE, 1.0)
    variants["mini_rotation.png"] = cv2.warpAffine(
        image, rotation_matrix, (width, height), borderMode=cv2.BORDER_REFLECT
    )
    for name, variant in variants.items():
        save_image(VARIANT_DIR / name, variant)

    rules = json.loads(RULE_PATH.read_text(encoding="utf-8"))
    threshold = float(rules["anomaly_threshold"])
    reference_vector, _ = load_reference(REFERENCE_PATH)
    model = create_backbone()

    print("=" * 70)
    print("DAY07 MINI CHALLENGE")
    print("Source:", source_path.relative_to(ROOT))
    print("Threshold:", threshold)
    print(
        "조건: Dark alpha=", DARK_ALPHA,
        ", Blur kernel=", BLUR_KERNEL,
        ", Rotation angle=", ROTATION_ANGLE,
        sep="",
    )
    for image_path in sorted(VARIANT_DIR.glob("*.png")):
        vector, _ = extract_features(model, image_path)
        score = anomaly_score(vector, reference_vector)
        predicted = "Anomaly" if score > threshold else "Normal"
        result = "FP" if predicted == "Anomaly" else "PASS"
        print(
            image_path.name,
            "score=", round(score, 6),
            "predicted=", predicted,
            "result=", result,
        )
    print("변형 이미지 저장:", VARIANT_DIR.relative_to(ROOT))


if __name__ == "__main__":
    main()
