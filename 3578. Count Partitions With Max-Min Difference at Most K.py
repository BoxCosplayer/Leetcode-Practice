from typing import List

MOD = 10 ** 9 + 7

def countPartitions(nums: List[int], k: int) -> int:
    n = len(nums)
    dp = [1] + [0] * n  # dp[i] = ways for prefix of length i
    acc = 1            # running sum of dp[l] for current window
    sl = SortedList()

    l = 0
    for r in range(n):
        sl.add(nums[r])
        # shrink window until max - min <= k
        while sl[-1] - sl[0] > k:
            sl.remove(nums[l])
            acc = (acc - dp[l]) % MOD
            l += 1

        dp[r + 1] = acc
        acc = (acc + dp[r + 1]) % MOD

    return dp[n]


# quick self-check
if __name__ == "__main__":
    nums = [9, 4, 1, 3, 7]
    k = 4
    print(countPartitions(nums, k))  # expected 6
