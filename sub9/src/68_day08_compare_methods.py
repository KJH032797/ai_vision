"""One-shot과 Few-shot의 기존 Query 결과를 같은 지표로 비교한다."""
import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ONE_PATH = ROOT / "reports/day08_one_shot_results.csv"
FEW_PATH = ROOT / "reports/day08_fewshot_results.csv"
OUTPUT_PATH = ROOT / "reports/day08_method_comparison.csv"


def calculate_metrics(frame: pd.DataFrame) -> dict:
    actual = frame["actual"]
    predicted = frame["predicted"]

    tp = int(((actual == "Anomaly") & (predicted == "Anomaly")).sum())
    tn = int(((actual == "Normal") & (predicted == "Normal")).sum())
    fp = int(((actual == "Normal") & (predicted == "Anomaly")).sum())
    fn = int(((actual == "Anomaly") & (predicted == "Normal")).sum())
    total = tp + tn + fp + fn

    return {
        "samples": total,
        "accuracy": (tp + tn) / total if total else 0.0,
        "anomaly_precision": tp / (tp + fp) if tp + fp else 0.0,
        "anomaly_recall": tp / (tp + fn) if tp + fn else 0.0,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def main() -> None:
    for path in (ONE_PATH, FEW_PATH):
        if not path.exists():
            raise FileNotFoundError(f"결과 CSV가 없습니다: {path}")

    one = pd.read_csv(ONE_PATH)
    few = pd.read_csv(FEW_PATH)
    required = {"sample_id", "actual", "predicted"}

    for name, frame in (("One-shot", one), ("Few-shot", few)):
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"{name} CSV에 필요한 컬럼이 없습니다: {sorted(missing)}")
        if frame["sample_id"].duplicated().any():
            raise ValueError(f"{name} CSV에 중복 sample_id가 있습니다.")

    one_by_id = one.set_index("sample_id")["actual"].sort_index()
    few_by_id = few.set_index("sample_id")["actual"].sort_index()
    if not one_by_id.equals(few_by_id):
        raise RuntimeError("One-shot과 Few-shot의 Common Query 또는 실제 정답이 다릅니다.")

    rows = []
    for method, frame in (("one_shot", one), ("few_shot", few)):
        row = {"method": method, **calculate_metrics(frame)}
        for key in ("accuracy", "anomaly_precision", "anomaly_recall"):
            row[key] = round(row[key], 4)
        rows.append(row)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print("=" * 70)
    print("DAY08 METHOD COMPARISON")
    print("=" * 70)
    for row in rows:
        print(
            f"{row['method']}: samples={row['samples']}, "
            f"accuracy={row['accuracy']:.4f}, "
            f"precision={row['anomaly_precision']:.4f}, "
            f"recall={row['anomaly_recall']:.4f}, "
            f"TP/TN/FP/FN={row['tp']}/{row['tn']}/{row['fp']}/{row['fn']}"
        )
    print("Saved:", OUTPUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
