# Better solution

def lengthOfLongestSubstring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best

# First, naive solution

def lengthOfLongestSubstring_naive(s: str) -> int:

    def myFunction(seen_letters = [], length = 0, max_length = 0, s=s):

        for letterIndex in range(len(s)):
            if s[letterIndex]:
                if s[letterIndex] not in seen_letters: 
                    seen_letters.append(s[letterIndex])
                    if len(seen_letters) > max_length:
                        max_length = len(seen_letters)
                elif len(s) > 1:
                    seen_letters = []
                    s = s[1:]
                    return myFunction(seen_letters, length, max_length, s)

        
        return max_length
    
    return myFunction()

s = "pwwkew"
print("ans: " + str(lengthOfLongestSubstring(s)))
# ans should be 3
