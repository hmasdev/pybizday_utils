import argparse
import contextlib
import time
from datetime import date
from typing import Generator

from pybizday_utils import get_n_next_bizday
from pybizday_utils.holiday_utils import is_saturday_or_sunday


@contextlib.contextmanager
def stopwatch(records: list[float]) -> Generator[None, None, None]:
    """
    Context manager to measure the execution time of a block of code.
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        records.append(end_time - start_time)


def calc_statistics(records: list[float]) -> dict[str, float]:
    """
    Calculate statistics from a list of execution times.
    """
    # empty case
    if not records:
        return {}
    # calculate statistics
    ave = sum(records) / len(records)
    squared_mean = sum(x ** 2 for x in records) / len(records)
    return {
        "min": min(records),
        "max": max(records),
        "avg": ave,
        "std": (squared_mean - ave ** 2) ** 0.5,
        "count": len(records),
    }


def main() -> None:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Check performance of get_n_next_bizday")  # noqa: E501
    parser.add_argument(
        "--n",
        type=int,
        default=100000,
        help="Number of business days to calculate",
    )
    parser.add_argument(
        "--n-trials",
        type=int,
        default=100,
        help="Number of trials to run",
    )
    parser.add_argument(
        "--date",
        type=str,
        default="2023-10-01",
        help="Date to start from (YYYY-MM-DD)",
    )
    args = parser.parse_args()

    # preparation
    n = args.n
    d = date.fromisoformat(args.date)
    n_trials = args.n_trials

    # Execute the function and measure performance
    records = []
    for _ in range(n_trials):
        with stopwatch(records):
            get_n_next_bizday(d, n, is_holiday=is_saturday_or_sunday)

    # Print the results
    stats = calc_statistics(records)
    print(f"Statistics of elapsed time for {n_trials} trials of get_n_next_bizday")  # noqa: E501
    for key, value in stats.items():
        print(f"{key}: {value:.6f}")


if __name__ == "__main__":
    main()
