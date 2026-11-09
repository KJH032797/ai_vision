"""정상 Test 한 장을 고정 조건으로 변형하는 Day07 Challenge 준비 스크립트."""
from pathlib import Path
import shutil

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NORMAL_DIR = ROOT / "samples/day07/test/normal"
CHALLENGE_ROOT = ROOT / "samples/day07/challenge"
SOURCE_DIR = CHALLENGE_ROOT / "source"
VARIANT_DIR = CHALLENGE_ROOT / "variants"


def save_image(path: Path, image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), image):
        raise OSError(f"이미지를 저장하지 못했습니다: {path}")


def main() -> None:
    normal_files = sorted(NORMAL_DIR.glob("*.png"))
    if not normal_files:
        raise FileNotFoundError(f"Normal Test 이미지가 없습니다: {NORMAL_DIR}")

    source_path = normal_files[0]
    image = cv2.imread(str(source_path))
    if image is None:
        raise OSError(f"이미지를 읽지 못했습니다: {source_path}")

    height, width = image.shape[:2]
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    VARIANT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, SOURCE_DIR / source_path.name)

    variants = {
        "normal_dark.png": cv2.convertScaleAbs(image, alpha=0.60, beta=0),
        "normal_bright.png": cv2.convertScaleAbs(image, alpha=1.20, beta=20),
        "normal_blur.png": cv2.GaussianBlur(image, (11, 11), 0),
    }

    shift_matrix = np.float32([[1, 0, 35], [0, 1, 20]])
    variants["normal_shift.png"] = cv2.warpAffine(
        image, shift_matrix, (width, height), borderMode=cv2.BORDER_REFLECT
    )

    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 6.0, 1.0)
    variants["normal_rotation.png"] = cv2.warpAffine(
        image, rotation_matrix, (width, height), borderMode=cv2.BORDER_REFLECT
    )

    for name, variant in variants.items():
        save_image(VARIANT_DIR / name, variant)

    print("Challenge Source:", source_path.relative_to(ROOT))
    print("변형 이미지 5장 저장:", VARIANT_DIR.relative_to(ROOT))


if __name__ == "__main__":
    main()
