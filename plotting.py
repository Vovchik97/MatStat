import matplotlib.pyplot as plt
import numpy as np

from estimations import TruncatedMean
from modelling import bootstrap_resample, Modelling
from random_number_generator import SimpleRandomNumberGenerator, TukeyNumberGenerator, AsymmetricTukeyNumberGenerator
from random_variables import LaplaceRandomVariable, SmoothedRandomVariable, UniformRandomVariable

# from bandwidth_calculator import LaplaceCore, BandwidthCalculator
from bandwidth_calculator import calculate_optimal_h

POINTS = 100


def print_statistics(alpha_values, bias_sqr_values, var_values, mse_values):
    best_alpha_sqr = alpha_values[np.argmin(bias_sqr_values)]
    best_alpha_var = alpha_values[np.argmin(var_values)]
    best_alpha_mse = alpha_values[np.argmin(mse_values)]

    print(f'Наилучшее значение alpha при квадратах смещения: {best_alpha_sqr}')
    print(f'Наилучшее значение alpha при дисперсии: {best_alpha_var}')
    print(f'Наилучшее значение alpha при СКО: {best_alpha_mse}')
#     mses = modelling.estimate_mse()
#     print("СКО:", mses)
#     variances = modelling.estimate_var()
#     print("Дисперсия: ", variances)
#     bias_sqr = modelling.estimate_bias_sqr()
#     print("Квадрат смещения: ", bias_sqr)


# def plot_samples(sample, bandwidth):
#     x_min = min(sample)
#     x_max = max(sample)
#     x = np.linspace(x_min, x_max, POINTS)
#     srv = SmoothedRandomVariable(sample, bandwidth)
#     y = np.vectorize(srv.pdf)(x)
#     plt.plot(x, y)
#     plt.show()


def plot_samples(alpha_values, bias_sqr_values, var_values, mse_values):
    plt.figure(figsize=(10, 6))

    # x = np.linspace(np.min(alpha_values), np.max(alpha_values), POINTS)

    # bandwidth_sqr = calculate_optimal_h(bias_sqr_values)
    # print(bandwidth_sqr)
    # bandwidth_var = calculate_optimal_h(var_values)
    # print(bandwidth_var)
    # bandwidth_mse = calculate_optimal_h(mse_values)
    # print(bandwidth_mse)

    # Plot for bias squared values
    plt.subplot(3, 1, 1)
    # srv = SmoothedRandomVariable(bias_sqr_values, bandwidth_sqr)
    # y = np.vectorize(srv.cdf)(x)
    plt.plot(alpha_values, bias_sqr_values, label='Bias Squared')
    # plt.plot(x, y, label='Bias Squared')
    plt.xlabel('Alpha')
    plt.ylabel('Bias Squared')
    plt.title('Bias Squared & Alpha')
    plt.grid(True)
    plt.legend()

    # Plot for variance values
    plt.subplot(3, 1, 2)
    # srv = SmoothedRandomVariable(var_values, bandwidth_var)
    # y = np.vectorize(srv.cdf)(x)
    plt.plot(alpha_values, var_values, label='Variance')
    # plt.plot(x, y, label='Variance')
    plt.xlabel('Alpha')
    plt.ylabel('Variance')
    plt.title('Variance & Alpha')
    plt.grid(True)
    plt.legend()

    # Plot for MSE values
    plt.subplot(3, 1, 3)
    # srv = SmoothedRandomVariable(mse_values, bandwidth_mse)
    # y = np.vectorize(srv.cdf)(x)
    plt.plot(alpha_values, mse_values, label='MSE')
    # plt.plot(x, y, label='MSE')
    plt.xlabel('Alpha')
    plt.ylabel('MSE')
    plt.title('MSE & Alpha')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


def run_modelling(number_resample: int, location: float, resamples: list, N):
    # Поиск наилучшего alpha
    alpha_values = [i for i in np.arange(0.001, 0.501, 0.001)]
    mse_values = []  # СКО
    var_values = []  # Дисперсия
    bias_sqr_values = []  # Квадрат смещения

    for alpha in alpha_values:
        tm_estimator = TruncatedMean(alpha)
        tm_sample = []
        for i in range(number_resample):
            sample = resamples[i]
            tm = tm_estimator.estimate(sample)
            tm_sample.append(tm)

        modelling = Modelling(tm_sample, location, number_resample)
        modelling.run()

        bias_sqr_values.append(modelling.estimate_bias_sqr())
        var_values.append(modelling.estimate_var())
        mse_values.append(modelling.estimate_mse())


    # # Определение наилучшего значения alpha
    # best_alpha = alpha_values[np.argmin(mse_values)]
    # print(f'Наилучшее значение alpha: {best_alpha}')
    #
    # truncated_sample = [TruncatedMean(best_alpha).estimate(sample) for sample in resamples]
    #
    # modelling = Modelling(truncated_sample, location, number_resample)
    # modelling.run()

    return alpha_values, mse_values, var_values, bias_sqr_values


def without_emissions(location: float, scale: float, N: int, number_resample: int):
    rv = LaplaceRandomVariable(location, scale)
    generator = SimpleRandomNumberGenerator(rv)

    sample = generator.get(N)

    resamples = bootstrap_resample(sample, number_resample)

    modelling = run_modelling(number_resample, location, resamples, N)

    alpha_values = modelling[0]
    mse_values = modelling[1]
    var_values = modelling[2]
    bias_sqr_values = modelling[3]

    print_statistics(alpha_values, bias_sqr_values, var_values, mse_values)

    # print_statistics(modelling)

    # sample = modelling.get_sample()

    # bandwidth = 0.1

    # plot_samples(sample, bandwidth)
    plot_samples(alpha_values, bias_sqr_values, var_values, mse_values)


def with_symmetrical_emissions(location: float, scale: float, N: int, number_resample: int):
    rv = LaplaceRandomVariable(location, scale)
    tukey_rv = UniformRandomVariable(-5, 5)

    generator = TukeyNumberGenerator(rv, tukey_rv)

    sample = generator.get(N)

    resamples = bootstrap_resample(sample, number_resample)

    modelling = run_modelling(number_resample, location, resamples, N)

    alpha_values = modelling[0]
    mse_values = modelling[1]
    var_values = modelling[2]
    bias_sqr_values = modelling[3]

    print_statistics(alpha_values, bias_sqr_values, var_values, mse_values)

    # print_statistics(modelling)

    # sample = modelling.get_sample()

    # bandwidth = 0.1

    # plot_samples(sample, bandwidth)
    plot_samples(alpha_values, bias_sqr_values, var_values, mse_values)


def with_asymmetrical_emissions(location: float, scale: float, N: int, number_resample: int):
    rv = LaplaceRandomVariable(location, scale)

    tukey_rv = UniformRandomVariable(-5, 5)

    generator = AsymmetricTukeyNumberGenerator(rv, tukey_rv)

    sample = generator.get(N, 0.1)

    resamples = bootstrap_resample(sample, number_resample)

    modelling = run_modelling(number_resample, location, resamples, N)

    alpha_values = modelling[0]
    mse_values = modelling[1]
    var_values = modelling[2]
    bias_sqr_values = modelling[3]

    print_statistics(alpha_values, bias_sqr_values, var_values, mse_values)

    # print_statistics(modelling)

    # sample = modelling.get_sample()

    # bandwidth = 0.1

    # plot_samples(sample, bandwidth)
    plot_samples(alpha_values, bias_sqr_values, var_values, mse_values)
