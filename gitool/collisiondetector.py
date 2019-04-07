import logging

from collections import defaultdict

from .util import dict_iter

logger = logging.getLogger("gitool")


class CollisionDetector():
    def __init__(self, items, functions):
        self.bucket = dict()

        for function in functions:
            self._init_dict(items, function)

    def _init_dict(self, items, function):
        dictionary = defaultdict(set)

        for topic, item in dict_iter(items):
            msg = "Inserting '{}' into table '{}'."
            logger.debug(msg.format(item, function))
            method = getattr(item, function)
            value = method()
            dictionary[value].add(item)

        self.bucket[function] = dictionary

    def get_collisions(self, item):
        items = set()

        for function, dictionary in self.bucket.items():
            method = getattr(item, function)
            value = method()
            lookup = dictionary[value]
            items.update(lookup)

        return items
