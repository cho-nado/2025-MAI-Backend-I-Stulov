from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> str:
        if key not in self.cache:
            return ""
        # Move to the end as the most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: str) -> None:
        if key in self.cache:
            # Remove and re-add to refresh the order
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove the oldest (the first in OrderedDict)
            self.cache.popitem(last=False)
        self.cache[key] = value

    def rem(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]
