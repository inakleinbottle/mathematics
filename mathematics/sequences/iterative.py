from abc import ABC, abstractmethod
from collections import deque
from sys import float_info

from . import base


MAX_ITER = 2<<19


class IterativeSchemeABC(base.AbstractSequence, ABC):
    """
    Abstract base class for iterative scheme sequences.
    """

    @abstractmethod
    def find_limit(self, *start_value, max_iterations=None, tolerance=None):
        """
        Find the limit of the sequence if it exists.

        :param start_value:
        :param max_iterations:
        :param tolerance:
        :return:
        """
        pass




class ConvergenceError(Exception):
    pass


class BaseIterativeScheme(IterativeSchemeABC):
    """
    Base class for iterative schemes
    """

    def __init__(self, *, error_calc=None, max_stored=None):
        self.previous_terms = deque(maxlen=max_stored)
        self.error_calc = (error_calc if error_calc
                           else lambda prv, cur: abs(cur - prv))

    def __next__(self):
        if not self.previous_terms:
            raise StopIteration('No initial value specified')

        next_val = self.calculate_next_value()
        self.previous_terms.append(next_val)
        return next_val

    def calculate_next_value(self):
        raise NotImplemented

    def find_limit(self, *start_value, max_iterations=None, tolerance=None):

        self.previous_terms.extend(start_value)
        current = start_value[-1]

        error_calc = self.error_calc

        max_iterations = max_iterations if max_iterations else MAX_ITER
        tolerance = tolerance if tolerance else float_info.epsilon

        for _ in range(max_iterations):
            nxt_val = next(self)

            if error_calc(current, nxt_val) < tolerance:
                break

            current = nxt_val
        else:
            # max_iterations reached
            raise ConvergenceError(f'No limit found after {max_iterations} '
                                   'iterations')
        return current


class NewtonScheme(BaseIterativeScheme):

    def __init__(self, function, derivative, *, error_calc=None):
        assert callable(function)
        assert callable(derivative)
        super().__init__(error_calc=error_calc, max_stored=1)
        self.function = function
        self.derivative = derivative

    def calculate_next_value(self):
        """
        Calculate the next term in the Newton iteration scheme.

        :return:
        """
        current = self.previous_terms[-1]

        return current - self.function(current) / self.derivative(current)

