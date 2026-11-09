"""Few-shot Support 1/3/5장 실험을 같은 Common Query에서 비교한다."""
import csv
from pathlib import Path

from day08_feature_core import (
    build_prototype,
    cosine_similarity,
    create_feature_model,
    extract_feature,
)


ROOT = Path(__file__).resolve().parents[1]
SUPPORT_ROOT = ROOT / "samples/day08/few_shot/support"
QUERY_ROOT = ROOT / "samples/day08/common_query"
OUTPUT_PATH = ROOT / "reports/day08_support_count_comparison.csv"
SUPPORT_COUNTS = (1, 3, 5)


def main() -> None:
    normal_support_paths = sorted((SUPPORT_ROOT / "normal").glob("*.png"))
    anomaly_support_paths = sorted((SUPPORT_ROOT / "anomaly").glob("*.png"))
    normal_query_paths = sorted((QUERY_ROOT / "normal").glob("*.png"))
    anomaly_query_paths = sorted((QUERY_ROOT / "anomaly/broken_small").glob("*.png"))

    for name, paths in (
        ("Normal Support", normal_support_paths),
        ("Anomaly Support", anomaly_support_paths),
        ("Normal Query", normal_query_paths),
        ("Anomaly Query", anomaly_query_paths),
    ):
        if not paths:
            raise FileNotFoundError(f"{name} 이미지가 없습니다.")
    if len(normal_support_paths) < max(SUPPORT_COUNTS):
        raise ValueError("Support 수 비교에 필요한 Normal Support가 부족합니다.")
    if len(anomaly_support_paths) < max(SUPPORT_COUNTS):
        raise ValueError("Support 수 비교에 필요한 Anomaly Support가 부족합니다.")

    model = create_feature_model()
    feature_cache = {}
    all_paths = (
        normal_support_paths + anomaly_support_paths
        + normal_query_paths + anomaly_query_paths
    )
    for path in all_paths:
        feature_cache[path] = extract_feature(model, path)

    queries = [
        (path, "Normal", f"normal/{path.name}")
        for path in normal_query_paths
    ] + [
        (path, "Anomaly", f"anomaly/broken_small/{path.name}")
        for path in anomaly_query_paths
    ]

    rows = []
    for support_count in SUPPORT_COUNTS:
        normal_prototype = build_prototype(
            [feature_cache[path] for path in normal_support_paths[:support_count]]
        )
        anomaly_prototype = build_prototype(
            [feature_cache[path] for path in anomaly_support_paths[:support_count]]
        )

        tp = tn = fp = fn = 0
        for path, actual, _sample_id in queries:
            feature = feature_cache[path]
            normal_similarity = cosine_similarity(feature, normal_prototype)
            anomaly_similarity = cosine_similarity(feature, anomaly_prototype)
            predicted = (
                "Normal"
                if normal_similarity >= anomaly_similarity
                else "Anomaly"
            )
            if actual == "Anomaly" and predicted == "Anomaly":
                tp += 1
            elif actual == "Normal" and predicted == "Normal":
                tn += 1
            elif actual == "Normal":
                fp += 1
            else:
                fn += 1

        total = tp + tn + fp + fn
        rows.append(
            {
                "support_per_class": support_count,
                "normal_support": support_count,
                "anomaly_support": support_count,
                "query_samples": total,
                "accuracy": round((tp + tn) / total, 4) if total else 0.0,
                "fp": fp,
                "fn": fn,
                "tp": tp,
                "tn": tn,
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print("DAY08 SUPPORT COUNT CHALLENGE")
    for row in rows:
        print(
            f"Support {row['support_per_class']}: "
            f"Accuracy={row['accuracy']:.4f}, FP={row['fp']}, FN={row['fn']}"
        )
    print("Saved:", OUTPUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
