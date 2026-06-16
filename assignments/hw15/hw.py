# %% [markdown]
r"""
# Laplace approximation

Adarsh Pyarelal

(Adapted from notebook originally developed by Simon Rogers)

In this notebook, you will implement the Laplace approximation for Bayesian logistic regression.
"""

# %% [markdown]
# Import numpy, matplotlib, set up plot style:

# %%
import numpy as np
from matplotlib import pyplot as plt
# %matplotlib inline
# %config InlineBackend.figure_format = "retina"


# %% [markdown]
# Load the data (this is the same data used in the binary classification
# example in FCML Chapter 4). The variables `X` and `t` below correspond to
# $\mathbf{X}$ and $\mathbf{t}$ in FCML equation 4.6.

# %%
X = np.loadtxt("data/X.csv", delimiter=",")
t = np.loadtxt("data/t.csv")


# %% [markdown]
# Plot the data. Your plot should look similar to FCML Figure 4.1

# %%
def plot_data():
    fig, axes = plt.subplots(figsize=(5,4))

    # Plot class 0
    pos = np.where(t==0)[0]
    axes.plot(X[pos,0],X[pos,1],'ko')

    # Plot class 1
    pos = np.where(t==1)[0]
    axes.plot(X[pos,0],X[pos,1],'ks', markerfacecolor="none")

    axes.set_xlabel("$x_1$")
    axes.set_ylabel("$x_2$")

    axes.set_xlim([-5,5])
    axes.set_ylim([-5,5])
    plt.tight_layout()
    return fig, axes

plot_data()

# %% [markdown]
# Use the Newton-Raphson procedure to obtain $\widehat{\mathbf{w}}_\text{MAP}$,
# using the same prior, likelihood, $\sigma^2$, starting value for $\mathbf{w}$
# (i.e., $\mathbf{w} = \mathbf{0}$), and number of iterations as in HW14. *Hint:
# reuse your code from HW14!*
#
# Use the variable name `w_MAP` for the value of $\widehat{\mathbf{w}}_\text{MAP}$ you obtain.

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
sig_sq = 10

def logistic(x):
    return 1/(1.0+np.exp(-x))

def gradient(w, X, t, sig_sq):
    p = logistic(X @ w).flatten()
    return -w/sig_sq + X.T @ (t - p)

def hessian(w, X, sig_sq):
    p = logistic(X @ w).flatten()
    W = np.diag((p*(1-p)))
    return -(1.0/sig_sq)*np.eye(len(w)) - X.T @ W @ X

w_MAP = np.zeros(2) # Initial guess
all_w = []
all_w.append(w_MAP.flatten())
for it in range(10):
    w_MAP = w_MAP - np.linalg.inv(hessian(w_MAP,X,sig_sq)) @ gradient(w_MAP,X,t,sig_sq)
    all_w.append(w_MAP.flatten())
### SOLUTION END ###

# %% [markdown]
# Sample 20 values of $\mathbf{w}$ from a multivariate normal with mean $\widehat{\mathbf{w}}_\text{MAP}$
# and covariance equal to the inverse of the negative Hessian of $\log g$. You can use Numpy's [`numpy.random.multivarate_normal`](https://numpy.org/doc/2.0/reference/random/generated/numpy.random.multivariate_normal.html#) function for this.
#
# Use the variable name `w_samples` for the array containing the samples, and
# `g_cov` for the covariance matrix..

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
H = hessian(w_MAP,X,sig_sq)
g_cov = np.linalg.inv(-H)
print(g_cov)
w_samples = np.random.multivariate_normal(w_MAP,g_cov,20)
### SOLUTION END ###

# %% [markdown]
# Plot the decision boundaries corresponding to these 20 samples. Your plot
# should look similar to (but may not be identical to) FCML Figure 4.7(a).

# %%
fig, axes = plot_data()

for w_sample in w_samples:
#   Plot the line corresponding to w.Tx = 0
    x = np.array([-5,5])
    y = (-w_sample[1]/w_sample[0])*x
    axes.plot(x,y, color='k', linewidth=0.5)


# %% [markdown]
# Plot the probability contours with the data. Your plot should look like
# FCML Figure 4.7(b).

# %%
gridX,gridY = np.meshgrid(np.arange(-5,5,0.1),np.arange(-5,5,0.1))

# %% [markdown]
# Now, sample 1000 samples from the Laplace approximation (instead of the 20 you did earlier).
# Use the same variable name (`w_samples`) for the array containing the 1000 samples.

# %%
### YOUR CODE HERE ###
### SOLUTION START ###
w_samples = np.random.multivariate_normal(w_MAP, g_cov, 100000)
### SOLUTION END ###
n_rows, n_cols = gridX.shape

gx = np.reshape(gridX,(n_rows*n_cols,1))
gy = np.reshape(gridY,(n_rows*n_cols,1))

g = np.hstack((gx,gy))

# Compute expected probabilities using the samples (FCML Equation 4.15)
# Compute probability for each sample, then take the mean of the probabilities
P = logistic(g @ w_samples.T).mean(axis = 1)
P = np.reshape(P,(n_rows,n_cols))

fig, axes = plot_data()

CS = axes.contour(
        gridX,
        gridY,
        P,
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        colors='k',
        linewidths=0.5
        )
axes.clabel(CS, CS.levels, inline=True)
axes.set_xlim((-5,4))

# %%
