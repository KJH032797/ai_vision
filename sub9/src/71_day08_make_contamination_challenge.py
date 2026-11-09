"""Mini Challenge용 contamination 합성 이미지 5장을 만든다."""
from pathlib import Path

from day08_cutpaste_core import generate_synthetic_set


ROOT = Path(__file__).resolve().parents[1]
NORMAL_DIR = ROOT / "samples/day08/mini_challenge/normal"
DEFECT_ROOT = ROOT / "samples/day08/mini_challenge/defect_source/contamination"
OUTPUT_DIR = ROOT / "outputs/day08/mini_challenge/contamination"
METADATA_PATH = ROOT / "reports/day08_mini_challenge_contamination_metadata.csv"


def main() -> None:
    rows = generate_synthetic_set(
        normal_dir=NORMAL_DIR,
        defect_image_dir=DEFECT_ROOT / "images",
        defect_mask_dir=DEFECT_ROOT / "masks",
        output_dir=OUTPUT_DIR,
        metadata_path=METADATA_PATH,
        defect_type="contamination",
        count=5,
        seed=42,
        scale_range=(0.6, 1.0),
        angle_range=(-10.0, 10.0),
    )
    print("=" * 70)
    print("DAY08 CONTAMINATION MINI CHALLENGE")
    print("Defect Type      : contamination")
    print("Generated Images :", len(rows))
    print("Output           :", OUTPUT_DIR.relative_to(ROOT))
    print("Metadata         :", METADATA_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
