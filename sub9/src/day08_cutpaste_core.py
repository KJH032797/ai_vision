"""Ground Truth Mask를 이용해 실제 결함 Patch를 합성하는 공통 함수."""
import csv
import random
from pathlib import Path

import cv2
import numpy as np


def extract_patch(image_path, mask_path):
    image = cv2.imread(str(image_path))
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"결함 원본 이미지를 읽지 못했습니다: {image_path}")
    if mask is None:
        raise FileNotFoundError(f"Ground Truth Mask를 읽지 못했습니다: {mask_path}")
    if image.shape[:2] != mask.shape[:2]:
        raise ValueError(f"이미지와 Mask 크기가 다릅니다: {image_path}, {mask_path}")

    binary = np.where(mask > 0, 255, 0).astype(np.uint8)
    points = cv2.findNonZero(binary)
    if points is None:
        raise ValueError(f"Mask에 결함 픽셀이 없습니다: {mask_path}")

    x, y, width, height = cv2.boundingRect(points)
    patch = image[y:y + height, x:x + width].copy()
    patch_mask = binary[y:y + height, x:x + width].copy()
    return patch, patch_mask


def rotate_pair(patch, mask, angle):
    height, width = patch.shape[:2]
    center = (width / 2.0, height / 2.0)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_patch = cv2.warpAffine(
        patch, matrix, (width, height),
        flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT,
    )
    rotated_mask = cv2.warpAffine(
        mask, matrix, (width, height),
        flags=cv2.INTER_NEAREST, borderValue=0,
    )
    return rotated_patch, rotated_mask


def paste_patch(
    background,
    patch,
    mask,
    rng,
    scale_range=(0.7, 1.2),
    angle_range=(-15.0, 15.0),
):
    result = background.copy()
    scale = rng.uniform(*scale_range)
    angle = rng.uniform(*angle_range)
    new_width = max(4, int(patch.shape[1] * scale))
    new_height = max(4, int(patch.shape[0] * scale))
    patch = cv2.resize(patch, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    mask = cv2.resize(mask, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    patch, mask = rotate_pair(patch, mask, angle)

    image_h, image_w = result.shape[:2]
    patch_h, patch_w = patch.shape[:2]
    if patch_w >= image_w or patch_h >= image_h:
        raise ValueError("Defect Patch가 정상 이미지보다 큽니다.")

    x_min, x_max = int(image_w * 0.25), int(image_w * 0.75) - patch_w
    y_min, y_max = int(image_h * 0.10), int(image_h * 0.90) - patch_h
    if x_max <= x_min:
        x_min, x_max = 0, image_w - patch_w
    if y_max <= y_min:
        y_min, y_max = 0, image_h - patch_h

    x = rng.randint(x_min, x_max)
    y = rng.randint(y_min, y_max)
    roi = result[y:y + patch_h, x:x + patch_w]

    alpha = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (3, 3), 0)[..., None]
    blended = patch.astype(np.float32) * alpha + roi.astype(np.float32) * (1.0 - alpha)
    result[y:y + patch_h, x:x + patch_w] = np.clip(blended, 0, 255).astype(np.uint8)

    info = {
        "x": x,
        "y": y,
        "width": patch_w,
        "height": patch_h,
        "rotation": round(angle, 2),
        "scale": round(scale, 3),
    }
    return result, info


def generate_synthetic_set(
    normal_dir,
    defect_image_dir,
    defect_mask_dir,
    output_dir,
    metadata_path,
    defect_type,
    count,
    seed,
    scale_range=(0.7, 1.2),
    angle_range=(-15.0, 15.0),
):
    normal_files = sorted(Path(normal_dir).glob("*.png"))
    defect_files = sorted(Path(defect_image_dir).glob("*.png"))
    if not normal_files:
        raise FileNotFoundError(f"Normal Target 이미지가 없습니다: {normal_dir}")
    if not defect_files:
        raise FileNotFoundError(f"Defect Source 이미지가 없습니다: {defect_image_dir}")
    if count <= 0:
        raise ValueError("생성할 이미지 수는 1 이상이어야 합니다.")

    output_dir = Path(output_dir)
    metadata_path = Path(metadata_path)
    existing = list(output_dir.glob("synthetic_*.png")) if output_dir.exists() else []
    if existing or metadata_path.exists():
        raise FileExistsError(
            "기존 합성 결과를 보호하기 위해 새 출력 경로를 사용하세요: "
            f"{output_dir}, {metadata_path}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    rows = []

    for index in range(count):
        normal_path = rng.choice(normal_files)
        defect_path = rng.choice(defect_files)
        mask_path = Path(defect_mask_dir) / f"{defect_path.stem}_mask.png"
        if not mask_path.exists():
            raise FileNotFoundError(f"짝이 되는 Mask가 없습니다: {mask_path}")

        background = cv2.imread(str(normal_path))
        if background is None:
            raise OSError(f"Normal 이미지를 읽지 못했습니다: {normal_path}")
        patch, patch_mask = extract_patch(defect_path, mask_path)
        synthetic, info = paste_patch(
            background, patch, patch_mask, rng,
            scale_range=scale_range, angle_range=angle_range,
        )

        output_name = f"synthetic_{index:03d}.png"
        output_path = output_dir / output_name
        if not cv2.imwrite(str(output_path), synthetic):
            raise OSError(f"Synthetic 이미지를 저장하지 못했습니다: {output_path}")
        rows.append(
            {
                "synthetic_file": output_name,
                "source_normal": normal_path.name,
                "source_defect": defect_path.name,
                "defect_type": defect_type,
                "seed": seed,
                **info,
            }
        )

    with metadata_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows
