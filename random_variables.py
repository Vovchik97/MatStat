import math
from abc import ABC, abstractmethod

import numpy as np


class RandomVariable(ABC):
    @abstractmethod
    def pdf(self, x):
        """
        Возвращает значение плотности вероятности (Probability Density Function - PDF)
        для заданного значения случайной величины.

        Параметры:
        x: float
            Значение случайной величины, для которого нужно вычислить плотность вероятности.

        Возвращает:
        float
            Значение плотности вероятности для заданного значения x.
        """
        pass

    @abstractmethod
    def cdf(self, x):
        """
        Возвращает значение функции распределения (Cumulative Distribution Function - CDF)
        для заданного значения случайной величины.

        Параметры:
        x: float
            Значение случайной величины, для которого нужно вычислить функцию распределения.

        Возвращает:
        float
            Значение функции распределения для заданного значения x.
        """
        pass

    @abstractmethod
    def quantile(self, alpha):
        """
        Возвращает квантиль уровня alpha для случайной величины.

        Параметры:
        alpha: float
            Уровень, для которого нужно вычислить квантиль. Должен быть в диапазоне [0, 1].

        Возвращает:
        float
            Квантиль уровня alpha для данной случайной величины.
        """
        pass


class LaplaceRandomVariable(RandomVariable):
    def __init__(self, location=0, scale=1) -> None:
        super().__init__()
        self.location = location
        self.scale = scale

    def pdf(self, x):
        return 0.5 * self.scale * math.exp(-self.scale * abs(x - self.location))

    def cdf(self, x):
        if x < self.location:
            return 0.5 * math.exp((x - self.location) / self.scale)
        else:
            return 1 - 0.5 * math.exp(-(x - self.location) / self.scale)

    def quantile(self, alpha):
        if alpha == 0.5:
            return self.location
        elif alpha < 0.5:
            return self.location - self.scale * math.log(1 - 2 * alpha)
        else:
            return self.location + self.scale * math.log(2 * alpha - 1)


class UniformRandomVariable(RandomVariable):
    def __init__(self, left=0, right=1) -> None:
        super().__init__()
        self.left = left
        self.right = right

    def pdf(self, x):
        if x < self.left or x > self.right:
            return 0
        else:
            return 1 / (self.right - self.left)

    def cdf(self, x):
        if x < self.left:
            return 0
        elif x > self.right:
            return 1
        else:
            return (x - self.left) / (self.right - self.left)

    def quantile(self, alpha):
        return self.left + alpha * (self.right - self.left)


class SmoothedRandomVariable(RandomVariable, ABC):

    def __init__(self, sample, h):
        self.sample = sample
        self.h = h

    def _k(x):
        if abs(x) <= 1:
            return 0.75 * (1 - x * x)
        else:
            return 0

    def _K(x):
        if x < -1:
            return 0
        elif -1 <= x < 1:
            return 0.5 + 0.75 * (x - x ** 3 / 3)
        else:
            return 1

    def pdf(self, x):
        return np.mean([SmoothedRandomVariable._k((x - y) / self.h) for y in self.sample]) / self.h

    def cdf(self, x):
        return np.mean([SmoothedRandomVariable._K((x - y) / self.h) for y in self.sample])

    def quantile(self, alpha):
        raise NotImplementedError
