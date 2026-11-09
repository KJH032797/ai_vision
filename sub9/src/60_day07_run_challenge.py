"""Frozen Day07 Rule을 바꾸지 않고 Challenge 변형 이미지를 검사한다."""
import csv
import json
from pathlib import Path

from day07_anomaly_core import (
    anomaly_score,
    create_backbone,
    extract_features,
    load_reference,
)


ROOT = Path(__file__).resolve().parents[1]
VARIANT_DIR = ROOT / "samples/day07/challenge/variants"
REFERENCE_PATH = ROOT / "artifacts/day07/normal_reference.npz"
RULE_PATH = ROOT / "configs/day07_anomaly_rules.json"
OUTPUT_CSV = ROOT / "reports/day07_challenge_results.csv"


def main() -> None:
    for path in (VARIANT_DIR, REFERENCE_PATH, RULE_PATH):
        if not path.exists():
            raise FileNotFoundError(f"필요한 파일 또는 폴더가 없습니다: {path}")

    rules = json.loads(RULE_PATH.read_text(encoding="utf-8"))
    threshold = float(rules["anomaly_threshold"])
    reference_vector, _ = load_reference(REFERENCE_PATH)
    model = create_backbone()

    rows = []
    for image_path in sorted(VARIANT_DIR.glob("*.png")):
        vector, _ = extract_features(model, image_path)
        score = anomaly_score(vector, reference_vector)
        predicted = "Anomaly" if score > threshold else "Normal"
        rows.append(
            {
                "file": image_path.name,
                "actual": "Normal",
                "anomaly_score": round(score, 6),
                "threshold": round(threshold, 6),
                "predicted": predicted,
                "result": "FP" if predicted == "Anomaly" else "PASS",
            }
        )

    if not rows:
        raise RuntimeError(f"검사할 Challenge 이미지가 없습니다: {VARIANT_DIR}")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print("=" * 70)
    print("DAY07 CHALLENGE")
    print("Threshold:", threshold)
    for row in rows:
        print(
            row["file"],
            "score=", row["anomaly_score"],
            "predicted=", row["predicted"],
            "result=", row["result"],
        )
    print("Saved:", OUTPUT_CSV.relative_to(ROOT))


if __name__ == "__main__":
    main()
