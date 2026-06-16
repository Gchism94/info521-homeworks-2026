#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
"""
# Linear regression


In this notebook, you will implement your very first machine learning model!

You will perform linear regression to try and predict the winning time of the
mens 100m sprint at the 2012 Olympics, using historical winning times.

There are a few places in this notebook where you will need to fill in the correct code.
These places are marked with the marker `### YOUR CODE HERE ###`.

Let us start by loading the Olympic 100m mens data (`data100m.csv`) and then
copying the first and second columns into the numpy variables `x` and `t`.
"""


# %%
import numpy as np

x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)


# %% [markdown]
"""
## Plotting

Let's start by plotting the data. We will do so using `matplotlib`, a powerful
Python plotting package.
"""


# %%
from matplotlib import pyplot as plt

# Display figures inline in the notebook
# %matplotlib inline

# Increase the resolution of the inline figures for high-resolution
# screens, e.g., on MacBooks with retina displays.

# %config InlineBackend.figure_format="retina"

# %%
# Set the plot style to the ggplot style
plt.style.use("ggplot")

# Plot the data
plt.plot(x, t, "ro")
plt.xlabel("Year")
plt.ylabel("Winning time (s)")


# %% [markdown]
r"""
## Minimizing the loss

Recall that the mean squared error loss function was given by:

$$ \mathcal{L} = \frac{1}{N}\sum_{n=1}^N (t_n - w_0 - w_1x_n)^2 $$

We plot the loss function below.
"""


# %%
def mse_loss(w0, w1, x, t):
    """Compute the mean squared error loss."""
    return (np.sum(w1*x + w0 - t)**2)/len(x)

fig = plt.figure(figsize=(14,6))
ax = fig.add_subplot(1, 2, 1, projection="3d")
a = np.linspace(36, 37)
b = np.linspace(0.015, -0.05)
A, B = np.meshgrid(a, b)
zs = np.array([mse_loss(w0, w1, x, t) for w0, w1 in zip(np.ravel(A), np.ravel(B))])
loss_vals = zs.reshape(A.shape)

ax.plot_surface(A, B, loss_vals, cmap="viridis")
plt.xlabel("$w_0$")
plt.ylabel("$w_1$")
ax.set_zlabel("Loss")


# %% [markdown]
r"""
Note that the loss function curvature is more pronounced along the $w_1$ axis.

One way of defining the **best** model is that one that minimises this error
(i.e. the values of $w_0$ and $w_1$ that make $\mathcal{L}$ as small as
possible). That is, we want to find the lowest point on the surface above.

To find a minimum we will
1. differentiate the expression with respect to $w_0$ and $w_1$,
2. set the resulting equations to zero (since the gradient must be zero at the minimum) and then
3. solve for $w_0$ and $w_1$.

You will perform this procedure in worksheet 1, which we will start in class
and you will finish outside of class. But for this lab, we will use the end
result of the procedure.

The loss is minimised by:

$$ w_1 = \frac{\overline{xt} - \overline{x}\overline{t}}
{\overline{x^2} - (\overline{x})^2} $$

and

$$ w_0 = \overline{t} - w_1\overline{x} $$

where $\overline{z} = \frac{1}{N}\sum_{n=1}^N z_n$

We can now compute these quantites, first computing all the mean values we need:
"""

# %%
class SimpleLinearModel():
    """This is a simple linear model with 1-D inputs and two parameters."""

    def __init__(self):
        """Initialize the parameters to None"""
        self.w0: float = None
        self.w1: float = None

    def train(self, x, t):
        """Train the model using the least-squares method."""
        # Set the value of xbar to the mean of x, using the
        # mean() method for ndarrays
        # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.mean.html
        xbar = x.mean()

        # Set the value of tbar to the mean of t
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        tbar = t.mean()
        ### SOLUTION END ###

        # Set the value of xxbar (i.e., the mean of x^2).
        # To do this, we first perform elementwise multiplication using
        # numpy's `multiply` function
        # (https://numpy.org/doc/stable/reference/generated/numpy.multiply.html)
        # followed by taking the mean of the resulting array.
        xxbar = np.multiply(x, x).mean()

        # Similarly, set xtbar to the mean of xt
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        xtbar = np.multiply(x, t).mean()
        ### SOLUTION END ###

        # And now, use `xbar`, `tbar`, `xxbar`, and `xtbar` to set the values
        # of `self.w1` and `self.w0` to the values of $w_1$ and $w_0$.
        # respectively.
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        self.w1 = (xtbar - xbar*tbar)/(xxbar - xbar**2)
        self.w0 = tbar - self.w1*xbar
        ### SOLUTION END ###

    def predict(self, x):
        """Make a prediction with the model."""
        return self.w0 + self.w1 * x


model = SimpleLinearModel()
model.train(x, t)

# %% [markdown]
# ## Plotting
#
# Now that we have $w_0$ and $w_1$ we can plot the data.

# %%
x_test = np.linspace(1896, 2008, 100)

# f_test represents your learned model (in this case, a straight line)
f_test = model.predict(x_test)

# Let us plot the data and the learned model
plt.plot(x_test, f_test, "b-", linewidth=2)
plt.plot(x, t, "ro")
plt.xlabel("Olympic year")
plt.ylabel("Winning time (s)")


# %% [markdown]
# From visual inspection, it seems like a reasonably good model.
#
# ## Predictions
#
# We can now compute the prediction at 2012 by plugging in $x=2012$ into the model:


# %%
winning_time_2012 = model.predict(2012)
print(winning_time_2012)

# %% [markdown]
# So, we predict that the winning time will be $\approx$9.59 seconds. The
# actual winning time for 2012 was 9.63 seconds. Not bad!
