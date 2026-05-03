import numpy as np


def gradient_descent(dfdx, dfdy, x, y, learning_rate=0.1, num_iterations=100):
    for iteration in range(num_iterations):
        x, y = x - learning_rate * dfdx(x, y), y - learning_rate * dfdy(x, y)
    return x, y


def f_example_3(x, y):
    return 2 * (x**2) + 3 * (y**3) - 2 * x * y - 10 * x


def dfdx_example_3(x, y):
    return 4 * x - 2 * y - 10


def dfdy_example_3(x, y):
    return 6 * y - 2 * x


num_iterations = 30
learning_rate = 0.25
x_initial = 0.5
y_initial = 0.6
print(
    "Gradient descent result: x_min, y_min =",
    gradient_descent(
        dfdx_example_3,
        dfdy_example_3,
        x_initial,
        y_initial,
        learning_rate,
        num_iterations,
    ),
)
