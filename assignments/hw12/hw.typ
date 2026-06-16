#import "../../common.typ": *
#import "../../equations.typ": expectation

#show: info521

#align(center)[

  #text(size: 14pt, fill: chili, smallcaps[Homework 12])
]

= Prior on noise variance $sigma^2$

#emph[(FCML Exercise 3.12)]

When performing a Bayesian analysis of the Olympics data, we assumed
that $sigma^2$ was known. If instead we assume that $upright(bold(w))$
is known and an Inverse Gamma prior is placed on $sigma^2$,

$ p (sigma^2|alpha , beta) = frac(beta^alpha, Gamma (alpha)) (sigma^2)^(- alpha - 1) exp {- beta / sigma^2} , $

then the posterior over $sigma^2$ will also be Inverse Gamma. Derive the
parameters for the posterior belief in the variance.

#answer(
  [
#strong[Solution.] Since, in this case, the prior and the likelihood are
conjugate and therefore the posterior will be Inverse Gamma, the goal is
to find the corresponding posterior parameters of the Inverse Gamma
distribution that play the corresponding roles of $alpha$ and $beta$ in
the prior distribution. We’ll denote the posterior parameters as
$alpha'$ and $beta'$.
$ p (sigma^2 | alpha', beta') = frac((beta')^(alpha'), Gamma (alpha')) (sigma^2)^(- alpha' - 1) exp {- beta' / sigma^2} , $

The product of the likelihood and prior is

#text(size:10pt)[
$ p (sigma^2|upright(bold(t)) , upright(bold(w)), upright(bold(X))) &prop 
p(upright(bold(t))|sigma^2 , upright(bold(w)) , upright(bold(X))) 
times p (sigma^2 \| alpha , beta)\
&= frac(1, (2 pi)^(D \/ 2) lr(|sigma^2 upright(bold(I))|)^(1 \/ 2)) exp {-
frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b
(upright(bold(t)) - upright(bold(X)) upright(bold(w)))} times frac(beta^alpha,
Gamma (alpha)) (sigma^2)^(- alpha - 1) exp {- beta / sigma^2} , $
]

where $upright(bold(I))$ is a $D times D$ identity matrix ($D$ is 
the number of training data points; it’s important to keep track
of the dimensions!). The next step is to get the above expression into
an Inverse Gamma form. All terms that are not a function of $sigma$ can
be treated as constants – in this case, this includes these two terms:
$ 1 / (2 pi)^(D \/ 2) med med upright("and") med med frac(beta^alpha, Gamma (alpha)) $

The resulting simplified product is then the following, which we can
rearrange to group like terms:
$ p (sigma^2 \| upright(bold(t)) , upright(bold(w)) , upright(bold(X))) & prop & 1 / lr(|sigma^2 upright(bold(I))|)^(1 \/ 2) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} (sigma^2)^(- alpha - 1) exp {- beta / sigma^2}\
 & prop & lr(|sigma^2 upright(bold(I))|)^(- 1 \/ 2) (sigma^2)^(- alpha - 1) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2} $

Now, our goal is to get this to match the simplified form of the
posterior Inverse Gamma (ignoring the terms that don’t involve $sigma$):

$ (sigma^2)^(- alpha' - 1) exp {- beta' / sigma^2} $
<eqn:simpgamma>

The scalar
product of $sigma^2$ with the $D$-dimensional identity matrix,
$upright(bold(I))$, is a diagonal matrix with $sigma^2$ for each of the
diagonal terms. The determinant of a diagonal matrix is the product of
all of the terms on the diagonal, so
$lr(|sigma^2 upright(bold(I))|) = product^D sigma^2 = sigma^(2 D)$. This
gives us:
$ p (sigma^2 \| upright(bold(t)) , upright(bold(w)) , upright(bold(X))) & prop sigma^((2 D) (- 1 \/ 2)) (sigma^2)^(- alpha - 1) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2}\
 & = sigma^(- D) (sigma^2)^(- alpha - 1) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2}\
 & = sigma^(- D) sigma^(- 2 alpha - 2) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2}\
 & = sigma^(- 2 alpha - D - 2) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2}\
 & = (sigma^2)^(- alpha - D \/ 2 - 1) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2}\
 & = (sigma^2)^(- (alpha + D \/ 2) - 1) exp {- frac(1, 2 sigma^2) (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))} exp {- beta / sigma^2} $

This gives us the form for the left term involving $alpha$ in
Equation~@eqn:simpgamma. Next we combine the two exponential terms on
the right:

$ p (sigma^2 \| upright(bold(t)) , upright(bold(w)) , upright(bold(X))) & prop & (sigma^2)^(- (alpha - D \/ 2) - 1) exp {- frac((1 / 2 (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))) + beta, sigma^2)} . $
<eqn:posteriorIG>

From this, we now also have the form of $beta$ in
Equation~@eqn:simpgamma. So the parameters for the posterior Inverse
Gamma distribution, $upright(I G) (alpha' , beta')$, are

$ alpha' & = alpha + D / 2 ,\
beta' & = (1 / 2 (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))) + beta . $

Equation~@eqn:posteriorIG is the full posterior parameterized in terms
of the prior and data. We can also write this as,
$ sigma^2 \| upright(bold(t)) , upright(bold(w)) , upright(bold(X)) med tilde.op med upright(I G) (alpha + D / 2 , (1 / 2 (upright(bold(t)) - upright(bold(X)) upright(bold(w)))^tack.b (upright(bold(t)) - upright(bold(X)) upright(bold(w)))) + beta) . $
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
