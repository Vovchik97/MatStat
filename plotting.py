import matplotlib.pyplot as plt
import numpy as np

from estimations import TruncatedMean
from modelling import bootstrap_resample, Modelling
from random_number_generator import SimpleRandomNumberGenerator, TukeyNumberGenerator, AsymmetricTukeyNumberGenerator
from random_variables import LaplaceRandomVariable, SmoothedRandomVariable, UniformRandomVariable

POINTS = 100


# def print_statistics(modelling: Modelling):
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

    # Plot for bias squared values
    plt.subplot(3, 1, 1)
    plt.plot(alpha_values, bias_sqr_values, label='Bias Squared')
    plt.xlabel('Alpha')
    plt.ylabel('Bias Squared')
    plt.title('Bias Squared vs Alpha')
    plt.grid(True)
    plt.legend()

    # Plot for variance values
    plt.subplot(3, 1, 2)
    plt.plot(alpha_values, var_values, label='Variance')
    plt.xlabel('Alpha')
    plt.ylabel('Variance')
    plt.title('Variance vs Alpha')
    plt.grid(True)
    plt.legend()

    # Plot for MSE values
    plt.subplot(3, 1, 3)
    plt.plot(alpha_values, mse_values, label='MSE')
    plt.xlabel('Alpha')
    plt.ylabel('MSE')
    plt.title('MSE vs Alpha')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()



def run_modelling(number_resample: int, location: float, resamples: list, N):
    # Поиск наилучшего alpha
    alpha_values = [i for i in np.arange(0.01, 0.51, 0.01)]
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

        mse_values.append(modelling.estimate_mse())
        var_values.append(modelling.estimate_var())
        bias_sqr_values.append(modelling.estimate_bias_sqr())


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

    # print_statistics(modelling)

    # sample = modelling.get_sample()

    # bandwidth = 0.1

    # plot_samples(sample, bandwidth)
    plot_samples(alpha_values, mse_values, var_values, bias_sqr_values)


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

    # print_statistics(modelling)

    # sample = modelling.get_sample()

    # bandwidth = 0.1

    # plot_samples(sample, bandwidth)
    plot_samples(alpha_values, mse_values, var_values, bias_sqr_values)


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

    # print_statistics(modelling)

    # sample = modelling.get_sample()

    # bandwidth = 0.1
    # plot_samples(sample, bandwidth)
    plot_samples(alpha_values, mse_values, var_values, bias_sqr_values)
