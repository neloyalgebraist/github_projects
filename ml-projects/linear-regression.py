import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib
matplotlib.use('Agg')

from sklearn.linear_model import LinearRegression

path = "data/tvmarketing.csv"

adv = pd.read_csv(path)
print(adv.head())

adv.plot(x="TV", y="Sales", kind="scatter", c="black")
plt.savefig("tv_sales_scatter.png")

X = adv["TV"]
Y = adv["Sales"]
# Linear Regression with numpy.
m_numpy, b_numpy = np.polyfit(X, Y, 1)
print(f"Linear regression with numpy. Slope: {m_numpy}. Intercept: {b_numpy}")


def plot_linear_regression(
    X, Y, x_label, y_label, m, b, X_pred=np.array([]), Y_pred=np.array([])
):
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(X, Y, "o", color="black")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.plot(X, m * X + b, color="red")
    ax.plot(X_pred, Y_pred, "o", color="blue", markersize=8)
    plt.savefig(f"linear_regression_{x_label}_{y_label}.png")


plot_linear_regression(X, Y, "TV", "Sales", m_numpy, b_numpy)


def pred_numpy(m, b, X):
    Y = m * X + b
    return Y


X_pred = np.array([50, 120, 280])
Y_pred_numpy = pred_numpy(m_numpy, b_numpy, X_pred)

print(f"TV marketing expenses:\n{X_pred}")
print(f"Predictions of sales using NumPy linear regression:\n{Y_pred_numpy}")

# Linear Regression with Scikit-Learn

lr_sklearn = LinearRegression()

print(f"Shape of X array: {X.shape}")
print(f"Shape of Y array: {Y.shape}")

try:
    lr_sklearn.fit(X.values.reshape(-1, 1), Y)
except ValueError as err:
    print(err)

X_sklearn = X.values[:, np.newaxis]
Y_sklearn = Y.values[:, np.newaxis]

print(f"Shape of new X array: {X_sklearn.shape}")
print(f"Shape of new Y array: {Y_sklearn.shape}")

lr_sklearn.fit(X_sklearn, Y_sklearn)

m_sklearn = lr_sklearn.coef_
b_sklearn = lr_sklearn.intercept_

print(
    f"Linear regression using Scikit-Learn. Slope: {m_sklearn}. Intercept: {b_sklearn}"
)


def pred_sklearn(X, lr_sklearn):
    X_2D = X[:, np.newaxis]
    Y = lr_sklearn.predict(X_2D)
    return Y


Y_pred_sklearn = pred_sklearn(X_pred, lr_sklearn)

print(f"TV marketing expenses:\n{X_pred}")
print(f"Predictions of sales using Scikit-Learn linear regression:\n{Y_pred_sklearn.T}")


# Linear Regression using gradient descent.

X_norm = (X - np.mean(X)) / np.std(X)
Y_norm = (Y - np.mean(Y)) / np.std(Y)


def E(m, b, X, Y):
    return 1 / (2 * len(Y)) * np.sum((m * X + b - Y) ** 2)


def dEdm(m, b, X, Y):
    res = 1 / len(X) * np.dot(m * X + b - Y, X)
    return res


def dEdb(m, b, X, Y):
    res = 1 / len(Y) * np.sum(m * X + b - Y)
    return res


print(dEdm(0, 0, X_norm, Y_norm))
print(dEdb(0, 0, X_norm, Y_norm))
print(dEdm(1, 5, X_norm, Y_norm))
print(dEdb(1, 5, X_norm, Y_norm))


def gradient_descent(
    dEdm, dEdb, m, b, X, Y, learning_rate=0.001, num_iterations=1000, print_cost=False
):
    for iteration in range(num_iterations):
        m_new = m - learning_rate * dEdm(m, b, X, Y)
        b_new = b - learning_rate * dEdb(m, b, X, Y)
        m = m_new
        b = b_new
        if print_cost:
            print(f"Cost after iteration {iteration}: {E(m,b,X,Y)}")

    return m, b


print(gradient_descent(dEdm, dEdb, 0, 0, X_norm, Y_norm))
print(
    gradient_descent(
        dEdm, dEdb, 1, 5, X_norm, Y_norm, learning_rate=0.01, num_iterations=10
    )
)

m_initial = 0
b_initial = 0
num_iterations = 30
learning_rate = 0.1
m_gd, b_gd = gradient_descent(
    dEdm,
    dEdb,
    m_initial,
    b_initial,
    X_norm,
    Y_norm,
    learning_rate,
    num_iterations,
    print_cost=True,
)

print(f"Gradient descent result: m_min, b_min = {m_gd}, {b_gd}")

X_pred = np.array([50, 120, 280])
X_pred_norm = (X_pred - np.mean(X)) / np.std(X)
Y_pred_gd_norm = m_gd * X_pred_norm + b_gd
Y_pred_gd = Y_pred_gd_norm * np.std(Y) + np.mean(Y)

print(f"TV marketing expenses:\n{X_pred}")
print(f"Predictions of sales using Scikit-Learn linear regression:\n{Y_pred_sklearn.T}")
print(f"Predictions of sales using Gradient Descent:\n{Y_pred_gd}")
