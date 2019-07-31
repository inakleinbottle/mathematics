from abc import ABC, abstractmethod

class AbstractSequence(ABC):
    """
    Abstract base class for mathematical sequence objects.
    """

    @abstractmethod
    def __next__(self):
        pass

class SimpleSequence(AbstractSequence):
    """
    Simple wrapper around a Python iterable.
    """

    def __init__(self, iterable):
        self.iterable = iter(iterable)

    def __next__(self):
        return next(self.iterable)