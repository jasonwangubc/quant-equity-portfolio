"""Run end-to-end factor research demo."""

from __future__ import annotations

from pathlib import Path

from factor_research.pipeline import run_research_pipeline


def main() -> None:
    output = run_research_pipeline(db_path=Path("data/factor_research.duckdb"))
    print("Factor Research Summary")
    print("-" * 40)
    for key, value in output.summary.items():
        print(f"{key:>24}: {value: .4f}")
    print("-" * 40)
    print(f"Backtest months: {len(output.backtest.history)}")
    print(f"IC observations: {len(output.information_coefficient)}")


if __name__ == "__main__":
    main()
