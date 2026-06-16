#import "../../common.typ": *
#import "../../equations.typ": expectation, jacobian, kdelta

#show: info521

#align(center)[
  #text(size: 14pt, fill: chili, smallcaps[Homework 7])
]

= Practice with Jacobians

+ Show that $ #jacobian([$bold(w)$], [w]) = bold(I)$, where $bold(I)$ is the
  identity matrix.

#answer(
  [
    In this homework solution, I use the compact derivative notation $dvcp(f,x)
    = dvp(f,x)$ in some places.

    $
      #jacobian([$bold(w)$], [w]) =
      mat(
        dvcp(w_1, w_1), dvcp(w_1, w_2), dots.c, dvcp(w_1, w_D);
        dvcp(w_2, w_1), dvcp(w_2, w_2), dots.c, dvcp(w_2, w_D);
        dots.v, dots.v, dots.down, dots.v;
        dvcp(w_D, w_1), dvcp(w_D, w_2), dots.c, dvcp(w_D, w_D);
      )
      = mat(
        1, 0, dots.c, 0;
        0, 1, dots.c, 0;
        dots.v, dots.v, dots.down, dots.v;
        0, 0, dots.c, 1
      )
      = bold(I)
    $

  ],
  []
)
+ Show that if $f(bold(w))$ is a scalar function, the following relation holds:
  $ dvp(, bold(w)^T) f(bold(w)) = (dvp(f(bold(w)), bold(w)))^T $

#answer(
  [
    $
    #jacobian($f(bold(w))$, [w]) =
    mat(
      dvcp(f, w_1),
      dots.c,
      dvcp(f, w_D)
    ) =
    mat(
      dvcp(f, w_1);
      dots.v;
      dvcp(f, w_D)
    )^T
     = (dvp(f, bold(w)))^T
    $

  ],
  []
)
+ Show that $ dvp(, bold(w)^T) bold(C) bold(w) = bold(C). $

#answer(
  [
    Let $dim(bold(C)) = N times D$ and $dim(bold(w)) = D times 1$. Then we can
    derive this result using explicit multiplication and using the Kronecker
    delta function's properties.

    $
    #jacobian($bold(C) bold(w)$, [w]) &=
    dvp(, bold(w)^T)
    mat(
      C_11, dots.c, C_(1D);
      dots.v, dots.down, dots.v;
      C_(N 1), dots.c, C_(N D);
    )
    mat(w_1; dots.v; w_D)\
    &=
    dvp(, bold(w)^T)
    mat(
      sum_d C_(1 d) w_d;
      dots.v;
      sum_d C_(N d) w_d
    )\
    &= mat(
      dvcp(sum_d C_(1 d) w_d, w_1), dots.c,  dvcp(sum_d C_(1 d) w_d, w_D);
      dots.v, dots.down, dots.v;
      dvcp(sum_d C_(N d) w_d, w_1), dots.c,  dvcp(sum_d C_(N d) w_d, w_D);
    )\
    &= mat(
      sum_d C_(1 d) dvcp(w_d, w_1), dots.c,  sum_d C_(1 d) dvcp(w_d, w_D);
      dots.v, dots.down, dots.v;
      sum_d C_(N d) dvcp(w_d, w_1), dots.c,  sum_d C_(N d) dvcp(w_d, w_D);
    )\
    &= mat(
      sum_d C_(1 d) kdelta(d, 1), dots.c,  sum_d C_(1 d) kdelta(d, D);
      dots.v, dots.down, dots.v;
      sum_d C_(N d) kdelta(d, 1), dots.c,  sum_d C_(N d) kdelta(d, D);
    )\
    &= mat(
      C_(1 1) , dots.c,  C_(1 D);
      dots.v, dots.down, dots.v;
      C_(N 1) , dots.c,  C_(N D);
    )\
    &= bold(C)
    $

  ],
  []
)

We will use the first two relations when we derive the Newton-Raphson update
rule for Bayesian logistic regression with a Gaussian prior (#fcml $section$ 4).
The third relation was used in class when we computed the Hessian of the
log-likelihood for the linear model with Gaussian additive noise.

= Workload
<workload>
How many hours did you spend on this homework assignment?

#heading(level: 1, numbering: none)[Acknowledgments]
<acknowledgments>

Cite all the people you've worked with on this homework, as well as any other
resources you used apart from the course textbooks. If you used generative AI
tools (e.g., ChatGPT), please describe how you used them.

If you did not work with anyone else or use generative AI tools, please say so.
