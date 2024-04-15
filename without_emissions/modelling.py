from abc import ABC

import numpy as np

from estimations import Var, Mean, Median, Estimation
from random_number_generator import RandomNumberGenerator


class Bootstrap:
    def __init__(self, sample, number_resample=1000):
        self.sample = sample
        self.number_resample = number_resample
        self.length = len(sample)

    def bootstrap_run(self):
        resamples_mean = []
        resamples_median = []
        for _ in range(self.number_resample):
            re_sample = np.random.choice(self.sample, size=self.length, replace=True)
            resamples_mean.append(Mean().estimate(re_sample))
            resamples_median.append(Median().estimate(re_sample))
        return [resamples_mean, resamples_median]


class Modelling(ABC):

    def __init__(self, gen: RandomNumberGenerator, estimations: list[Estimation], M: int, truth_value: float, N: int):
        self.N = N  # Выборка
        self.gen = gen
        self.estimations = estimations
        self.M = M
        self.truth_value = truth_value

        # Здесь будут храниться выборки оценок
        self.estimations_sample = np.zeros((self.M, len(self.estimations)), dtype=np.float64)

    # Метод, оценивающий квадрат смещения оценок
    def estimate_bias_sqr(self):
        return np.array([(Mean().estimate(self.estimations_sample[:, i]) - self.truth_value) ** 2 for i in
                         range(len(self.estimations))])

    # Метод, оценивающий дисперсию оценок
    def estimate_var(self):
        return np.array([Var().estimate(self.estimations_sample[:, i]) for i in range(len(self.estimations))])

    # Метод, оценивающий СКО оценок
    def estimate_mse(self):
        return self.estimate_bias_sqr() + self.estimate_var()

    def get_samples(self):
        return self.estimations_sample

    def get_sample(self):
        return self.gen.get(self.N)

    def run(self):
        for i in range(self.M):
            sample = self.get_sample()
            self.estimations_sample[i, :] = [e.estimate(sample) for e in self.estimations]

