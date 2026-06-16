#import "../../common.typ": *

#show: info521

#align(center)[

  #text(size: 14pt, fill: chili, smallcaps[Homework 2])
]

= Deriving matrix calculus identities
<deriving-matrix-calculus-identities>

Derive the identities in @tab:matrix_calc_identities assuming
$upright(bold(C))$ is symmetric.

#figure(
  align(center)[#table(
    columns: 2,
    stroke: none,
    align: (center,center,),
    table.hline(),
    table.header([$f (upright(bold(w)))$], [$gradient f$],),
    table.hline(stroke: 0.5pt),
    [$bold(w)^T bold(x)$], [$bold(x)$],
    [$bold(x)^T bold(w)$], [$bold(x)$],
    [$bold(w)^T bold(w)$], [$2bold(w)$],
    [$bold(w)^T bold(C)bold(w)$], [$2bold(C)bold(w)$],
    table.hline()
  )]
  , kind: table,
    caption: [Identites from FCML Table 1.4.]
  )
<tab:matrix_calc_identities>

There are multiple ways to derive these---two of them are described below.

== Explicit multiplication
<explicit-multiplication>
One approach is to explicitly write out the components of
$upright(bold(w))$, $upright(bold(x))$, and $upright(bold(C))$,
performing the necessary matrix/vector products, and then taking the
necessary scalar derivatives.

== Kronecker delta
<kronecker-delta>
Another approach is to work out the general form of the components of
the gradient—for example, to derive the first identity, it is enough to
show that the $k^(upright("th"))$ component of
$gradient_bold(w) upright(bold(w))^(⊺) upright(bold(x))$
equals $x_k$. If you take this approach, I suggest using the properties
of the Kronecker delta function, which is defined as below.

$
delta_(i j) = cases(
  1 "if" i = j,
  0 "otherwise"
)
$

Taking the derivative of a component of a vector with respect to another
component yields the Kronecker delta function:

$ frac(partial w_i, partial w_k) = delta_(i k) $ where $w_i$ and $w_k$
are the $i^(upright("th"))$ and $k^(upright("th"))$ components of
$upright(bold(w))$, respectively.

Additionally, the following property holds when summing over products of
Kronecker deltas with other expressions:

$ sum_j delta_(i j) w_j = w_i $

#answer([
  *Solution*

  Identity \#1:

  $
    dvp(, bold(w)) bold(w)^T bold(x) &= dvp(, bold(w)) (w_1 x_1 + dots.c + w_N x_N)\
    &= vec(
      dvp(, w_1) (w_1 x_1 + dots.c + w_N x_N),
      dots.v,
      dvp(, w_N) (w_N x_N + dots.c + w_N x_N),
    )\
    &= vec(
      x_1,
      dots.v,
      x_N
    )\
    &= bold(x)

  $

  Identity \#2:

  $
    dvp(, bold(w)) bold(x)^T bold(w) &= dvp(, bold(w)) bold(w)^T bold(x) "(Since inner products commute)"\
    &= bold(x) "(From the proof of Identity #1")
  $

  Identity \#3:

  $
    dvp(, bold(w)) bold(w)^T bold(w) &= dvp(, bold(w)) (w_1^2 + dots.c + w_N^2)\
    &= vec(
      dvp(, w_1) (w_1^2 + dots.c + w_N^2),
      dots.v,
      dvp(, w_N) (w_1^2 + dots.c + w_N^2),
    )\
    &= vec(
      2w_1,
      dots.v,
      2w_N
    )\
    &= 2 bold(w)

  $

  Identity \#4:

  Let us derive the $k^"th"$ component of $dvp(, bold(w)) bold(w)^T bold(C) bold(w)$. This is given by:

  $

    dvp(, w_k) bold(w)^T bold(C) bold(w) &= dvp(, w_k) mat(w_1, dots.c, w_N)
    mat(
      C_(11), dots.c, C_(1N);
      dots.v, dots.down, dots.v;
      C_(N 1), dots.c, C_(N N);
    )
    vec(w_1, dots.v, w_N)\
    &= dvp(, w_k) mat(w_1, dots.c, w_N)
    vec(
      sum_(i = 1)^N C_(1 i) w_i,
      dots.v,
      sum_(i = 1)^N C_(N i) w_i,
    )\
    &= dvp(, w_k) sum_(j = 1)^N w_j sum_(i = 1)^N C_(j i) w_i\
    &= sum_(j = 1)^N sum_(i = 1)^N dvp(, w_k) w_j C_(j i) w_i\
    &= sum_(j = 1)^N sum_(i = 1)^N C_(j i) dvp(, w_k) (w_j w_i)\
    &= sum_(j = 1)^N sum_(i = 1)^N C_(j i) (w_j dvp(, w_k) w_i + w_i dvp(, w_k) w_j) "(Product rule of differentiation)"\
    &= sum_(j = 1)^N sum_(i = 1)^N C_(j i) (w_j delta_(k i) + w_i delta_(k j))\
    &= sum_(j = 1)^N sum_(i = 1)^N C_(j i) w_j delta_(k i) + C_(j i) w_i delta_(k j)\
    &= sum_(j = 1)^N sum_(i = 1)^N C_(j i) w_j delta_(k i) + sum_(j = 1)^N sum_(i = 1)^N C_(j i) w_i delta_(k j)\
    &= sum_(j = 1)^N C_(j k) w_j + sum_(i = 1)^N C_(k i) w_i \
    &= sum_(i = 1)^N C_(i k) w_i + sum_(i = 1)^N C_(k i) w_i "(we can replace j with i in the first term)"\
    &= sum_(i = 1)^N C_(i k) w_i + C_(k i) w_i\
    &= sum_(i = 1)^N C_(k i) w_i + C_(k i) w_i "(Since" bold(C) "is symmetric )"\
    &= 2 sum_(i = 1)^N C_(k i) w_i \
  $

  Thus,
  $

  dvp(, bold(w)) bold(w)^T bold(C w) &=
  vec(
    2 sum_(i = 1)^N C_(1 i) w_i,
    dots.v,
    2 sum_(i = 1)^N C_(N i) w_i,
  )\
  &=
  2 vec(
    sum_(i = 1)^N C_(1 i) w_i,
    dots.v,
    sum_(i = 1)^N C_(N i) w_i,
  )\
  &= 2bold(C w)

  $


],[])

= Workload
<workload>
How much time did you spend on this homework assignment?

#heading(level: 1, numbering: none)[Acknowledgments]
<acknowledgments>
Cite all the people you’ve worked with on this homework, as well as any
other resources you used apart from the FCML textbook.
