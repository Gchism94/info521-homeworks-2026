#import "../../common.typ": *
#import "../../equations.typ": expectation

#show: info521

#align(center)[

  #text(size: 14pt, fill: chili, smallcaps[Homework 8])
]

= Gaussian manipulation
<gaussian-manipulation>
#emph[(Adapted from FCML Ex. 2.5)]

Assume that $p (upright(bold(w)))$ is the Gaussian (Normal) distribution
for a $D$-dimensional vector $upright(bold(w))$ given by

$ p (upright(bold(w))) = frac(1, (2 pi)^(D \/ 2) lr(|bold(Sigma)|)^(1 \/ 2)) exp {- 1 / 2 (upright(bold(w)) - bold(mu))^tack.b bold(Sigma)^(- 1) (upright(bold(w)) - bold(mu))} . $
<multnormal>

Suppose we use a diagonal covariance matrix with different elements on
the diagonal, i.e.,

$ bold(Sigma) = mat(delim: "[", sigma_1^2, 0, dots.h.c, 0; 0, sigma_2^2, dots.h.c, 0; dots.v, dots.v, dots.down, dots.v; 0, 0, dots.h.c, sigma_D^2) $

Show that this implies independence of the $D$ elements of
$upright(bold(w))$—that is, show that it is equivalent to the product of
$D$ univariate Gaussians with variances
$sigma_1^2 , dots.h , sigma_D^2$. You can do this by expanding the
vector notation of Eq 1 and re-arranging. You will need
to be aware that the determinant of a matrix that only has entries on
the diagonal is the product of the diagonal values and that the inverse
of such a matrix is constructed by simply inverting each element on the
diagonal. #emph[Hint: a product of exponentials can be expressed as an
exponential of a sum.]

#answer([
  == Solution
  <solution>
  The inverse of the covariance matrix, $bold(Sigma)^(- 1)$, is given by:

  $ bold(Sigma)^(- 1) = mat(delim: "[", 1 / sigma_1^2, 0, dots.h.c, 0; 0, 1 / sigma_2^2, dots.h.c, 0; dots.v, dots.v, dots.down, dots.v; 0, 0, dots.h.c, 1 / sigma_D^2) $
  This can be written more compactly as
  $"diag" (1 / sigma_1^2 , . . . , 1 / sigma_D^2)$. Also,
  $lr(|bold(Sigma)|) = product_(d = 1)^D sigma_d^2$. Plugging both of
  these into the multivariate Gaussian and manipulating, we get:

  $ p (upright(bold(w))) & = frac(1, (2 pi)^(D \/ 2) (product_(d = 1)^D sigma_d^2)^(1 \/ 2)) exp {- 1 / 2 (upright(bold(w)) - bold(mu))^tack.b "diag" (1 / sigma_1^2 , . . . , 1 / sigma_D^2) (upright(bold(w)) - bold(mu))}\
  & = product_(d = 1)^D [1 / sqrt(2 pi sigma_d^2)] exp {- sum_(d = 1)^D frac((x_d - mu_d)^2, 2 sigma_d^2)}\
  & = product_(d = 1)^D [1 / sqrt(2 pi sigma_d^2)] product_(d = 1)^D exp {- frac((x_d - mu_d)^2, 2 sigma_d^2)}\
  & = product_(d = 1)^D [1 / sqrt(2 pi sigma_d^2)] exp {- frac((x_d - mu_d)^2, 2 sigma_d^2)} $
  This is another product of univariate Gaussian pdfs; this time, however,
  each random variable has a (potentially) different variance.
  ],
  []
)

= Showing that an MLE is unbiased

Show that the maximum likelihood estimator (MLE) that you derived in HW5 is unbiased.

#answer(
  [
    *Solution:* Let us denote by $bold(x)$ the vector random variable such that $bold(x)
    = vec(x_1, x_2, dots.v, x_N)$.

    $hat(r)$ is unbiased if $expectation(hat(r), P(bold(x)|r)) = r$.
    $
      expectation(hat(r), P({x_i}|r)) &= expectation(frac(sum_i x_i, N), P(bold(x)|r)) \
                                &= frac(1, N) expectation(sum_i x_i, P(bold(x)|r)) \
                                &= frac(1, N) sum_i expectation(x_i, P(bold(x)|r)) \
                                &= frac(1, N) sum_i sum_bold(x) x_i P(bold(x)|r) \
                                &= frac(1, N) sum_i sum_(x_i) sum_({x_j|j != i}) x_i P(bold(x)|r) \
                                &= frac(1, N) sum_i sum_(x_i) x_i sum_({x_j|j != i}) P(bold(x)|r) \
                                &= frac(1, N) sum_i sum_(x_i) x_i P(x_i|r) \
                                &= frac(1, N) sum_i expectation(x_i, P(x_i|r)) \
                                &= frac(1, N) sum_i r \
                                &= frac(1, N) N r \
                                &= r
    $

    Thus, $hat(r)$ is an unbiased estimator.

    A more concise proof is shown below which relies on the linearity of
    expectations.

    $
      expectation(hat(r), "") &= expectation(frac(sum_i x_i, N),"") \
                                &= frac(1, N) expectation(sum_i x_i, "") \
                                &= frac(1, N) sum_i expectation(x_i, "") \
                                &= frac(1, N) sum_i r \
                                &= frac(1, N) N r \
                                &= r
    $


  ], []
)

= Expected value of Beta density parameter
#emph[(FCML Exercise 3.5)]

Consider a random variable with a Beta density (see FCML $section$ 2.5.2 or PML1 $section$ 2.7.4):

$ p(r) = frac(Gamma(alpha + beta), Gamma(alpha)Gamma(beta)) r^(alpha - 1) (1 - r)^(beta - 1) $

Derive an expression for $#expectation([r], [p(r)])$. You will need the following identity for the gamma function:

$ Gamma(n + 1) = n Gamma(n) $

Hint: Use the fact that

$ integral_(r = 0)^(r = 1) r^(alpha - 1) (1 - r)^(beta - 1) "dr" =
frac(Gamma(alpha)Gamma(beta), Gamma(alpha + beta)) $

#answer(
  [
#strong[Solution]
$ upright(bold(E))_(p (r)) {r} & = integral_0^1 frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) r^(alpha - 1) (1 - r)^(beta - 1) r thin d r\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) integral_0^1 r^((alpha + 1) - 1) (1 - r)^(beta - 1) thin d r\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) frac(Gamma (alpha + 1) Gamma (beta), Gamma (alpha + beta + 1))\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) frac(alpha Gamma (alpha) Gamma (beta), (alpha + beta) Gamma (alpha + beta))\
 & = frac(alpha, alpha + beta) $
  ],
  []
)

= Variance of Beta density parameter
#emph[(FCML Exercise 3.6)]

Using the setup in the previous exercise, and the identity

$ "var"{r} = #expectation([$r^2$], [p(r)]) - (#expectation([r], [p(r)]))^2, $

derive an expression for $"var"{r}$. You will need the gamma identity given in the previous exercise.

#answer(
  [
#strong[Solution]
$ upright(bold(E))_(p (r)) {r^2} & = integral_0^1 frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) r^(alpha - 1) (1 - r)^(beta - 1) r^2 thin d r\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) integral_0^1 r^((alpha + 2) - 1) (1 - r)^(beta - 1) thin d r\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) frac(Gamma (alpha + 2) Gamma (beta), Gamma (alpha + beta + 2))\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) frac((alpha + 1) Gamma (alpha + 1) Gamma (beta), (alpha + beta + 1) Gamma (alpha + beta + 1))\
 & = frac(Gamma (alpha + beta), Gamma (alpha) Gamma (beta)) frac((alpha + 1) alpha Gamma (alpha) Gamma (beta), (alpha + beta + 1) (alpha + beta) Gamma (alpha + beta))\
 & = frac(alpha (alpha + 1), (alpha + beta) (alpha + beta + 1)) $ From
Exercise 3.5, we derived that
$ upright(bold(E))_(p (r)) {r} = frac(alpha, alpha + beta) $ So
$ mono("var") (r) & = upright(bold(E))_(p (r)) {r^2} - (upright(bold(E))_(p (r)) {r})^2\
 & = frac(alpha (alpha + 1), (alpha + beta) (alpha + beta + 1)) - (frac(alpha, alpha + beta))^2\
 & = frac(alpha beta, (alpha + beta)^2 (alpha + beta + 1)) $
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
