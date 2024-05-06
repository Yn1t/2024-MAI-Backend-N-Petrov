from collections import OrderedDict


class LRUCache:

    def __init__(self, capacity: int = 10) -> None:
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> str:
        res = self.cache.get(key)
        if res:
            self.cache.move_to_end(key)
            return res
        return ''

    def set(self, key: str, value: str) -> None:
        res = self.cache.get(key, None)
        self.cache.move_to_end(key) if res else None
        self.cache[key] = value
        self.cache.popitem(False) if len(self.cache) > self.capacity else None

    def rem(self, key: str) -> None:
        self.set(key, None)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cache = LRUCache(100)
    cache.set('Jesse', 'Pinkman')
    cache.set('Walter', 'White')
    cache.set('Jesse', 'James')
    print(cache.get('Jesse'))  # вернёт 'James'
    cache.rem('Walter')
    print(cache.get('Walter'))  # вернёт ''
