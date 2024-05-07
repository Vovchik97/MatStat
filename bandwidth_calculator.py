import math
from abc import ABC, abstractmethod


class Function(ABC):
    @abstractmethod
    def _k(self, x):
        pass

    @abstractmethod
    def _K(self, x):
        pass

    @abstractmethod
    def h(self, x):
        pass


class CauchyCore(Function):
    def _k(self, x):
        return 1 / (math.pi * (1 + x ** 2))

    def _K(self, x):
        return math.atan(x) / math.pi + 0.5

    def h(self, x):
        return -2 * x / (math.pi * (1 + x ** 2))


class BandwidthCalculator:
    def __init__(self, sample, core):
        self.sample = sample
        self.core = core

    def calculate_bandwidth(self):
        n = len(self.sample)
        sum_sample = sum(self.sample)
        mean = sum_sample / n
        sum_squares = sum((x - mean) ** 2 for x in self.sample)
        hn = math.sqrt(sum_squares) / (n - 1)
        delta = 1.0
        while delta >= 0.001:
            s = 0.0
            for i in range(n):
                num = 0.0
                div = 0.0
                for j in range(n):
                    if i != j:
                        diff = (self.sample[j] - self.sample[i]) / hn
                        num += self.core.h(diff) * (self.sample[j] - self.sample[i])
                        div += self.core._k(diff)
                if div == 0.0:
                    continue
                s += num / div
            new_hn = - (1 / n) * s
            delta = abs(new_hn - hn)
            hn = new_hn
        return hn
