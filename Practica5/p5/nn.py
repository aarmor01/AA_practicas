import utils as ut

import numpy as np

# obtain results from a trained neural network
def feed_forward(theta1, theta2, X):
    m = X.shape[0]

    a1 = np.column_stack([np.ones((m, 1)), X])  # 5000 x 401
    z2 = a1 @ theta1.T                          # 5000 x 401 @ 401 x 25

    a2 = ut.sigmoid(z2)
    a2 = np.column_stack([np.ones((m, 1)), a2]) # 5000 x 26
    z3 = a2 @ theta2.T                          # 5000 x 26 @ 26 x 10

    a3 = ut.sigmoid(z3)                         # 5000 x 10

    return a3, a2, a1

def cost(theta1, theta2, X, y, lambda_):
    """
    Compute cost for 2-layer neural network. 

    Parameters
    ----------
    theta1 : array_like
        Weights for the first layer in the neural network.
        It has shape (2nd hidden layer size x input size + 1)

    theta2: array_like
        Weights for the second layer in the neural network. 
        It has shape (output layer size x 2nd hidden layer size + 1)

    X : array_like
        The inputs having shape (number of examples x number of dimensions).

    y : array_like
        1-hot encoding of labels for the input, having shape 
        (number of examples x number of labels).

    lambda_ : float
        The regularization parameter. 

    Returns
    -------
    cost : float
        The computed value for the cost function. 

    """
    m = X.shape[0]

    h0, _, _ = feed_forward(theta1, theta2, X)

    cost = np.sum((y * np.log(h0)) + ((1 - y) * np.log(1 - h0)))
    reg_factor = np.sum(pow(theta1[:, 1:], 2)) + np.sum(pow(theta2[:, 1:], 2))
    J = (-cost / m) + (lambda_ * reg_factor / (2 * m))

    return J

def backprop(theta1, theta2, X, y, lambda_):
    """
    Compute cost and gradient for 2-layer neural network. 

    Parameters
    ----------
    theta1 : array_like
        Weights for the first layer in the neural network.
        It has shape (2nd hidden layer size x input size + 1)

    theta2: array_like
        Weights for the second layer in the neural network. 
        It has shape (output layer size x 2nd hidden layer size + 1)

    X : array_like
        The inputs having shape (number of examples x number of dimensions).

    y : array_like
        1-hot encoding of labels for the input, having shape 
        (number of examples x number of labels).

    lambda_ : float
        The regularization parameter. 

    Returns
    -------
    J : float
        The computed value for the cost function. 

    grad1 : array_like
        Gradient of the cost function with respect to weights
        for the first layer in the neural network, theta1.
        It has shape (2nd hidden layer size x input size + 1)

    grad2 : array_like
        Gradient of the cost function with respect to weights
        for the second layer in the neural network, theta2.
        It has shape (output layer size x 2nd hidden layer size + 1)

    """
    m = X.shape[0]

    J = cost(theta1, theta2, X, y, lambda_)

    grad1 = np.zeros(theta1.shape)
    grad2 = np.zeros(theta2.shape)
    a3, a2, a1 = feed_forward(theta1, theta2, X)
    
    for i in range(m):    
        d3 = (a3[i] - y[i])[np.newaxis]            # 1 x 10

        gZ = (a2[i] * (1 - a2[i]))                 # 1 x 26
        d2 = (d3 @ theta2 * gZ)                    # 1 x 10 @ 10 x 26 * 1 x 26
        d2 = d2[:, 1:]                             # 1 x 25

        grad1 += d2.T @ a1[i, np.newaxis]          # 25 x 1 @ 1 x 401
        grad2 += d3.T @ a2[i, np.newaxis]          # 10 x 1 @ 1 x 26

    grad1[:, 0] /= m
    grad2[:, 0] /= m

    grad1[:, 1:] = (grad1[:, 1:] + lambda_ * theta1[:, 1:]) / m
    grad2[:, 1:] = (grad2[:, 1:] + lambda_ * theta2[:, 1:]) / m

    return J, grad1, grad2                         # 25 x 401; 10 x 26 

# unoptimized way to obtain gradient
def gradient(theta1, theta2, X, y, num_iters, alpha, lambda_=0):
    for _ in range(num_iters):
        J, grad1, grad2 = backprop(theta1, theta2, X, y, lambda_)

        theta1 -= alpha * grad1
        theta2 -= alpha * grad2

    return J, theta1, theta2

# function to be called by sciopt.minimize
def backprop_min(theta, X, y, t1_s, t2_s, lambda_):
    # reshape to adapt to the minimize function
    theta1 = np.reshape(theta[:t1_s[0] * t1_s[1]], (t1_s[0], t1_s[1]))
    theta2 = np.reshape(theta[t1_s[0] * t1_s[1]:], (t2_s[0], t2_s[1]))

    # train neural network
    J, grad1, grad2 = backprop(theta1, theta2, X, y, lambda_)

    # return results (adapted again to the sciopt.minimize function)
    return J, np.concatenate([np.ravel(grad1), np.ravel(grad2)])