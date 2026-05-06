import heapq
from itertools import count
from typing import TypeVar, Generic
T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self.elements: list[tuple[int, int, T]] = []
        self._counter = count()

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: int) -> None:
        heapq.heappush(self.elements, (priority, next(self._counter),  item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[2]
