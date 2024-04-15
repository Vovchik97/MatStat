import sys

import numpy as np
from matplotlib import pyplot as plt

from estimations import TruncatedMean
from modelling import Modelling
from random_number_generator import SimpleRandomNumberGenerator
from random_variables import LaplaceRandomVariable, NonParametricRandomVariable, SmoothedRandomVariable

location = float(sys.argv[1])  # Параметр местоположения (центра) распределения Коши
scale = float(sys.argv[2])  # Параметр масштаба (разброса) распределения Коши
N = int(sys.argv[3])  # Объем выборки

rv = LaplaceRandomVariable(location, scale)
generator = SimpleRandomNumberGenerator(rv)  # Создание экземпляра генератора случайных чисел на основе заданной случайной величины

sample = generator.get(N)  # Генерация исходной выборки с помощью генератора случайных чисел

rv1 = NonParametricRandomVariable(sample)  # Создание экземпляра класса NonParametricRandomVariable на основе исходной выборки
generator1 = SimpleRandomNumberGenerator(rv1)  # Создание генератора случайных чисел на основе непараметрической случайной величины

modelling = Modelling(generator1, [TruncatedMean(0.01)], 2 * N, location, N)
modelling.run()


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