import argparse
import json
import sys
from typing import Optional

from .core import generate_mcqs


def _read_input(text: Optional[str], input_file: Optional[str]) -> str:
    if text:
        return text
    if input_file:
        with open(input_file, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate MCQs from input text using simple keyword cloze.")
    parser.add_argument("--text", type=str, help="Inline text to generate questions from", default=None)
    parser.add_argument("--input-file", type=str, help="Path to a text file", default=None)
    parser.add_argument("--num", type=int, help="Number of questions", default=5)
    parser.add_argument("--choices", type=int, help="Number of choices per question", default=4)
    parser.add_argument("--seed", type=int, help="Random seed", default=42)
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    text = _read_input(args.text, args.input_file)
    mcqs = generate_mcqs(text, num_questions=args.num, num_choices=args.choices, seed=args.seed)

    if args.json:
        print(json.dumps(mcqs, ensure_ascii=False, indent=2))
        return

    # Human-readable output
    for i, q in enumerate(mcqs, start=1):
        print(f"Q{i}. {q['question']}")
        for j, opt in enumerate(q["options"]):
            label = chr(ord('A') + j)
            print(f"  {label}) {opt}")
        correct_label = chr(ord('A') + int(q["answer_index"]))
        print(f"  Answer: {correct_label}")
        print()


if __name__ == "__main__":
    main()


