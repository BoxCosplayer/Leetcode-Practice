from typing import List
import heapq

def maxEvents(events: List[List[int]]) -> int:

    # Attend event that ends first
    events.sort(key=lambda x:x[0])
    n = len(events)
    
    # Setup pointer, minHeap and trackers
    i = 0
    minHeap: List[int] = []
    day = 0
    attended = 0

    while i < n or minHeap:
        
        # Add all events that have started on or before day i
        while i < n and events[i][0] <= day:
            heapq.heappush(minHeap, events[i][1])
            i += 1

        # Drop events that have ended
        while minHeap and minHeap[0] < day:
            heapq.heappop(minHeap)

        # If there is an event in the minheap, pop it (attend the event)
        if minHeap:
            heapq.heappop(minHeap)
            attended += 1

        day += 1

    return attended


events = [[1,4],[4,4],[2,2],[3,4],[1,1]]
print(maxEvents(events))
# ans should be 4
