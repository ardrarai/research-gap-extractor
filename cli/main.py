"""
Purpose:
- Serve as the command-line entry point for the tool.
- Parse CLI arguments and flags.
- Invoke the pipeline orchestrator with validated inputs.

Responsibilities:
- Define supported CLI commands and arguments.
- Display final structured output or refusal messages.

Forbidden:
- Do NOT contain pipeline logic.
- Do NOT parse PDFs or process text.
- Do NOT communicate directly with the LLM.
"""


# cli/main.py

import argparse
import sys

from contracts.input_contract import validate_inputs, InputValidationError
from contracts.refusal import get_refusal_message
from pipeline.orchestrator import run


def main():
    parser = argparse.ArgumentParser(
        prog="extract-gaps",
        description="Extract unanswered research questions from multiple papers."
    )

    parser.add_argument(
        "--papers",
        nargs="+",
        required=True,
        help="Paths to research papers (PDF or text). Minimum 3."
    )

    parser.add_argument(
        "--max-questions",
        type=int,
        default=3,
        help="Maximum number of unanswered questions to extract (default: 3)."
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Optional output file path. If not provided, prints to stdout."
    )

    args = parser.parse_args()

    try:
        validated_input = validate_inputs(
            papers=args.papers,
            max_questions=args.max_questions
        )
    except InputValidationError as e:
        print(get_refusal_message(e.code))
        sys.exit(1)

    output = run(validated_input)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
