from typing import List
from functools import lru_cache
import bisect


def maxValue(events: List[List[int]], maxAttend: int) -> int:
    """
    Optimal (non-naive) solution using DP + binary search.
    events: [start, end, value], maxAttend: max number of events to attend.
    """
    if not events or maxAttend <= 0:
        return 0

    # Sort by start day to binary-search the next non-overlapping event
    events.sort(key=lambda x: x[0])
    starts = [e[0] for e in events]
    n = len(events)

    @lru_cache(None)
    def dp(i: int, remaining: int) -> int:
        if i == n or remaining == 0:
            return 0

        # Option 1: skip current event
        best = dp(i + 1, remaining)

        # Option 2: take current event and jump to next non-overlapping
        next_i = bisect.bisect_left(starts, events[i][1] + 1)
        best = max(best, events[i][2] + dp(next_i, remaining - 1))
        return best

    return dp(0, maxAttend)


if __name__ == "__main__":
    events = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
    k = 3
    # events = [startDay, endDay, value], k = MaxNumberofEvents
    # Must attend whole event, endDay is inclusive
    print(maxEvents(events, k))  # expected 9 for this sample
