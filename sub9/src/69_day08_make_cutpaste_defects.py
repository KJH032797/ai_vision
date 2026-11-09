"""broken_small Cut-Paste Synthetic Defect 20장을 생성한다."""
from pathlib import Path

from day08_cutpaste_core import generate_synthetic_set


ROOT = Path(__file__).resolve().parents[1]
NORMAL_DIR = ROOT / "samples/day08/cutpaste/normal"
DEFECT_ROOT = ROOT / "samples/day08/cutpaste/defect_source/broken_small"
OUTPUT_DIR = ROOT / "outputs/day08/cutpaste/generated"
METADATA_PATH = ROOT / "reports/day08_defect_metadata.csv"


def main() -> None:
    rows = generate_synthetic_set(
        normal_dir=NORMAL_DIR,
        defect_image_dir=DEFECT_ROOT / "images",
        defect_mask_dir=DEFECT_ROOT / "masks",
        output_dir=OUTPUT_DIR,
        metadata_path=METADATA_PATH,
        defect_type="broken_small",
        count=20,
        seed=42,
        scale_range=(0.7, 1.2),
        angle_range=(-15.0, 15.0),
    )
    print("=" * 70)
    print("DAY08 CUT-PASTE DEFECT GENERATION")
    print("Defect Type      : broken_small")
    print("Generated Images :", len(rows))
    print("Output           :", OUTPUT_DIR.relative_to(ROOT))
    print("Metadata         :", METADATA_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
