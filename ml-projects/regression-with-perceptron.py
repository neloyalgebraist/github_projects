import numpy as np
import pandas as pd
from pandas.core.arrays import numpy_
from pandas.core.frame import treat_as_nested

path = "data/tvmarketing.csv"
adv = pd.read_csv(path)

adv.head()
adv_norm = (adv - np.mean(adv)) / np.std(adv)

X_norm = adv_norm["TV"]
Y_norm = adv_norm["Sales"]

X_norm = np.array(X_norm).reshape((1, len(X_norm)))
Y_norm = np.array(Y_norm).reshape((1, len(Y_norm)))

print("The shape of X_norm: " + str(X_norm.shape))
print("The shape of Y_norm: " + str(Y_norm.shape))
print("I have m = %d training examples!" % (X_norm.shape[1]))


def layer_sizes(X, Y):
    """
    Arguments:
    X -- input dataset of shape (input size, number of examples)
    Y -- labels of shape (output size, number of examples)

    Returns:
    n_x -- the size of the input layer
    n_y -- the size of the output layer
    """
    n_x = X.shape[0]
    n_y = Y.shape[0]

    return (n_x, n_y)


n_x, n_y = layer_sizes(X_norm, Y_norm)
print("The size of the input layer is: n_x = " + str(n_x))
print("The size of the output layer is: n_y = " + str(n_y))


def initialize_parameters(n_x, n_y):
    """
    Returns:
    params -- python dictionary containing your parameters:
                    W -- weight matrix of shape (n_y,n_x)
                    b -- bias value set as a vector of shape (n_y,1)
    """
    W = np.random.randn(n_y, n_x) * 0.01
    b = np.zeros((n_y, 1))

    parameters = {"W": W, "b": b}

    return parameters


parameters = initialize_parameters(n_x, n_y)
print("W = " + str(parameters["W"]))
print("b = " + str(parameters["b"]))


def forward_propagation(X, parameters):
    """
    Arguments:
    X -- input data of size (n_x, m)
    parameters -- python dictionary containing your parameters (output of initialization function)

    Returns:
    Y_hat -- The output
    """
    W = parameters["W"]
    b = parameters["b"]

    Z = np.matmul(W, X) + b
    Y_hat = Z

    return Y_hat


Y_hat = forward_propagation(X_norm, parameters)
print("Some elements of output vector Y_hat:", Y_hat[0, 0:5])


def compute_cost(Y_hat, Y):
    """
    Computes the cost function as a sum of squares

    Arguments:
    Y_hat -- The output of the neural network of shape (n_y, number of examples)
    Y -- "true" labels vector of shape (n_y, number of examples)

    Returns:
    cost -- sum of squares scaled by 1/(2*number of examples)
    """
    m = Y_hat.shape[1]
    cost = np.sum((Y_hat - Y) ** 2) / (2 * m)

    return cost


print("cost = " + str(compute_cost(Y_hat, Y_norm)))


def backward_propagation(Y_hat, X, Y):
    """
    Implements the backward propagation, calculting gradients

    Arguments:
    Y_hat -- the output of the neural network of shape (n_y, number of examples)
    X -- input data of shape (n_x, number of examples)
    Y -- "true" labels vector of shape (n_y, number of examples)

    Returns:
    grads -- python dictionary containing gradients with respect to different parameters
    """
    m = X.shape[1]
    dZ = Y_hat - Y
    dW = 1 / m * np.dot(dZ, X.T)
    db = 1 / m * np.sum(dZ, axis=1, keepdims=True)

    grads = {"dW": dW, "db": db}

    return grads


grads = backward_propagation(Y_hat, X_norm, Y_norm)

print("dW = " + str(grads["dW"]))
print("db = " + str(grads["db"]))


def update_parameters(parameters, grads, learning_rate=1.2):
    """
    Updates parameters using the gradient descent update rule
    Arguments:
    parameters -- python dictionary containing initialize_parameters
    grads -- python dictionary containing gradients
    learning_rate -- learning_rate parameter for gradient descent

    Returns:
    parameters -- python dictionary containing updated parameters
    """
    W = parameters["W"]
    b = parameters["b"]

    dW = grads["dW"]
    db = grads["db"]

    W = W - learning_rate * dW
    b = b - learning_rate * db

    parameters = {"W": W, "b": b}
    return parameters


parameters_updated = update_parameters(parameters, grads)

print("W updated = " + str(parameters_updated["W"]))
print("b updated = " + str(parameters_updated["b"]))


def nn_model(X, Y, num_iterations=10, learning_rate=1.2, print_cost=False):
    """
    Arguments:
    X -- dataset of shape (n_x, number of examples)
    Y -- labels of shape (n_y, number of examples)
    num_iterations -- number of iterations in the loop
    learning_rate -- learning rate parameter for gradient descent
    print_cost -- if True, print the cost every iteration

    Returns:
    parameters -- parameters learnt by the model. They can then be used to make predictions.
    """
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[1]

    parameters = initialize_parameters(n_x, n_y)

    for i in range(0, num_iterations):
        Y_hat = forward_propagation(X, parameters)
        cost = compute_cost(Y_hat, Y)
        grads = backward_propagation(Y_hat, X, Y)
        parameters = update_parameters(parameters, grads, learning_rate)
        if print_cost:
            print("cost after iteration %i: %f" % (i, cost))

    return parameters


parameters_simple = nn_model(
    X_norm, Y_norm, num_iterations=30, learning_rate=1.2, print_cost=True
)
print("W = " + str(parameters_simple["W"]))
print("b = " + str(parameters_simple["b"]))

W_simple = parameters["W"]
b_simple = parameters["b"]


def predict(X, Y, parameters, X_pred):
    W = parameters["W"]
    b = parameters["b"]

    if isinstance(X, pd.Series):
        X_mean = np.mean(X)
        X_std = np.std(X)
        X_pred_norm = ((X_pred - X_mean) / X_std).reshape((1, len(X_pred)))
    else:
        X_mean = np.array(np.mean(X)).reshape((len(X.axes[1]), 1))
        X_std = np.array(np.std(X)).reshape((len(X.axes[1]), 1))
        X_pred_norm = (X_pred - X_mean) / X_std

    Y_pred_norm = np.matmul(W, X_pred_norm) + b
    Y_pred = Y_pred_norm * np.std(Y) + np.mean(Y)

    return Y_pred[0]


X_pred = np.array([50, 120, 280])
Y_pred = predict(adv["TV"], adv["Sales"], parameters_simple, X_pred)
print(f"TV marketing expenses:\n{X_pred}")
print(f"Predictions of sales:\n{Y_pred}")

df = pd.read_csv("data/AmesHousing.csv")

X_multi = df[["GrLivArea", "OverallQual"]]
Y_multi = df["SalePrice"]

display(X_multi)
display(Y_multi)

X_multi_norm = (X_multi - np.mean(X_multi)) / np.std(X_multi)
Y_multi_norm = (Y_multi - np.mean(Y_multi)) / np.std(Y_multi)

X_multi_norm = np.array(X_multi_norm).T
Y_multi_norm = np.array(Y_multi_norm).reshape((1, len(Y_multi_norm)))

print("The shape of X: " + str(X_multi_norm.shape))
print("The shape of Y: " + str(Y_multi_norm.shape))
print("I have m = %d training examples!" % (X_multi_norm.shape[1]))

parameters_multi = nn.model(
    X_multi_norm, Y_multi_norm, num_iterations=100, print_cost=True
)

print("W = " + str(parameters_multi["W"]))
print("b = " + str(parameters_multi["b"]))

W_multi = parameters_multi["W"]
b_multi = parameters_multi["b"]

X_pred_multi = np.array([[1710, 7], [1200, 6], [2200, 8]]).T
Y_pred_multi = predict(X_multi, Y_multi, parameters_multi, X_pred_multi)

print(f"Ground living area, square feet:\n{X_pred_multi[0]}")
print(f"Rates of the overall quality of material and finish, 1-10:\n{X_pred_multi[1]}")
print(f"Predictions of sales price, $:\n {np.round(Y_pred_multi)}")
