import heapq
from itertools import count
from ..core.zone import Zone


class PriorityQueue:
    def __init__(self) -> None:
        self.elements: list[tuple[int, int,  Zone]] = []
        self._counter = count()

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: Zone, priority: int) -> None:
        heapq.heappush(self.elements, (priority, next(self._counter),  item))

    def get(self) -> Zone:
        return heapq.heappop(self.elements)[2]
