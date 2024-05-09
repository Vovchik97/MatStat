import math
# from abc import ABC, abstractmethod


# class Function(ABC):
#     @abstractmethod
#     def _k(self, x):
#         pass
#
#     @abstractmethod
#     def _K(self, x):
#         pass
#
#     @abstractmethod
#     def h(self, x):
#         pass
#
#
# class NormalCore(Function):
#     def _k(self, x):
#         return math.exp(-0.5 * x ** 2) / (math.sqrt(2 * math.pi))
#
#     def _K(self, x):
#         if x <= 0:
#             return 0.852 * math.exp(-math.pow((-x + 1.5774) / 2.0637, 2.34))
#         return 1 - 0.852 * math.exp(-math.pow((x + 1.5774) / 2.0637, 2.34))
#
#     def h(self, x):
#         return -x * self._k(x)
#
# class LaplaceCore(Function):
#     def _k(self, x):
#         return math.exp(-abs(x)) / 2
#
#     def _K(self, x):
#         if x <= 0:
#             return math.exp(0.5 * x) * 0.5
#         else:
#             return 1 - math.exp(-0.5 * x) * 0.5
#
#     def h(self, x):
#         return x * self._k(x)
#
#
# class BandwidthCalculator:
#     def __init__(self, sample, core):
#         self.sample = sample
#         self.core = core
#
#     def calculate_bandwidth(self):
#         n = len(self.sample)
#         sum_sample = sum(self.sample)
#         mean = sum_sample / n
#         sum_squares = sum((x - mean) ** 2 for x in self.sample)
#         hn = math.sqrt(sum_squares) / (n - 1)
#         delta = 1.0
#         while delta >= 0.001:
#             s = 0.0
#             for i in range(n):
#                 num = 0.0
#                 div = 0.0
#                 for j in range(n):
#                     if i != j:
#                         diff = (self.sample[j] - self.sample[i]) / hn
#                         num += self.core.h(diff) * (self.sample[j] - self.sample[i])
#                         div += self.core._k(diff)
#                 if div == 0.0:
#                     continue
#                 s += num / div
#             new_hn = - (1 / n) * s
#             delta = abs(new_hn - hn)
#             hn = new_hn
#         return hn


def k(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

def dk(x):
    return -x * k(x)

def calculate_optimal_h(arr: list, eps=0.01):
    def iteration(prev_h: float):
        result = 0

        for i in range(len(arr)):
            numerator = 0
            denominator = 0

            for j in range(len(arr)):
                if i != j:
                    numerator += dk((arr[i] - arr[j]) / prev_h) * (arr[i] - arr[j])
                    denominator += k((arr[i] - arr[j]) / prev_h)

            result += numerator / denominator

        return -result

    prev_h = 0.1
    cur_h = iteration(prev_h) / len(arr)

    while abs(cur_h - prev_h) <= eps:
        cur_h, prev_h = iteration(prev_h) / len(arr), cur_h

    return cur_h
