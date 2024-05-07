import matplotlib.pyplot as plt
import numpy as np

from estimations import TruncatedMean
from modelling import bootstrap_resample, Modelling
from random_number_generator import SimpleRandomNumberGenerator, TukeyNumberGenerator, AsymmetricTukeyNumberGenerator
from random_variables import LaplaceRandomVariable, SmoothedRandomVariable, UniformRandomVariable

POINTS = 100


def print_statistics(modelling: Modelling):
    mses = modelling.estimate_mse()
    print("СКО:", mses)
    variances = modelling.estimate_var()
    print("Дисперсия: ", variances)
    variances = modelling.estimate_bias_sqr()
    print("Квадрат смещения: ", variances)


def plot_samples(sample, bandwidth):
    x_min = min(sample)
    x_max = max(sample)
    x = np.linspace(x_min, x_max, POINTS)
    srv = SmoothedRandomVariable(sample, bandwidth)
    y = np.vectorize(srv.pdf)(x)
    plt.plot(x, y)
    plt.show()


def run_modelling(number_resample: int, location: float, resamples: list, N):
    # Поиск наилучшего alpha
    alpha_values = [i for i in np.arange(0.01, 0.5, 0.01)]
    mse_values = []  # СКО

    for alpha in alpha_values:
        tm_estimator = TruncatedMean(alpha)
        mses = []
        for i in range(N):
            sample = resamples[i]
            tm = tm_estimator.estimate(sample)
            mse = (tm - 0.5) ** 2
            mses.append(mse)
        mse_values.append(np.mean(mses))

    # Определение наилучшего значения alpha
    best_alpha = alpha_values[np.argmin(mse_values)]
    print(f'Наилучшее значение alpha: {best_alpha}')

    truncated_sample = [TruncatedMean(best_alpha).estimate(sample) for sample in resamples]

    modelling = Modelling(truncated_sample, location, number_resample)
    modelling.run()

    return modelling


def without_emissions(location: float, scale: float, N: int, number_resample: int):
    rv = LaplaceRandomVariable(location, scale)
    generator = SimpleRandomNumberGenerator(rv)

    sample = generator.get(N)

    resamples = bootstrap_resample(sample, number_resample)

    modelling = run_modelling(number_resample, location, resamples, N)

    print_statistics(modelling)

    sample = modelling.get_sample()

    bandwidth = 0.1

    plot_samples(sample, bandwidth)


def with_symmetrical_emissions(location: float, scale: float, N: int, number_resample: int):
    rv = LaplaceRandomVariable(location, scale)
    tukey_rv = UniformRandomVariable(-5, 5)

    generator = TukeyNumberGenerator(rv, tukey_rv)

    sample = generator.get(N)

    resamples = bootstrap_resample(sample, number_resample)

    modelling = run_modelling(number_resample, location, resamples, N)

    print_statistics(modelling)

    sample = modelling.get_sample()

    bandwidth = 0.1

    plot_samples(sample, bandwidth)


def with_asymmetrical_emissions(location: float, scale: float, N: int, number_resample: int):
    rv = LaplaceRandomVariable(location, scale)

    tukey_rv = UniformRandomVariable(-5, 5)

    generator = AsymmetricTukeyNumberGenerator(rv, tukey_rv)

    sample = generator.get(N, 0.1)

    resamples = bootstrap_resample(sample, number_resample)

    modelling = run_modelling(number_resample, location, resamples, N)

    print_statistics(modelling)

    sample = modelling.get_sample()

    bandwidth = 0.1
    plot_samples(sample, bandwidth)
