import numpy as np
import matplotlib.pyplot as plt

# x1 = x0 - a(df/dx)(x0).
# a = learning rate , n = number of iterations


def f_example_1(x):
    return np.exp(x) - np.log(x)


def dfdx_example_1(x):
    return np.exp(x) - 1 / x


def gradient_descent(dfdx, x, learning_rate=0.1, num_iterations=100):
    for iteration in range(num_iterations):
        x = x - learning_rate * dfdx(x)
    return x


num_iterations = 25
learning_rate = 0.1
x_initial = 1.6
print(
    "Gradient descent result: x_min =",
    gradient_descent(dfdx_example_1, x_initial, learning_rate, num_iterations),
)
