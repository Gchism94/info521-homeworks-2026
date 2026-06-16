# %% [markdown]
r"""
## Linear regression in vector/matrix format

In lecture, we discussed how things quickly get messy as we increase the
dimensions of the input to linear models. Fortunately, we can use
representations and tools from linear algebra to simplify our lives, and
obtained a matrix equation for $\widehat{\mathbf{w}}$, the parameter vector
that minimizes the mean squared error loss function for *any* linear model:

$$\widehat{\mathbf{w}} = (\mathbf{X}^\intercal\mathbf{X})^{-1}\mathbf{X}^\intercal\mathbf{t}$$

In this notebook, we will implement this equation for the same simple linear
model (single-variable, two parameter) that we saw in the last homework.

Just like in the previous homework, you will need to add your code wherever
you see the markers that say `### YOUR CODE HERE ###`.
"""

# %% [markdown]
# Start by loading the data into the variables `x` and `t` (see the previous
# homework to do this).

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
import numpy as np
x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
### SOLUTION END ###

# %% [markdown]
# Next, we will construct the *design matrix*, $\mathbf{X}$. As a reminder, if
# we represent the $N$ inputs as vectors:
#
# $$\mathbf{x}_n = \begin{bmatrix}1 \\ x_n\end{bmatrix}$$
#
# then the design matrix is given by:
#
# $$
# \mathbf{X} =
# \begin{bmatrix}
# \mathbf{x}_1^\intercal \\
# \mathbf{x}_2^\intercal \\
# \vdots\\
# \mathbf{x}_N^\intercal
# \end{bmatrix}=
# \begin{bmatrix}
# 1 & x_1 \\
# 1 & x_2 \\
# \vdots \\
# 1 & x_n
# \end{bmatrix}
# $$
#
# This design matrix can be viewed as two $N\times 1$ column vectors stacked
# next to each other, the first one being populated with ones, and the other
# being populated with $x_1, \ldots, x_n$. Let us construct these vectors.

# %% [markdown]
# First construct an N x 1 vector of ones called `ones_vec` (where N is the
# number of training data points (i.e., the dimension of the `x` array
# that you created earlier in this notebook).
# Use NumPy's `ones_like` function to do this.
# https://numpy.org/doc/stable/reference/generated/numpy.ones_like.html

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
ones_vec = np.ones_like(x)
### SOLUTION END ###

# %% [markdown]
# Next, create the design matrix (call it `X`) by stacking `ones_vec` side by
# side with the `x` vector that you created earlier in this notebook. Use
# NumPy's `column_stack` function to do this:
# https://numpy.org/doc/stable/reference/generated/numpy.column_stack.html

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
X = np.column_stack((ones_vec, x))
### SOLUTION END ###

# %% [markdown]
# **Question**: What are the dimensions of $\mathbf{X}$? (Hint: You can use
# NumPy's
# [shape](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html)
# method to find out the shape of a NumPy array).

# %% [markdown]
# The other ingredient we need is the vector of targets (outputs),
# $\mathbf{t}$. Fortunately, we already have this (it's the variable `t` that
# you computed at the beginning of this homework).
#
# Now, use $\mathbf{t}$ and $\mathbf{X}$ to compute $\widehat{\mathbf{w}}$
# (call this variable `w`) using the matrix normal equation:
#
# $$\widehat{\mathbf{w}} = (\mathbf{X}^\intercal\mathbf{X})^{-1}\mathbf{X}^\intercal\mathbf{t}$$
#
# To do this, you may find the following NumPy functions/methods helpful:
# - Transpose (https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html)
# - To multiply matrices (encoded as NumPy ndarrays), you can use the `@` infix
# operator
# (https://numpy.org/doc/stable/reference/generated/numpy.matmul.html#numpy.matmul)
# - To take the inverse of a matrix, you can use `numpy.linalg.inv`

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
w = np.linalg.inv(X.T @ X) @ X.T @ t
### SOLUTION END ###

# %% [markdown]
# Now we can plot the best-fit line obtained. To do so, we need to create a
# matrix of test points in the same format as $\mathbf{X}$ above. A reminder
# that we are trying to compute the vector $\mathbf{t}_\text{test}$, where
#
# $$\mathbf{t}_\text{test} = \mathbf{X}_\text{test}\widehat{\mathbf{w}}$$

# %%
test_x = np.linspace(1896, 2012, 100)
test_X = np.column_stack((np.ones_like(test_x),test_x))
test_t = test_X @ w

# %%
from matplotlib import pyplot as plt
# %config InlineBackend.figure_format="retina"
plt.style.use("ggplot")
plt.plot(x,t, 'o')
plt.plot(test_x,test_t)
plt.xlabel("Year")
plt.ylabel("Winning time (s)")


# %% [markdown]
# Next, let us implement making a prediction with this model for a new input
# $\mathbf{x}_\text{new}$:
#
# $$\mathbf{t}_\text{new} = \widehat{\mathbf{w}}^\intercal\mathbf{x}_\text{new}$$

# %%
def predict(year):
    """Predict winning time given the year."""
    # First, construct the vector x_new. You can simply create a 1D numpy array
    # with two elements: (1, year) using numpy.array
    # (https://numpy.org/doc/stable/reference/generated/numpy.array.html)
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    x_new = np.array([1, year])
    ### SOLUTION END ###

    # Then, compute t_new using the equation above.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    t_new = w @ x_new
    ### SOLUTION END ###

    # Then, return t_new
    return t_new


# %% [markdown]
# Finally, use the `predict` function to predict the winning time for 2012.
# Verify that it matches up with the prediction you got in the previous
# homework.

# %%
winning_time_for_2012 = predict(2012)
print(winning_time_for_2012)

# %% [markdown]
# So far, you have fit a first-order polynomial to the data. Now, fit a
# second-order polynomial to the same data and compute the best fit parameter
# vector (call it `w_second_order`).
#
# **Hint**: mostly, you just need to change the design matrix (call the new
# design matrix `X_2`)---the actual line code to compute the best fit parameter
# vector $\widehat{\mathbf{w}}$ barely changes! To construct the design matrix
# for the second-order polynomial fit, you can simply add another array (you
# can use `numpy.power`
# (https://numpy.org/doc/stable/reference/generated/numpy.power.html#numpy.power)
# for this, or just use the `**` infix operator, which is overloaded by NumPy)
# to the tuple that you passed to the `column_stack` function in the case of
# the first-order polynomial fit.

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
X_2 = np.column_stack((ones_vec, x, x**2))
w_second_order = np.linalg.inv(X_2.T @ X_2) @ X_2.T @ t
print(w_second_order)
### SOLUTION END

# %% [markdown]
# ### Appendix: solving linear systems
#
# Our expression for the optimal value of $\mathbf{w}$ is:
#
# $$ \widehat{\mathbf{w}} =
# \left(\mathbf{X}^\intercal\mathbf{X}\right)^{-1}\mathbf{X}^\intercal\mathbf{t}
# $$
#
# Above, we have computed this by writing code to compute the right hand side.
# This involves performing a matrix inversion *which is almost always something
# to avoid* (as the matrix gets bigger, this becomes time consuming and
# numerically innacurate).
#
# Instead, we can go back a step to this equation:
#
# $$ \mathbf{X}^\intercal\mathbf{X}\mathbf{w} = \mathbf{X}^\intercal \mathbf{t} $$
#
# This is a system of linear equations (in general: $\mathbf{A}\mathbf{z} =
# \mathbf{B}$) and we can solve this directly for $\mathbf{w}$ using
# `numpy.linalg.solve`:

# %%
w_without_matrix_inversion = np.linalg.solve(X.T @ X, X.T @ t)
print(w_without_matrix_inversion)

# %% [markdown]
# Note that you get the same value of $\widehat{\mathbf{w}}$ as you did with
# the method involving matrix inversion.

# %% [markdown]
# For this system, it doesn't make any difference, but you don't have to get
# much bigger to see a difference.

# %% [markdown]
# ## Acknowledgements
#
# This notebook has been adapted from a notebook provided by the FCML textbook
# authors.

# %%
