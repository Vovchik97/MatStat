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


class NonParametricRandomVariable(RandomVariable):
    def __init__(self, source_sample) -> None:
        super().__init__()
        self.source_sample = sorted(source_sample)

    def pdf(self, x):
        if x in self.source_sample:
            return float('inf')
        return 0

    @staticmethod
    def heaviside_function(x):
        if x > 0:
            return 1
        else:
            return 0

    def cdf(self, x):
        return np.mean(np.vectorize(self.heaviside_function)(x - self.source_sample))

    def quantile(self, alpha):
        index = int(alpha * len(self.source_sample))
        return self.source_sample[index]


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
    """
    def _k(self, x):
        return math.exp(-0.5 * x ** 2) / (math.sqrt(2 * math.pi))

    def _K(self, x):
        if x <= 0:
            return 0.852 * math.exp(-math.pow((-x + 1.5774) / 2.0637, 2.34))
        return 1 - 0.852 * math.exp(-math.pow((x + 1.5774) / 2.0637, 2.34))

    def h(self, x):
        return -x * self._k(x)

    def __init__(self, sample):
        self.sample = sample
        self.length = len(sample)
        self.h = self.get_h()

    def get_hn(self):
        temp = 0.0
        for i in range(self.length):
            temp += self.sample[i]
        mean = temp / self.length
        temp2 = 0.0
        for i in range(self.length):
            temp2 += np.power(self.sample[i] - mean, 2)
        return np.sqrt(temp2) / (self.length - 1)

    def get_h(self):
        hn = self.get_hn()
        delta = 1.0
        while delta >= 0.001:
            s = 0.0
            for i in range(self.length):
                num = 0.0
                div = 0.0
                for j in range(self.length):
                    if i != j:
                        diff = (self.sample[j] - self.sample[i]) / hn
                        num += self.h(diff) * (self.sample[j] - self.sample[i])
                        div += self._k(diff)
                if div == 0.0:
                    continue
                s += num / div
            new_hn = - (1 / self.length) * s
            delta = abs(new_hn - hn)
            hn = new_hn
        return hn

    def pdf(self, x):
        return np.mean([self._k((x - y) / self.h) for y in self.sample]) / self.h

    def cdf(self, x):
        return np.mean([self._K((x - y) / self.h) for y in self.sample])

    def quantile(self, alpha):
        raise NotImplementedError"""


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