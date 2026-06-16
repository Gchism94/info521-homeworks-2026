# %% [markdown]
r"""
# Nonlinear regression with a linear model

## Overview

In this notebook, you will implement a polynomial regression model.
Fill in the missing pieces of code at the markers that say
`### YOUR CODE HERE ###`.

Additionally, there are a few questions for which you will enter answers in the
spots marked `### YOUR ANSWER HERE ###`.


Start by loading the Olympic data into the variables `x` and `t`, as you have
done in prior homeworks.
"""

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
import numpy as np
x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
### SOLUTION END ###


# %% [markdown]
# The `PolynomialRegressionModel` class has a constructor that takes a single
# argument, the order of the polynomial.

# %%
class PolynomialRegressionModel:
    """Polynomial regression model"""

    def __init__(self, order: int):
        """
        Class constructor.

        Args:
            order: The order of the polynomial to fit
        """
        self.w = None

        # The `order` attribute is set in the constructor and is thus
        # accessible within all class methods that have `self` as the first
        # argument.
        self.order = order

    def get_design_matrix_shape(self, x):
        """Returns the shape of the design matrix"""
        # This function should return a 2-tuple, where the first element of the
        # tuple is the number of rows in the design matrix, and the second
        # element is the number of columns.  You can get the number of rows by
        # inspecting the shape of the input `x` (you did this in the previous
        # homework!) and taking the first element of the shape tuple.

        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return (x.shape[0], self.order + 1)
        ### SOLUTION END ###

    @staticmethod
    def initialize_design_matrix(shape):
        """Returns a matrix with the required dimensions for the design matrix,
        filled with zeros."""
        # Initialize the design matrix as an array filled with zeros, with the
        # correct dimensions (which you computed in the previous step).  Use
        # the numpy.zeros function to do this
        # (https://numpy.org/doc/stable/reference/generated/numpy.zeros.html).

        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return np.zeros(shape)
        ### SOLUTION END ###

    def fill_design_matrix(self, X, x):
        """Fills in the design matrix with entries based on the training data."""
        # Then, use a for-loop to fill in the columns of design matrix one by
        # one.  What should the total number iterations of the loop be? (Hint:
        # it depends on the polynomial order) To set the k-th column in the
        # design matrix, you can use the Numpy slice operator
        # (https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding)
        #
        # e.g., the line of code below will set the k-th column of the array
        # `X` to an array whose elements are the squares of the input training
        # data vector.
        # X[:, k] = x**2

        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        for k in range(self.order + 1):
            X[:, k] = x**k
        ### SOLUTION END ###

    def create_design_matrix(self, x):
        """Create design matrix for polynomial regression from a vector of inputs."""
        X_shape = self.get_design_matrix_shape(x)
        X = self.initialize_design_matrix(X_shape)
        self.fill_design_matrix(X, x)
        return X

    def compute_mse_loss(self, x, t):
        """Returns the mean squared error loss"""
        error = self.predict(x) - t
        N = error.shape[0]
        L = (error.T @ error)/N
        return L

    def train(self, x, t):
        """
        Train the model using the normal equation.
        That is, find the best-fit parameters using the matrix normal equation.
        """

        X = self.create_design_matrix(x)

        # Set self.w to equal the best fit parameters computed using the matrix
        # normal equation (you did this in the previous homework).
        self.w = np.linalg.inv(X.T @ X) @ X.T @ t

    def predict(self, x):
        """Returns a prediction made by the model."""
        if self.w is None:
            raise ValueError(
                "The model has not been trained yet! "
                "Please train it before making a prediction."
            )

        # This function should return the inner product of the parameter vector
        # w and the new input x for which we would like to make a prediction.

        # In the previous homework, you constructed the input vector x_new
        # 'manually' by creating a numpy array with the elements (1, year).
        # This becomes a pain when you go to higher orders. Additionally, it is
        # desirable to have a 'vectorized' `predict` method, so that you can
        # make predictions for multiple years efficiently.

        # Basically, you will need to construct a design matrix from the array
        # of inputs that you want to make predictions with. Use the
        # `create_design_matrix` method to do this.
        X = self.create_design_matrix(x)

        # Finally, return the vector of predictions obtained by multiplying `X`
        # and the model parameter vector `w`.

        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return X @ self.w
        ### SOLUTION END ###


# %% [markdown]
# You now have a class that can be used to instantiate polynomial regression
# models of different orders. Let us see what the outputs of these models look
# like.

# %%
x_predict = np.linspace(min(x), max(x))
from matplotlib import pyplot as plt
# %config InlineBackend.figure_format = "retina"
plt.style.use("ggplot")

# Set the maximum order
MAX_ORDER = 8

for n in range(1, MAX_ORDER + 1):
    fig, axes = plt.subplots()
    axes.plot(x, t, 'o')
    model = PolynomialRegressionModel(n)
    model.train(x, t)
    predictions = model.predict(x_predict)
    axes.plot(x_predict, predictions, label = f"Polynomial order: {n}")
    axes.set_xlabel("Year")
    axes.set_ylabel("Winning Time (s)")
    plt.legend()


# %% # Scaling [markdown]
#
# At some point, you will see the plots start to look weird -- the fits will
# start to look way off.
#
# **Question 1 (1 point)** At which polynomial order do you start to see the
# fit getting worse?
#
# **Answer:** ### YOUR ANSWER HERE ###
#
# Mathematically, the sizes of the values of variables (such as x) could be
# arbitrarily large.  However, when we go to manipulate those values on a
# computer, we need to be careful.
#
# E.g., in these exercises we are taking powers of values and if the values are
# large, then taking a large power of the variable may exceed what can be
# represented numerically in the computer.
#
# For example, in the Olympics data (both men's and women's), the input x
# values are years in the 1000's.  If your model is, say, polynomial order 5,
# then you're taking a large number to the power of 5, which is the order of a
# quadrillion! Python floating point numbers have trouble representing this
# many significant digits.
#
# In this homework, you will construct regression models for polynomials of various
# orders. However, as you saw above, as the order of the polynomial increases,
# you will run into numerical issues. To avoid this, we will *scale* the data
# prior to training the model.
#
# This is a very common task in general data manipulation, called "linear
# scaling" (or a "linear transformation")
#
# The `scale` function below takes an array and returns a new array with the
# elements of the original array scaled to be between 0 and 1, along with the
# minimum of the original array and its 'range' (i.e., the difference between
# the maximum and minimum elements of the array). We will use the minimum and
# the range to 'unscale' the scaled inputs and predictions when it comes time
# to plot the predictions, in order to make our plots more clearly
# interpretable.

# %%
def scale(array):
    """Returns a linearly scaled version of the input array
    with elements in [0, 1], along with the minimum and the
    range of the array.
    """

    # Create two variables, `array_min` and `array_max`, set to the minimum and
    # maximum of the array respectively
    # (use numpy.min: https://numpy.org/doc/stable/reference/generated/numpy.min.html
    # and numpy.max: https://numpy.org/doc/stable/reference/generated/numpy.max.html)
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    array_min = np.min(array)
    array_max = np.max(array)
    ### SOLUTION END ###

    # Create a variable `array_range` that equals the difference of `array_min`
    # and `array_max`.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    array_range = array_max - array_min
    ### SOLUTION END ###

    # Create a variable called `scaled_array` whose elements are the elements
    # of `array`, except that you subtract `array_min` from each element and then
    # divide the element by `array_range`. Don't use a for-loop for this! You can
    # take advantage of numpy's broadcasting
    # (https://numpy.org/doc/stable/user/basics.broadcasting.html) to do this
    # in a single line of code.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    scaled_array = (array - array_min)/array_range
    ### SOLUTION END ###

    return scaled_array, array_min, array_range


# %% [markdown]
# Now we can use the `scale` function to scale `x` and `t` prior to training
# and prediction.

# %%
# Set the maximum order
max_order = 8

def make_scaled_plot(n, x, t):
    """Create plot showing data and best-fit curve for polynomial regression
    with scaled data."""
    x_scaled, x_min, x_range = scale(x)
    t_scaled, t_min, t_range = scale(t)
    x_predict = np.linspace(0, 1.1)
    fig, axes = plt.subplots()
    axes.plot(x, t, 'o')
    model = PolynomialRegressionModel(n)
    model.train(x_scaled, t_scaled)
    t_predict = model.predict(x_predict)

    # Note that we 'unscale' x_predict and t_predict below for a
    # more interpretable plot.
    axes.plot(
        x_predict*x_range + x_min,
        t_predict*t_range + t_min,
        label = f"Polynomial order: {n}"
    )
    axes.set_xlabel("Year")
    axes.set_ylabel("Winning Time (s)")
    plt.legend()

    # Save the plot to a file in the `images` directory.
    fig.savefig(f"images/polyfit_scaled_{n}.pdf")

for n in range(1, max_order + 1):
    make_scaled_plot(n, x, t)


# %% [markdown]
# Much nicer!
#
# Your 8-th order polynomial figure should match up with Figure 1.10 in FCML.

# %% [markdown]
# # Overfitting
#
# As we increase the order of the polynomial, the best-fit line seems to be
# getting somewhat closer to the training data points. However, the predictions
# for years outside the training data range seem quite suspect. What you are
# seeing here is called *overfitting*, where the model is paying too much
# attention to the training data and is unable to *generalize* to unseen data.
#
# We can see at which polynomial order overfitting starts to set in, by using a
# *validation* dataset. This could be a separate dataset, or we could set aside
# some portion of our training data as the validation set.
#
# Following FCML, let us set aside data post-1979 as the validation set.

# %%
x_train, x_validation = x[:-8], x[-8:]
t_train, t_validation = t[:-8], t[-8:]

x_train_scaled, _, _ = scale(x_train)
x_validation_scaled, _, _ = scale(x_validation)

t_train_scaled, _, _ = scale(t_train)
t_validation_scaled, _, _ = scale(t_validation)


# %% [markdown]
# Now, let us plot training loss and validation loss as a function of
# polynomial order.

# %%
def compute_loss(n):
    """Compute train and validation loss for a regression model for a
    polynomial of a given order."""
    model = PolynomialRegressionModel(n)
    model.train(x_train_scaled, t_train_scaled)
    train_loss = model.compute_mse_loss(x_train_scaled, t_train_scaled)
    validation_loss = model.compute_mse_loss(x_validation_scaled, t_validation_scaled)
    return train_loss, validation_loss


# %%
losses = [compute_loss(n) for n in range(1, 9)]

# %%
fig, axes = plt.subplots()
axes.plot(range(1,9), [loss[0] for loss in losses], label="Training loss")

# Set axis labels
axes.set_xlabel("Polynomial order")
axes.set_ylabel("Training loss")

# Save the plot to a file.
fig.savefig("images/training_loss.pdf")

# %%

# %%
fig, axes = plt.subplots()
axes.plot(range(1,9), [loss[1] for loss in losses], label="Validation loss")
axes.set_xlabel("Polynomial order")
axes.set_ylabel("Validation loss")
axes.set_yscale("log")
plt.tight_layout()
fig.savefig("images/validation_loss.pdf")

# %% [markdown]
# The plot above is a bit different from FCML Figure 1.12(b), since the figure
# in the textbook is generated with the scaling applied *prior* to the
# train-validation data split, while the plot above is generated with the
# scaling applied *after* the train-validation data split.
#
# Scaling the data before splitting it is a common error that results in *data leakage* from the training set to the test set (since the scaled test set will be affected by the values in the training set, as those values influence the scaling transformation).
#
# **Do not scale the data before splitting it!**
#
# We can clearly see that while the training loss keeps going down with
# increasing polynomial order, the validation loss tends to keep increasing.

# %% [markdown]
# # Cross-validation
#
# Earlier in this notebook we took data from years after 1979 as our validation
# set. But what if we had taken a different subset of our data as the
# validation set? When you have relatively limited data, your model's
# performance may be sensitive to the choice of validation set. One way to
# overcome this limitation is to use *cross-validation* (CV). The basic
# procedure is as follows:
#
# 1. Create $K$ equal-sized non-overlapping subsets (called 'folds') of the
# training data.
# 2. For each fold $k$, train the model on the other K-1 folds and then compute
# the loss on fold number $k$.
# 3. Average the loss over all folds.
#
#
# To use CV for model selection, you would loop over the different models you
# are deciding between (in our case, the different polynomial orders), and
# select the model that achieves the lowest average loss across all folds.
#
# Note that the folds must be created **before** looping over the models,
# otherwise you introduce an additional confounding variable into your
# experiment.
#
# Below, we will implement K-fold cross-validation for our polynomial
# regression model.
#
# First, we will stack our inputs and outputs to form a combined array
# called `stack`.

# %%
stack = np.column_stack((x, t))

# %% [markdown]
# **Question 2:** What do you expect the dimensions of `stack` to be? Now
# check the dimensions using NumPy's `shape` method. Was your guess correct?
#
# **Answer:** ### YOUR ANSWER HERE ###

# %% [markdown]
# ## Reproducibility and random seed setting
#
# The next step will involve randomly shuffling the data. However, when
# conducting machine learning experiments, it is useful to be able to set the
# random seed for the sake of reproducibility.
#
# In the line below, we will initialize NumPy's random number generator with a
# given seed.
# You can choose any seed you want. For the purposes of demonstration, we will
# set the seed to `0`.

# %%
rng = np.random.default_rng(0)
stack_shuffled = rng.permutation(stack)


# %% [markdown]
# With the shuffling done, let us now move on to the actual implementation of
# cross-validation, which is done in the `run_K_fold_cv` function below.

# %%
def run_K_fold_cv(K: int, P: int, data):
    """Run K-fold cross validation over polynomial orders.
    Args:
        K: Number of folds
        P: Maximum polynomial order
        data: Training data array
    Returns:
        List of tuples of the form:
        (mean validation loss over all folds, polynomial order)
    """

    # Use NumPy's `array_split` method
    # (https://numpy.org/doc/stable/reference/generated/numpy.array_split.html#numpy-array-split)
    # to split the data into K folds of approximately equal size.

    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    folds = np.array_split(data, K)
    ### SOLUTION END ###


    # Initialize an empty array of size P called `mean_validation_losses` to
    # hold the mean validation loss across all folds for each polynomial order.
    # You can use NumPy's `zeros` method for this.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    mean_validation_losses = np.zeros(P)
    ### SOLUTION END ###

    for p in range(1, P + 1):
        # Create an variable `model` and set its value to an instance
        # of the `PolynomialRegressionModel` class for polynomial order `p`.
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        model = PolynomialRegressionModel(p)
        ### SOLUTION END ###

        # Initialize an empty array to contain the validation loss for each
        # fold considered for a particular polynomial order.
        order_validation_losses = np.zeros(K)
        for k in range(K):
            training_set = np.concatenate([folds[i] for i in range(K) if i != k])
            validation_set = folds[k]

            x_train = training_set[:,0]
            t_train = training_set[:,1]

            # Train the model with `x_train_scaled` and `t_train_scaled`,
            # which are scaled versions of `x_train` and `t_train`.
            # Store the values of the minimum and range of `x_train` and
            # `t_train` that are output by the `scale` function---you'll
            # need them later on.
            ### YOUR CODE HERE ###
            ### SOLUTION START ###
            x_train_scaled, x_train_min, x_train_range = scale(x_train)
            t_train_scaled, t_train_min, t_train_range = scale(t_train)
            model.train(x_train_scaled, t_train_scaled)
            ### SOLUTION END ###

            # Construct `x_validation_scaled` and `t_validation_scaled` using
            # the transformation parameters (minimum and range) obtained from
            # scaling the training data.
            x_validation = validation_set[:,0]
            t_validation = validation_set[:,1]

            x_validation_scaled = (x_validation - x_train_min)/x_train_range
            t_validation_scaled = (t_validation - t_train_min)/t_train_range

            # Create a variable `validation_loss` and set it equal to
            # the MSE loss (use the `compute_mse_loss` method
            # implemented earlier) on the validation set.
            ### YOUR CODE HERE ###
            ### SOLUTION START ###
            validation_loss = model.compute_mse_loss(x_validation_scaled,
                                                    t_validation_scaled)
            ### SOLUTION END ###
            order_validation_losses[k] = validation_loss

        # Create a variable `mean_validation_loss` and set it equal
        # to the mean of `order_validation_losses`. Use NumPy's `mean` method for this
        # (https://numpy.org/doc/stable/reference/generated/numpy.mean.html#numpy.mean)
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        mean_validation_loss = order_validation_losses.mean()
        ### SOLUTION END ###

        mean_validation_losses[p - 1] = mean_validation_loss

    # Plot mean loss vs polynomial order.
    fig, axes = plt.subplots()
    axes.plot(range(1, P + 1), mean_validation_losses)

    # Set the x-axis label to "Polynomial order",
    # and the y-axis label to "Mean loss"
    # (see how this was done earlier in this notebook)
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    axes.set_xlabel("Polynomial order")
    axes.set_ylabel("Mean loss")
    ### SOLUTION END ###

    # Save the figure
    fig.savefig(f"images/{K}_fold_cv_loss.pdf")

# %% [markdown]
# Let us first try running 5-fold cross-validation.

# %%
run_K_fold_cv(5, 8, stack_shuffled)

# %% [markdown]
# Now, create a similar plot, but running LOOCV instead of 5-fold CV.

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
run_K_fold_cv(x.shape[0], 8, stack_shuffled)
### SOLUTION END ###

# %% [markdown]
# The figure you get above should be similar in shape (but not identical, we
# scaled the data *after* splitting it instead of before) FCML Figure 1.15,
# modulo the y axis scale (since that depends on the specific scaling procedure
# used).
#
# Note that the end conclusion is the same (that is, a polynomial of order 3
# works best).
# %%

# %%

# %%
