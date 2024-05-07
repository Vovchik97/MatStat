import statistics
from abc import ABC, abstractmethod


class Estimation(ABC):
    @abstractmethod
    def estimate(self, sample):
        pass


class TruncatedMean(Estimation):
    def __init__(self, alpha):
        self.alpha = alpha

    def estimate(self, sample):
        sorted_sample = sorted(sample)
        n = len(sample)
        lower_bound = int(n * (self.alpha / 2))
        upper_bound = n - lower_bound
        truncated_sample = sorted_sample[lower_bound:upper_bound]
        return sum(truncated_sample) / len(truncated_sample)


class Mean(Estimation):
    def estimate(self, sample):
        return statistics.mean(sample)


class Var(Estimation):
    def estimate(self, sample):
        return statistics.variance(sample)

