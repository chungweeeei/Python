import time
from itertools import cycle

if __name__ == "__main__":
    
    nums = ["A", "B"]
    
    count = 0
    for x in cycle(nums):
        print(count, x)
        count += 1
        
        time.sleep(1.0)