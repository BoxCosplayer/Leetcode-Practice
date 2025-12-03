from typing import List
from collections import defaultdict

def countTrapezoids(points: List[List[int]]) -> int:
    ans = 0

    # find number of rows (y values) where there are at least 2 points on that row
    # Count number of cominbations of valid x pairs on each line (n! / (n-x)!)
    # return sum of pairs mod const

    rows = defaultdict(set)
    for x, y in points:
        rows[y].add(x)
    
    # keep only y’s with >1 distinct x
    rows = {y: xs for y, xs in rows.items() if len(xs) > 1}

    pair_count = []
    for xs in rows.values():
        n = len(xs)
        if n >= 2:
            pair_count.append(len(xs) * (len(xs) - 1) // 2)
    
    if len(pair_count) < 2:
        return 0

    # for i in range(len(pair_count)):
    #     for j in range(i + 1, len(pair_count)):
    #         ans += pair_count[i] * pair_count[j]

    # Σᵢ<ⱼ aᵢaⱼ = ( (Σaᵢ)² − Σ(aᵢ²) ) / 2.

    s = sum(pair_count)
    s_squared = sum(count * count for count in pair_count)

    ans = ((s ** 2 - s_squared) // 2)

    modulo = (10 ** 9) + 7
    return ans % modulo