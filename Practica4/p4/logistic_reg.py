import copy
import numpy as np

def sigmoid(z):
    """
    Compute the sigmoid of z

    Args:
        z (ndarray): A scalar, numpy array of any size.

    Returns:
        g (ndarray): sigmoid(z), with the same shape as z

    """

    g = 1 / (1 + (np.e ** -z)) # np.exp(-z)

    return g

#########################################################################
# logistic regression
#
def compute_cost(X, y, w, b, lambda_=None):
    """
    Computes the cost over all examples
    Args:
      X : (ndarray Shape (m,n)) data, m examples by n features
      y : (array_like Shape (m,)) target value
      w : (array_like Shape (n,)) Values of parameters of the model
      b : scalar Values of bias parameter of the model
      lambda_: unused placeholder

    Returns:
      cost: (scalar)         cost
    """

    m = X.shape[0]

    f_wb = sigmoid(X @ w + b)
    loss = (~y @ np.log(f_wb)) - ((1 - y) @ np.log(1 - f_wb))
    cost = np.sum(loss) / m

    return cost


def compute_gradient(X, y, w, b, lambda_=None):
    """
    Computes the gradient for logistic regression

    Args:
      X : (ndarray Shape (m,n)) variable such as house size
      y : (array_like Shape (m,1)) actual value
      w : (array_like Shape (n,1)) values of parameters of the model
      b : (scalar)                 value of parameter of the model
      lambda_: unused placeholder

    Returns
      dj_db: (scalar)                The gradient of the cost w.r.t. the parameter b.
      dj_dw: (array_like Shape (n,1)) The gradient of the cost w.r.t. the parameters w.
    """

    m = X.shape[0]

    dj_dw = X.T @ (sigmoid(X @ w + b) - y)
    dj_db = np.sum((sigmoid(X @ w + b) - y))

    dj_dw /= m
    dj_db /= m

    return dj_dw, dj_db

#########################################################################
# regularized logistic regression
#
def compute_cost_reg(X, y, w, b, lambda_=1):
    """
    Computes the cost over all examples
    Args:
      X : (array_like Shape (m,n)) data, m examples by n features
      y : (array_like Shape (m,)) target value 
      w : (array_like Shape (n,)) Values of parameters of the model      
      b : (array_like Shape (n,)) Values of bias parameter of the model
      lambda_ : (scalar, float)    Controls amount of regularization

    Returns:
      cost: (scalar)         cost 
    """

    m = X.shape[0]

    reg_factor = (lambda_ / (2 * m)) * np.sum(w ** 2)
    cost = compute_cost(X, y, w, b) + reg_factor

    return cost

def compute_gradient_reg(X, y, w, b, lambda_=1):
    """
    Computes the gradient for linear regression 

    Args:
      X : (ndarray Shape (m,n))   variable such as house size 
      y : (ndarray Shape (m,))    actual value 
      w : (ndarray Shape (n,))    values of parameters of the model      
      b : (scalar)                value of parameter of the model  
      lambda_ : (scalar,float)    regularization constant

    Returns
      dj_db: (scalar)             The gradient of the cost w.r.t. the parameter b. 
      dj_dw: (ndarray Shape (n,)) The gradient of the cost w.r.t. the parameters w. 
    """

    m = X.shape[0]

    reg_factor = (lambda_ * w / m)
    dj_dw, dj_db = compute_gradient(X, y, w, b)
    dj_dw += reg_factor
    
    return dj_dw, dj_db

#########################################################################
# gradient descent
#
def gradient_descent(X, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters, lambda_=None):
    """
    Performs batch gradient descent to learn theta. Updates theta by taking 
    num_iters gradient steps with learning rate alpha

    Args:
      X :    (array_like Shape (m, n)
      y :    (array_like Shape (m,))
      w_in : (array_like Shape (n,))  Initial values of parameters of the model
      b_in : (scalar)                 Initial value of parameter of the model
      cost_function:                  function to compute cost
      alpha : (float)                 Learning rate
      num_iters : (int)               number of iterations to run gradient descent
      lambda_ (scalar, float)         regularization constant

    Returns:
      w : (array_like Shape (n,)) Updated values of parameters of the model after
          running gradient descent
      b : (scalar)                Updated value of parameter of the model after
          running gradient descent
      J_history : (ndarray): Shape (num_iters,) J at each iteration,
          primarily for graphing later
    """

    J_history = []
    w = copy.deepcopy(w_in)
    b = copy.deepcopy(b_in)

    for _ in range(num_iters):
        dj_dw, dj_db = gradient_function(X, y, w, b, lambda_)

        w -= alpha * dj_dw
        b -= alpha * dj_db

        cost = cost_function(X, y, w, b)
        J_history.append(cost) 

    return w, b, J_history

#########################################################################
# predict
#
def predict(X, w, b):
    """
    Predict whether the label is 0 or 1 using learned logistic
    regression parameters w and b

    Args:
      X : (ndarray Shape (m, n))
      w : (array_like Shape (n,))      Parameters of the model
      b : (scalar, float)              Parameter of the model

    Returns:
      predict: (ndarray (m,1))         The predictions for X using a threshold at 0.5
    """

    f_wb = sigmoid(X @ w + b)
    predict = np.round(f_wb)    # 0 or 1 values

    return predict