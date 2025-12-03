import math
from typing import List
from collections import defaultdict

def _normalize(dy: int, dx: int) -> tuple[int, int]:
    """Return a canonical direction vector for the given slope."""
    if dx == 0:
        return (1, 0)  # vertical line
    if dy == 0:
        return (0, 1)  # horizontal line

    g = math.gcd(abs(dy), abs(dx))
    dy //= g
    dx //= g

    if dx < 0:  # keep dx positive for uniqueness
        dy, dx = -dy, -dx
    return dy, dx


def countTrapezoids(points: List[List[int]]) -> int:
    n = len(points)

    # Count segments on each distinct line grouped by slope.
    slope_to_segments = defaultdict(list)  # slope -> [number of segments on each line]
    seen_lines = set()  # (dy, dx, intercept) to avoid re-processing the same line

    # Do a double pass to find store, and all pairs of values
    for i in range(n):
        x1, y1 = points[i]
        slope_count = defaultdict(int)
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dy, dx = y2 - y1, x2 - x1
            slope = _normalize(dy, dx)
            slope_count[slope] += 1

        # For every slope have we seen it before?
        for slope, cnt in slope_count.items():
            if cnt == 0:
                continue
            dy, dx = slope
            intercept = dy * x1 - dx * y1  # constant term for line in form dy*x - dx*y = c
            line_key = (dy, dx, intercept)
            if line_key in seen_lines:
                continue
            seen_lines.add(line_key)

            # How many paris of points lie on this slope?
            points_on_line = 1 + cnt  # anchor point i plus all with same slope relative to it
            if points_on_line >= 2:
                segments = points_on_line * (points_on_line - 1) // 2
                slope_to_segments[slope].append(segments)

    # Parrellograms have similar properties to trapezoids, so our traditional 
    # definition catches both, we need to care for duplicates

    # Totals all pairs of segments with same slope, regardless of diagonal
    trapezoids_with_duplicates = 0
    for segs in slope_to_segments.values():
        if len(segs) < 2:
            continue  # need two distinct parallel lines
        total = sum(segs)
        total_sq = sum(v * v for v in segs)
        trapezoids_with_duplicates += (total * total - total_sq) // 2


    # Another pass through to store midpoints and (midpoints, direction_vector)
    midpoint_counts = defaultdict(int)  # midpoint -> number of diagonals through it
    midpoint_dir_counts = defaultdict(int)  # (midpoint, direction) -> count of diagonals along that line

    # This passthrough treats every possible line as a diagonal
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            mid = (x1 + x2, y1 + y2)  # store doubled midpoint to keep integers
            dir_vec = _normalize(y1 - y2, x1 - x2)  # direction of the diagonal
            midpoint_counts[mid] += 1
            midpoint_dir_counts[(mid, dir_vec)] += 1

    # sum all pairs of diagonals with the same midpoint
    # This dictates the numbber of 4 points which are on the same line, not
    # Parallelograms
    collinear_pairs_by_mid = defaultdict(int)
    for (mid, _dir), cnt in midpoint_dir_counts.items():
        collinear_pairs_by_mid[mid] += cnt * (cnt - 1) // 2

    # Calculate all parallelograms found using midpoint intersection
    parallelograms = 0
    for mid, total in midpoint_counts.items():
        if total < 2:
            continue
        all_pairs = total * (total - 1) // 2
        parallelograms += all_pairs - collinear_pairs_by_mid[mid]

    ans = (trapezoids_with_duplicates - parallelograms)
    return ans


points = [[-3, 2], [3, 0], [2, 3], [3, 2], [2, -3]]
print(countTrapezoids(points))
# ans should be: 2


# slightly better theoretical runtime, but harder to read (only 1 double pass through instead of 2)


def countTrapezoids(points: List[List[int]]) -> int:
    n = len(points)

    # Count segments on each distinct line grouped by slope.
    slope_to_segments = defaultdict(list)  # slope -> [number of segments on each line]
    seen_lines = set()  # (dy, dx, intercept) to avoid re-processing the same line

    # Count midpoints of diagonals
    midpoint_counts = defaultdict(int)  # midpoint -> number of diagonals through it
    midpoint_dir_counts = defaultdict(int)  # (midpoint, direction) -> count of diagonals along that line

    # Do a double pass to find store, and all pairs of values
    for i in range(n):
        x1, y1 = points[i]
        slope_count = defaultdict(int)
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dy, dx = y2 - y1, x2 - x1
            slope = _normalize(dy, dx)
            slope_count[slope] += 1

            # Diagonal calulcations for parallelograms
            mid = (x1 + x2, y1 + y2)  # store doubled midpoint to keep integers
            dir_vec = _normalize(y1 - y2, x1 - x2)  # direction of the diagonal
            midpoint_counts[mid] += 1
            midpoint_dir_counts[(mid, dir_vec)] += 1

        # For every slope have we seen it before?
        for slope, cnt in slope_count.items():
            if cnt == 0:
                continue
            dy, dx = slope
            intercept = dy * x1 - dx * y1  # constant term for line in form dy*x - dx*y = c
            line_key = (dy, dx, intercept)
            if line_key in seen_lines:
                continue
            seen_lines.add(line_key)

            # How many paris of points lie on this slope?
            points_on_line = 1 + cnt  # anchor point i plus all with same slope relative to it
            if points_on_line >= 2:
                segments = points_on_line * (points_on_line - 1) // 2
                slope_to_segments[slope].append(segments)

    # Parrellograms have similar properties to trapezoids, so our traditional 
    # definition catches both, we need to care for duplicates

    # Totals all pairs of segments with same slope, regardless of diagonal
    trapezoids_with_duplicates = 0
    for segs in slope_to_segments.values():
        if len(segs) < 2:
            continue  # need two distinct parallel lines
        total = sum(segs)
        total_sq = sum(v * v for v in segs)
        trapezoids_with_duplicates += (total * total - total_sq) // 2

    # sum all pairs of diagonals with the same midpoint
    # This dictates the numbber of 4 points which are on the same line, not
    # Parallelograms
    collinear_pairs_by_mid = defaultdict(int)
    for (mid, _dir), cnt in midpoint_dir_counts.items():
        collinear_pairs_by_mid[mid] += cnt * (cnt - 1) // 2

    # Calculate all parallelograms found using midpoint intersection
    parallelograms = 0
    for mid, total in midpoint_counts.items():
        if total < 2:
            continue
        all_pairs = total * (total - 1) // 2
        parallelograms += all_pairs - collinear_pairs_by_mid[mid]

    ans = (trapezoids_with_duplicates - parallelograms)
    return ans


points = [[-3, 2], [3, 0], [2, 3], [3, 2], [2, -3]]
print(countTrapezoids(points))
# ans should be: 2