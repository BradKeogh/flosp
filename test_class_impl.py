import random

class BingoCage:
    """
    This is my documentation.
    """
    def __init__(self,items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        """
        Wrigint about pick method here here. here.!
        """
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingCage')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))

bingo

bingo._items

bingo.pick()

bingo()
