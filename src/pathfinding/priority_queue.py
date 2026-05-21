import heapq
from itertools import count
from typing import Generic, TypeVar

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    """
    A min-heap priority queue with stable ordering.

    Items with lower priority values are returned first. When two items
    share the same priority, insertion order is preserved using an
    internal counter, avoiding comparison errors on items that do not
    support ordering.
    """

    def __init__(self) -> None:
        """Initializes an empty priority queue."""

        self.elements: list[tuple[float, float, T]] = []
        self._counter = count()

    def empty(self) -> bool:
        """Returns True if the queue contains no items."""

        return not self.elements

    def put(self, item: T, priority: float) -> None:
        """
        Inserts an item into the queue.

        Args:
            item: The item to insert.
            priority: The priority value. Lower values are dequeued first.
        """

        heapq.heappush(self.elements, (priority, next(self._counter),  item))

    def get(self) -> T:
        """
        Removes and returns the item with the lowest priority.

        Returns:
            The highest-priority item in the queue.
        """

        return heapq.heappop(self.elements)[2]
