"""CLI entry point for Prompt Engineering for Assessment Question Generation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from generator.question_generator import QuestionGenerator
from reports.comparison_report import build_report, save_markdown, save_report


SAMPLES_PATH = Path("samples/generated_samples.json")
REPORT_JSON_PATH = Path("samples/comparison_report.json")
REPORT_MD_PATH = Path("reports/comparison_report.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate assessment questions using multiple prompt strategies."
    )
    parser.add_argument("--domain", default="Python", help="Example: Python")
    parser.add_argument("--difficulty", default="Easy", help="Example: Easy")
    parser.add_argument(
        "--input-json",
        help='Optional JSON string such as {"domain":"Python","difficulty":"Easy"}',
    )
    parser.add_argument(
        "--reset-history",
        action="store_true",
        help="Clear duplicate-detection history before generating samples.",
    )
    return parser.parse_args()


def resolve_input(args: argparse.Namespace) -> tuple[str, str]:
    if not args.input_json:
        return args.domain, args.difficulty

    payload = parse_input_json(args.input_json)
    return payload["domain"], payload["difficulty"]


def parse_input_json(raw_value: str) -> dict[str, str]:
    """Parse strict JSON, with a fallback for shells that strip inner quotes."""

    try:
        return json.loads(raw_value)
    except json.JSONDecodeError:
        loose_pairs = re.findall(r"([A-Za-z_][\w ]*)\s*:\s*([^,{}]+)", raw_value)
        if not loose_pairs:
            raise
        return {key.strip(): value.strip().strip("\"'") for key, value in loose_pairs}


def main() -> None:
    args = parse_args()
    domain, requested_difficulty = resolve_input(args)

    generator = QuestionGenerator()
    if args.reset_history:
        generator.reset_history()

    samples = generator.generate_all(domain=domain)
    selected = [
        sample for sample in samples if sample["difficulty"] == requested_difficulty
    ]

    SAMPLES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SAMPLES_PATH.open("w", encoding="utf-8") as file:
        json.dump(samples, file, indent=2)

    report = build_report(samples)
    save_report(report, REPORT_JSON_PATH)
    save_markdown(report, REPORT_MD_PATH)

    print(json.dumps({"requested_samples": selected, "all_samples": samples}, indent=2))
    print(f"\nSaved samples to {SAMPLES_PATH}")
    print(f"Saved comparison report to {REPORT_MD_PATH}")


if __name__ == "__main__":
    main()
