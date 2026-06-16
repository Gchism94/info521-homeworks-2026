# %% [markdown]
r"""
# Bayesian logistic regression: MAP estimation

Adarsh Pyarelal

(Adapted from notebook originally developed by Simon Rogers)
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
fig, axes = plt.subplots()

# Plot class 0
pos = np.where(t==0)[0]
axes.plot(X[pos,0],X[pos,1],'ko')

# Plot class 1
pos = np.where(t==1)[0]
axes.plot(X[pos,0],X[pos,1],'ks', markerfacecolor="none")

axes.set_xlabel("$x_1$")
axes.set_ylabel("$x_2$")

# %% [markdown]
# Set the parameter $\sigma^2$ (the variance of the prior in our example).

# %%
sig_sq = 10


# %% [markdown]
# First, implement the logistic function:
#
# $$\text{Logistic}(x) = \frac{1}{1 + e^{-x}}$$.
#
# Use the `exp` function from `numpy` to make sure the function is vectorized.

# %%
def logistic(x):
    # Implement the logistic function.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return 1/(1.0+np.exp(-x))
    ### SOLUTION END ###


# %% [markdown]
# Next, implement the computation of the gradient:
#
# $$\frac{\partial\log g(\mathbf{w}; \mathbf{X},
# \mathbf{t})}{\partial\mathbf{w}} = -\frac{1}{\sigma^2}\mathbf{w} +
# \sum_{n=1}^{N}\mathbf{x_n}(t_n - P_n)$$

# %%
def gradient(w, X, t, sig_sq):
    # Compute a N x 1 vector of probabilities containing all your P_n values.
    # Name this vector `p`.
    # Hint: this computation involves:
    # 1. constructing an expression out of X and w,
    # 2. passing that expression into the logistic function you implemented above,
    # 3. then flattening the resulting array using NumPy's `flatten` method.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    p = logistic(X @ w).flatten()
    ### SOLUTION END ###
    return -w/sig_sq + X.T @ (t - p)


# %% [markdown]
# Next, compute the Hessian (FCML equation 4.10)

# %%
def hessian(w, X, sig_sq):
    # Compute the vector of probabilities p using X and w,
    # like you did in the gradient function earlier.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    p = logistic(X @ w).flatten()
    ### SOLUTION END ###
    W = np.diag((p*(1-p)))
    return -(1.0/sig_sq)*np.eye(len(w)) - X.T @ W @ X


# %% [markdown]
# Now, let us plot training loss and validation loss as a function of
# polynomial order.

# %%
w = np.zeros(2) # Initial guess

all_w = []
all_w.append(w.flatten())
for it in range(10):
    w = w - np.linalg.inv(hessian(w,X,sig_sq)) @ gradient(w,X,t,sig_sq)
    all_w.append(w.flatten())

# %% [markdown]
# Plot the evolution of $w_1$ and $w_2$ versus iterations. The plot should look
# similar to FCML Figure 4.3.

# %%
fig, axes = plt.subplots()
all_w = np.array(all_w)
for i in range(2):
    axes.plot(all_w[:,i], label=f"$w_{i}$")
axes.legend()
axes.set_xlabel("Iteration")
axes.set_ylabel("$w_i$")

# %% [markdown]
# Plot the probability contours with the data. Your plot should look like
# Figure 4.4(b) from FCML.

# %%
gridX,gridY = np.meshgrid(np.arange(-5,4,0.1),np.arange(-5,5,0.1))

# %%
P = np.zeros_like(gridX,dtype=np.float32)
for i,row in enumerate(gridX):
    for j,val in enumerate(row):
        pos_vec = np.vstack((val,gridY[i,j]))
        P[i][j] = logistic(w @ pos_vec).squeeze()

fig, axes = plt.subplots()

# Plot class 0
pos = np.where(t==0)[0]
axes.plot(X[pos,0],X[pos,1],'ko')

# Plot class 1
pos = np.where(t==1)[0]
axes.plot(X[pos,0],X[pos,1],'ks', markerfacecolor="none")

CS = axes.contour(gridX,gridY,P, levels=np.arange(0.1, 1, 0.1))
axes.clabel(CS, CS.levels, inline=True)
axes.set_xlim((-5,4))
axes.set_ylim((-5,5))

# %%
