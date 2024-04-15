import sys

import numpy as np
from matplotlib import pyplot as plt

from modelling import Modelling
from random_number_generator import TukeyNumberGenerator, SimpleRandomNumberGenerator
from random_variables import LaplaceRandomVariable, UniformRandomVariable, SmoothedRandomVariable, \
    NonParametricRandomVariable
from estimations import TruncatedMean

location = float(sys.argv[1])
scale = float(sys.argv[2])
length = int(round(float(sys.argv[3])))
number_resample = int(sys.argv[4])

rv = LaplaceRandomVariable(location, scale)  # Создание экземпляра класса CauchyRandomVariable с заданными параметрами

tukey_rv = UniformRandomVariable(-5, 5)

generator = TukeyNumberGenerator(rv, tukey_rv)

sample = generator.get(length, 0.1)

rv1 = NonParametricRandomVariable(sample)  # Создание экземпляра класса NonParametricRandomVariable на основе исходной выборки
generator1 = SimpleRandomNumberGenerator(rv1)  # Создание генератора случайных чисел на основе непараметрической случайной величины

modelling = Modelling(generator1, [TruncatedMean(0.01)], 2 * length, location, length)
modelling.run()
"""modelling = Modelling(sample, location, number_resample)

result = modelling.run()

print('Результат', ["Оценка среднего", "Оценка медианы"])
print('Значения MSE', [result[0], result[1]])
print('Отношения', [result[0] / result[1], result[1] / result[0]])
"""

mses = modelling.estimate_mse()  # СКО оценок
print(mses)
#print(mses[1] / mses[0])
variances = modelling.estimate_var()
print("Дисперсия: ", variances)
variances = modelling.estimate_bias_sqr()
print("Квадрат смещения: ", variances)

samples = modelling.get_samples()

if __name__ == '__main__':
    POINTS = 100
    bandwidth = 0.1

    for i in range(samples.shape[1]):
        sample = samples[:, i]
        X_min = min(sample)
        X_max = max(sample)
        x = np.linspace(X_min, X_max, POINTS)
        srv = SmoothedRandomVariable(sample, bandwidth)
        y = np.vectorize(srv.pdf)(x)
        plt.plot(x, y)
    plt.show()
"""
POINTS = 100
bandwidth = 0.1

for i in samples:
    X_min = min(i)
    X_max = max(i)
    x = np.linspace(X_min, X_max, POINTS)
    srv = SmoothedRandomVariable(i, bandwidth)
    y = np.vectorize(srv.pdf)(x)
    plt.plot(x, y)
plt.show()"""
