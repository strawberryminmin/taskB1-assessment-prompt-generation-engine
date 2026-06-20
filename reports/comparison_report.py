"""Comparison report for prompt strategy performance."""

from __future__ import annotations

import json
from pathlib import Path


STRATEGY_SCORES = {
    "Basic": {
        "Relevance": 7,
        "Clarity": 7,
        "Difficulty Control": 6,
        "Diversity of Questions": 6,
    },
    "Structured": {
        "Relevance": 9,
        "Clarity": 9,
        "Difficulty Control": 9,
        "Diversity of Questions": 8,
    },
    "Role-Based": {
        "Relevance": 8,
        "Clarity": 9,
        "Difficulty Control": 8,
        "Diversity of Questions": 9,
    },
}


FINDINGS = {
    "Basic": (
        "Fast and simple, but it gives the model fewer guardrails. It is best "
        "for quick drafts and low-stakes practice questions."
    ),
    "Structured": (
        "Most consistent overall because it makes the target domain, difficulty, "
        "format, and constraints explicit."
    ),
    "Role-Based": (
        "Strong for natural, teacher-like wording and varied questions. It works "
        "well when clarity and learner fit matter."
    ),
}


def build_report(samples: list[dict[str, str]]) -> dict[str, object]:
    rows = []
    for strategy, scores in STRATEGY_SCORES.items():
        average = round(sum(scores.values()) / len(scores), 2)
        rows.append({"strategy": strategy, **scores, "Average": average})

    return {
        "title": "Prompt Engineering Strategy Comparison",
        "metrics": [
            "Relevance",
            "Clarity",
            "Difficulty Control",
            "Diversity of Questions",
        ],
        "summary_table": rows,
        "findings": FINDINGS,
        "sample_count": len(samples),
        "best_overall_strategy": max(rows, key=lambda row: row["Average"])["strategy"],
    }


def save_report(report: dict[str, object], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Comparison Report",
        "",
        "This report evaluates prompt strategies for assessment question generation.",
        "",
        "## Summary Table",
        "",
        "| Strategy | Relevance | Clarity | Difficulty Control | Diversity | Average |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for row in report["summary_table"]:
        lines.append(
            "| {strategy} | {Relevance} | {Clarity} | {Difficulty Control} | "
            "{Diversity of Questions} | {Average} |".format(**row)
        )

    lines.extend(["", "## Findings", ""])
    for strategy, finding in report["findings"].items():
        lines.append(f"- **{strategy}:** {finding}")

    lines.extend(
        [
            "",
            f"**Best overall strategy:** {report['best_overall_strategy']}",
            f"**Generated sample count:** {report['sample_count']}",
        ]
    )
    return "\n".join(lines) + "\n"


def save_markdown(report: dict[str, object], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(report), encoding="utf-8")
