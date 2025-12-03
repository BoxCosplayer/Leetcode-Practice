# O(n**2)
def sol(nums, target):
    for i in range(0, len(nums) - 1):
        x = nums[i]
        possibleY = target - x
        print(possibleY)
        for j in range(i + 1, len(nums)):
            y = nums[j]
            print("Y: " + str(y))
            if y == possibleY:
                return [i, j]

# O(n)

def sol(nums, target):
    map = {}
    for i, num in enumerate(nums):
        compliment = target - nums[i]
        if compliment in map:
            return [map[compliment], i]
        
        map[num] = i