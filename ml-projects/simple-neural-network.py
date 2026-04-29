# A single perceptron and two input nodes for linear regression
# forward propagation using matrix multiplication


from typing import ParamSpecArgs

parameters = utils.initialize_parameters(2)
print(parameters)


def forward_propagation(X, parameters):
    """
    Arguments:
        X -- input data of size (n_x,m), where n_x is the dimension input (in our example is 2) and m is the number of training samples.
        parameters -- python dictionary containing your parameters (output of initialization function)

    Returns:
        Y_hat -- The output of size (1, m)
    """
    W = parameters["W"]
    b = parameters["b"]

    Z = W @ X + b
    Y_hat = Z

    return Y_hat


def compute_cost(Y_hat, Y):
    """
    Computes the cost function as a sum of squares

    Arguments:
    Y_hat -- The output of the neural network of shape (n_y, number of examples)
    Y -- "true" labels vector of shape (n_y, number of examples)

    Returns:
    cost -- sum of squares scaled by 1/(2*number of exampless)
    """
    m = Y.shape[1]
    cost = np.sum((Y_hat - Y) ** 2) / (2 * m)

    return cost


def nn_model(X, Y, num_iterations=1000, print_cost=False):
    """
    Arguments:
    X -- dataset of shape (n_x, number of examples)
    Y -- labels of shape (1, number of examples)
    num_iterations -- number of iterations in the loop
    print_cost -- if true, print the cost every iteration

    Returns:
    parameters -- parameters learnt by the model. They can then be used to make predictions.
    """

    n_x = X.shape[0]
    parameters = utils.initialize_parameters(n_x)

    for i in range(0, num_iterations):

        Y_hat = forward_propagation(X, parameters)

        cost = compute_cost(Y_hat, Y)

        parameters = utils.train_nn(parameters, Y_hat, X, Y, learning_rate=0.001)

        if print_cost:
            if i % 100 == 0:
                print("Cost after iteration %i: %f" % (i, cost))

    return parameters


df = pd.read_csv("data/toy_dataset.csv")
df.head()

X = np.array(df[["x1", "x2"]]).T
Y = np.array(df["y"]).reshape(1, -1)

parameters = nn_model(X, Y, num_iterations=5000, print_cost=True)


def predict(X, parameters):
    W = parameters["W"]
    b = parameters["b"]
    z = np.dot(W, X) + b
    return Z


Y_hat = predict(X, parameters)
df["y_hat"] = y_hat[0]
for i in range(10):
    print(
        f"(x1,x2) = ({df.loc[i,'x1']:.2f}, {df.loc[i,'x2']:.2f}): Actual value: {df.loc[i,'y']:.2f}. Predicted value: {df.loc[i,'y_hat']:.2f}"
    )
