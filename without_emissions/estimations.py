import statistics
from abc import ABC, abstractmethod

import numpy as np


class Estimation(ABC):
    @abstractmethod
    def estimate(self, sample):
        pass


class SampleMean(Estimation):

    # SampleMean (Выборочное среднее)

    def estimate(self, sample):
        # Estimate вычисляет выборочное среднее значение для переданной выборки.

        return sum(sample) / len(sample)


class HodgesLehmannEstimator(Estimation):
    def median(self, arr):
        # Медиана списка arr.

        return (arr[(len(arr) - 1) // 2] + arr[len(arr) // 2]) / 2

    def estimate(self, sample):

        # Estimate вычисляет оценку Ходжеса-Лемана на основе переданной выборки.
        # Создаем список для хранения средних значений Уолша
        walsh_average = []

        # Вычисляем средние значения Уолша для всех пар элементов выборки
        for i in range(len(sample)):
            for j in range(i + 1, len(sample)):
                walsh_average.append((sample[i] + sample[j]) / 2)

        # Сортируем средние значения Уолша
        walsh_average.sort()

        # Возвращаем медиану средних значений Уолша
        return self.median(walsh_average)


class Mean(Estimation):
    def estimate(self, sample):
        return statistics.mean(sample)


class Var(Estimation):
    def estimate(self, sample):
        return statistics.variance(sample)


class Median(Estimation):
    def estimate(self, sample: list):
        return np.median(sample)

"""class TrimmedMean(Estimation):
    def __init__(self, trim_percent):
        self.trim_percent = trim_percent

    def estimate(self, sample):
        if self.trim_percent <= 0 or self.trim_percent >= 50:
            raise ValueError("Неверное значение процента усечения.")

        trim_count = int(len(sample) * self.trim_percent / 100)
        trimmed_sample = sorted(sample)[trim_count : len(sample) - trim_count]
        return sum(trimmed_sample) / len(trimmed_sample)"""

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