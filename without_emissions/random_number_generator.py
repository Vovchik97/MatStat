from abc import abstractmethod, ABC

import numpy as np

from random_variables import RandomVariable


# Напишем интерфейс для генераторов случайных величин.
class RandomNumberGenerator(ABC):
    def __init__(self, random_variable: RandomVariable):
        self.random_variable = random_variable

    @abstractmethod
    def get(self, N):
        pass


# Реализуем конкретный класс генератора случайных величин на базе квантилей.
class SimpleRandomNumberGenerator(RandomNumberGenerator):
    def __init__(self, random_variable: RandomVariable):
        super().__init__(random_variable)

    def get(self, N):
        us = np.random.uniform(0, 1, N)
        return np.vectorize(self.random_variable.quantile)(us)