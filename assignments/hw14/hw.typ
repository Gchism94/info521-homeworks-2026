#import "../../common.typ": *
#import "../../equations.typ": expectation

#show: info521

#align(center)[
  #text(size: 14pt, fill: chili, smallcaps[Homework 14: Newton-Raphson Method])

  #course | #semester | Instructor: #instructor
]

= Newton-Raphson update rule for Poisson likelihood
<newton-raphson-update-rule-for-poisson-likelihood>
#emph[(Adapted from FCML Exercise 4.6)]

Assume that we observe $N$ vectors of attributes,
$upright(bold(x))_1 , . . . , upright(bold(x))_N$, and associated
integer counts $t_1 , . . . , t_N$. A Poisson likelihood would be
suitable:
$ p (t_n|upright(bold(x))_n , upright(bold(w))) = frac(f (upright(bold(x))_n ; upright(bold(w)))^(t_n) exp { - f (upright(bold(x))_n ; upright(bold(w))) }, t_n !) , $
where
$f (upright(bold(x))_n ; upright(bold(w))) = upright(bold(w))^tack.b upright(bold(x))_n$.
Assuming
$upright(bold(w)) tilde.op cal(N) (upright(bold(0)) , sigma^2 upright(bold(I))_D)$,
derive the parameter update rule for the Newton-Raphson procedure to
find the MAP estimate of $upright(bold(w))$.


#answer(
  [
    *Solution*:

The likelihood over all the observations is
$ p (upright(bold(t)) \| upright(bold(X)) , upright(bold(w))) = product_n^N p (t_n \| upright(bold(x))_n , upright(bold(w))) , $
and the full posterior is:
$ p (upright(bold(w)) \| upright(bold(t)) , upright(bold(X)) , sigma^2) = p (upright(bold(w)) \| sigma^2) product_n^N p (t_n \| upright(bold(x))_n , upright(bold(w))) . $

The log posterior is:
$ log p (upright(bold(w)) \| upright(bold(t)) , upright(bold(X)) , sigma^2) = log p (upright(bold(w)) \| sigma^2) + sum_n^N log p (t_n \| upright(bold(x))_n , upright(bold(w))) . $

The log of the likelihood term (for $n$) is:
$ log p (t_n \| upright(bold(x))_n , upright(bold(w))) & = & log {(t_n !)^(- 1) (upright(bold(w))^tack.b upright(bold(x))_n)^(t_n) exp { - upright(bold(w))^tack.b upright(bold(x))_n }}\
 & = & - log (t_n !) + t_n log (upright(bold(w))^tack.b upright(bold(x))_n) - upright(bold(w))^tack.b upright(bold(x))_n . $

The middle term is the most challenging for taking the partial
w.r.t.~$upright(bold(w))$. Note that
$upright(bold(w))^tack.b upright(bold(x))_n$ is a scalar. Let
$ G (upright(bold(w))) = t_n log (upright(bold(w))^tack.b upright(bold(x))_n) . $
Then, applying the derivative chain rule, where
$ frac(partial log f (x), partial x) = frac(1, f (x)) frac(partial f (x), partial x) = f (x)^(- 1) frac(partial f (x), partial x) med med med med upright(a n d) med med med med frac(partial (upright(bold(w))^tack.b upright(bold(x))_n), partial upright(bold(w))) = upright(bold(x))_n $
we get
$ frac(partial G, partial upright(bold(w))) = t_n (upright(bold(w))^tack.b upright(bold(x))_n)^(- 1) upright(bold(x))_n . $

The gradient of the likelihood (for datum $n$) is then
$ frac(partial p (t_n \| upright(bold(x))_n , upright(bold(w))), partial upright(bold(w))) = t_n (upright(bold(w))^tack.b upright(bold(x))_n)^(- 1) upright(bold(x))_n - upright(bold(x))_n , $
and the gradient of the likelihood across all of the data is
$ frac(partial p (upright(bold(t)) \| upright(bold(X)) , upright(bold(w))), partial upright(bold(w))) = sum_n^N t_n (upright(bold(w))^tack.b upright(bold(x))_n)^(- 1) upright(bold(x))_n - upright(bold(x))_n . $

Now to finding the gradient of the prior. The log of the zero-mean
Gaussian with diagonal constant $sigma^2$ covariance is
$ log p (upright(bold(w)) \| sigma^2) = - D / 2 log 2 pi - D log sigma - frac(1, 2 sigma^2) upright(bold(w))^tack.b upright(bold(w)) . $
So
$ frac(partial log p (upright(bold(w)) \| sigma^2), partial upright(bold(w))) = - 1 / sigma^2 upright(bold(w)) , $
and the gradient of the posterior across all of the data is:
$ frac(partial log p (upright(bold(w)) \| upright(bold(X)) , sigma^2), partial upright(bold(w))) = - 1 / sigma^2 upright(bold(w)) + sum_n^N t_n (upright(bold(w))^tack.b upright(bold(x))_n)^(- 1) upright(bold(x))_n - upright(bold(x))_n . $
This gives us the gradient that will be use for gradient ascent
updating.

Now to derive the Hessian to be used in Newton-Rhapson. Using
$ frac(partial (upright(bold(w))^tack.b upright(bold(x))_n), partial upright(bold(w))^tack.b) = upright(bold(x))_n^tack.b med med med med upright(a n d) med med med med frac(partial (- 1 / sigma^2 upright(bold(w))), partial upright(bold(w))^tack.b) = - 1 / sigma^2 upright(bold(I)) $
and again using the fact that
$upright(bold(w))^tack.b upright(bold(x))_n$ is a scalar, the Hessian
is:
$ frac(partial^2 p (upright(bold(w)) \| upright(bold(X)) , sigma^2), partial upright(bold(w)) partial upright(bold(w))^tack.b) = - 1 / sigma^2 upright(bold(I)) + sum_n^N - t_n (upright(bold(w))^tack.b upright(bold(x))_n)^(- 2) upright(bold(x))_n upright(bold(x))_n^tack.b $

Now, use the pieces derived above (the gradient and the Hessian) to
derive the update rules.

The gradient ascent update rule just flips the subtraction in the
Widrow-Hoff update to an addition, with step size $alpha$, to get:
$ upright(bold(w))^((i + 1)) & := upright(bold(w))^((i)) + alpha frac(partial
log p (upright(bold(w)) \| upright(bold(X)) , sigma^2), partial upright(bold(w))
partial upright(bold(w))^tack.b)\|_(upright(bold(w^((i)))))\
 & := upright(bold(w))^((i)) + alpha (- 1 / sigma^2 upright(bold(w))^((i)) +
 sum_n^N t_n (upright(bold(w))^((i) tack.b) upright(bold(x))_n)^(- 1)
 upright(bold(x))_n - upright(bold(x))_n) . $

The Newton-Raphson update is then,
$ upright(bold(w))^((i + 1)) & := upright(bold(w))^((i)) - (frac(partial^2 p
(upright(bold(w)) \| upright(bold(X)) , sigma^2), partial upright(bold(w))
partial upright(bold(w))^tack.b)\|_(upright(bold(w))^((i))))^(- 1) (frac(partial
log p (upright(bold(w)) \| upright(bold(X)) , sigma^2), partial
upright(bold(w)))\|_(upright(bold(w^((i))))))\
 & := upright(bold(w))^((i)) - (- 1 / sigma^2 upright(bold(I)) + sum_n^N - t_n
 (upright(bold(w))^((i) tack.b) upright(bold(x))_n)^(- 2) upright(bold(x))_n
 upright(bold(x))_n^tack.b)^(- 1) (- 1 / sigma^2 upright(bold(w))^((i)) +
 sum_n^N t_n (upright(bold(w))^((i) tack.b) upright(bold(x))_n)^(- 1)
 upright(bold(x))_n - upright(bold(x))_n) . $
Note that the difference from the previous $upright(bold(w))^((i))$
stays as a subtraction because Newton-Raphson is searching for local
minimum or maximum, where the first derivative is zero. In this case, it
happens to be a maximum.

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
