# %% [markdown]
# # Monte Carlo approximation for expectations
#
# In the written part of this homework, you analytically computed the following expression:
#
# $$\mathbf{E}_{p(x)}\{35 + 3x - 3x^2 + 0.2x^3 + 0.01x^4\}$$
#
# where $p(x) = \mathcal{U}(-1, 9)$.
#
# Now, you will compute a sample-based approximation to this integral (see FCML Equation 2.23)
#
#

# %% [markdown]
# Perform the necessary imports:

# %%
import numpy as np
from matplotlib import pyplot as plt
# %config InlineBackend.figure_format = "retina"

# %% [markdown]
# Then, define the function `f` such that
#
# $$f(x) = 35 + 3x - 3x^2 + 0.2x^3 + 0.01x^4$$

# %%
def f(x):
    ...
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return 35 + 3*x - 3*(x**2) + 0.2*(x**3) + 0.01*(x**4)
    ### SOLUTION END ###


# %%
# Set the random seed to 100 (you learned how to do this in HW3).

### YOUR CODE HERE ###
### SOLUTION START ###
rng = np.random.default_rng(100)
### SOLUTION END ###

# %%
# Next, sample 1000 values from U(-1, 9) using the Numpy
# `numpy.random.Generator.uniform` function
# (https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html)
# Store the array of values in a variable called `xs`.
### YOUR CODE HERE ###
### SOLUTION START ###
xs = rng.uniform(low=-1, high=9, size=1000)
### SOLUTION END ###

# Construct an array of values corresponding to applying the function `f`
# to each of the values in `xs`. Store the resulting array in variable
# called `vals`. Remember that Python is dynamically typed and
# NumPy operations are vectorized, so you should be able to do this with
# just one line of code (do not use explicit looping here!)

### YOUR CODE HERE ###
### SOLUTION START ###
vals = f(xs)
### SOLUTION END ###

# Create an array to store the sizes of the subsets of samples
sample_subset_sizes = np.arange(1, xs.shape[0], 10)

# Create an array to store expectations
expectations = np.zeros((sample_subset_sizes.shape[0]))

# The following loop computes approximate expectations for each of the different
# sample subset sizes in `sample_subset_sizes`, and stores them in the array
# `expectations`.
for i in range(sample_subset_sizes.shape[0]):
    expectations[i] = vals[0:sample_subset_sizes[i]].mean()

# Print the approximate expectation computed using all 1000 samples.
print("Approximate expectation using 1000 samples: ", expectations[-1])

# %%
plt.plot(sample_subset_sizes, expectations)

# The true, analytic result of the expected value
# Create a variable named `true_expectation` and set it equal to the value that
# you computed in the written portion of the homework.
### YOUR CODE HERE ###
### SOLUTION START ###
true_expectation = 18.61
### SOLUTION END ###

# Plot the approximate expectations
plt.plot(
    np.array([sample_subset_sizes[0], sample_subset_sizes[-1]]),
    # Plot the analytic expected result as a red line:
    np.array([true_expectation, true_expectation]), color='r'
)
plt.xlabel('Sample size')
plt.ylabel('Approximate expectation')
plt.title('Evolution of expectation of $f(x)$')
plt.savefig("sample_based_approximation.pdf")
