#import "../../common.typ": *
#import "../../equations.typ": expectation

#show: info521

#align(center)[
  #text(size: 14pt, fill: chili, smallcaps[Homework 15: Laplace Approximation])

  #course | #semester | Instructor: #instructor
]


= Laplace approximation for beta prior and binomial likelihood
<laplace-approximation-for-beta-prior-and-binomial-likelihood>
_(Adapted from FCML Exercise 4.2)_

In Chapter 3, we computed the posterior density over $r$, the probability of a
coin giving heads, using a beta prior and a binomial likelihood. Compute the
Laplace approximation to the posterior for this prior-likelihood combination.
Note that you should be able to obtain a closed-form solution for the MAP value of
$r$ by analytically optimizing the posterior.


#answer([
#strong[Solution.] To form the Laplace approximation, we need to
determine both the mean, $hat(mu)$, and variance, $hat(sigma^2)$
(1-dimensional, in this case) parameters of the Gaussian that will be
used as the approximation to the posterior.

The first step, identifying the mean, $hat(mu)$, involves finding the
mode of the posterior. We already know the $upright(B e t a)$
distribution is a conjugate prior to the $r$ parameter of the binomial
likelihood, so we can calculate the mode analytically.

Recall that the product of the binomial likelihood and prior beta
density can be put in the form of a posterior $upright(B e t a)$ density
$ p (y|r , N) p (r|alpha , beta) &= binom(y, N) r^y (1 - r)^(N - y) times frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) r^(alpha - 1) (1 - r)^(beta - 1)\
 &= binom(y, N) frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) r^(y + alpha - 1) (1 - r)^(N - y + beta - 1)\
 & prop & r^(y + alpha - 1) (1 - r)^(N - y + beta - 1) $ With
$gamma = y + alpha$ and $delta = N - y + beta$, the resulting posterior
beta distribution is
$ p (y|gamma , delta) = frac(Gamma (gamma + delta), Gamma (gamma) Gamma (delta)) r^(gamma - 1) (1 - r)^(delta - 1) $
It will be more convenient to work with the log posterior
$ log (p (y|gamma , delta)) = log (frac(Gamma (gamma + delta), Gamma (gamma) Gamma (delta))) + (gamma - 1) log (r) + (delta - 1) log (1 - r) $
We can now take the first partial derivative with respect to $r$ (we’ll
use this result again below):

$ frac(partial log (p (y|gamma , delta)), partial r) & = frac(gamma - 1, r) + frac(delta - 1, 1 - r) frac(partial (1 - r), partial r)\
 & = frac(gamma - 1, r) - frac(delta - 1, 1 - r) , $
<eqn:firstderiv>

set it to $0$, and
solve for $r$ $ frac(gamma - 1, r) - frac(delta - 1, 1 - r) &= 0\
frac(gamma - 1, r) &= frac(delta - 1, 1 - r)\
gamma - 1 &= frac(r (delta - 1), 1 - r)\
(gamma - 1) (1 - r) &= r (delta - 1)\
gamma - 1 + r - r gamma &= r delta - r\
gamma - 1 &= r delta + r gamma - 2 r\
gamma - 1 &= r (delta + gamma - 2)\
frac(gamma - 1, delta + gamma - 2) &= r med . $ This value, $hat(r)$,
is the mode of the posterior, and will be used as our estimate of the
mean, $hat(mu)$ of the Gaussian Laplace estimator:
$ hat(mu) = hat(r) = frac(gamma - 1, delta + gamma - 2) $ where
$gamma = y + alpha$ and $delta = N - y + beta$.

The next step is to calculate the variance, $1 / nu$, where
$ nu = - frac(partial^2 log p (r|y , N , alpha , beta), partial r^2)\|_(hat(r)) $
The first partial derivative of the log-posterior was already derived
above in Equation~@eqn:firstderiv; the second partial derivative with
respect to $r$ is given by
$ frac(partial^2 log p (r|y , N , alpha , beta), partial r^2) &= frac(partial log p (r|dot.op), partial r) (frac(gamma - 1, r) - frac(delta - 1, 1 - r))\
 &= (- 1) frac(gamma - 1, r^2) - (- 1) frac(delta - 1, (1 - r)^2) frac(partial (1 - r), partial r)\
 &= - frac(gamma - 1, r^2) - (- 1) frac(delta - 1, (1 - r)^2) (- 1)\
 &= - frac(gamma - 1, r^2) - frac(delta - 1, (1 - r)^2) med . $ We
can then express $nu$ in terms of $hat(r)$:
$ nu &= - (- frac(gamma - 1, hat(r)^2) - frac(delta - 1, (1 - hat(r))^2))\
 &= (gamma - 1) (gamma + delta - 2)^2 / (gamma - 1)^2 + (delta - 1) (1 - frac(gamma - 1, gamma + delta - 2))^(- 2)\
 &= frac((gamma + delta - 2)^2, gamma - 1) + (delta - 1) (frac(gamma + delta - 2, gamma + delta - 2) - frac(gamma - 1, gamma + delta - 2))^(- 2)\
 &= frac((gamma + delta - 2)^2, gamma - 1) + (delta - 1) (frac(delta - 1, gamma + delta - 2))^(- 2)\
 &= frac((gamma + delta - 2)^2, gamma - 1) + (delta - 1) (gamma + delta - 2)^2 / (delta - 1)^2\
 &= frac((gamma + delta - 2)^2, gamma - 1) + frac((gamma + delta - 2)^2, delta - 1)\
 &= frac((delta - 1) (gamma + delta - 2)^2 + (gamma - 1) (gamma + delta - 2)^2, (gamma - 1) (delta - 1))\
 &= frac((delta + gamma - 2) (gamma + delta - 2)^2, (gamma - 1) (delta - 1))\
 &= frac((gamma + delta - 2)^3, (gamma - 1) (delta - 1)) $ Finally,
we can re-express $nu$ in terms of $alpha$, $beta$, $N$ and $y$ by
substituting in the terms for $gamma$ and $delta$:
$ nu = frac((alpha + beta + N - 2)^3, (y + alpha - 1) (N - y + beta - 1)) $
From this, we conclude that we can approximate the posterior
$upright(B e t a)$ distribution with a normal of the form
$cal(N) (hat(r) , 1 / nu)$

—–

An alternate form that I see a lot of: Rather than expressing the
posterior in the re-parameterized form, instead multiply the likelihood
and prior, keeping the original parameters, then take the derivatives.
This results in the following:

$ g (r|alpha , beta) &= binom(N, y) r^y (1 - r)^(N - y) frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) r^(alpha - 1) (1 - r)^(beta - 1)\
log (g (r|alpha , beta)) &= . . . + y log r + (N - y) log (1 - r) + . . . + (alpha - 1) log r + (beta - 1) log (1 - r) $

$ frac(partial log g (r|y , N , alpha , beta), partial r) &= y / r - frac(N - y, 1 - r) + frac(alpha - 1, r) - frac(beta - 1, 1 - r)\
 &= frac(y + alpha - 1, r) + frac(- N + y - beta + 1, 1 - r) $
Setting $frac(partial log g (r|y , N , alpha , beta), partial r) = 0$
and solving for $r$:
$ r &= frac(1 - y - alpha, 2 - N - alpha - beta) $ Taking the second
derivative w.r.t. r is:
$ frac(partial^2 log g (r|y , N , alpha , beta), partial r^2) &= (- 1) (y + alpha - 1) r^(- 2) + (- 1) (- N + y - beta + 1) (1 - r)^(- 2) (- 1)\
 &= frac(- y - alpha + 1, r^2) + frac(- N + y - beta + 1, (1 - r)^2)\
 &= frac((- y - alpha + 1) (1 - r)^2 + (- N + y - beta + 1) r^2, r^2 (1 - r)^2) $
 ],
 []
 )


= Workload
<workload>
How many hours did you spend on this homework assignment?

#heading(level: 1, numbering: none)[Acknowledgments]
<acknowledgments>

Cite all the people you've worked with on this homework, as well as any other
resources you used apart from the FCML textbook. If you used generative AI
tools (e.g., ChatGPT), please describe how you used them.

If you did not work with anyone else or use generative AI tools, please say so.
