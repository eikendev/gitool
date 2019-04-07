import functools


@functools.total_ordering
class Configuration:
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def __str__(self):
        return str(self.path)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        same_path = self.path == other.path

        return same_path

    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        gte_path = self.path >= other.path

        return gte_path

    def __hash__(self):
        return hash(self.path)
