#import "../../../common.typ": *
#show: info521
#show math.equation.where(block: true): it => {
  set align(left)
  block(inset: (left: 1cm), it)
}
#set math.equation(numbering: "(1)")

= Worksheet 1: Normal equations
<worksheet-1-normal-equations>

#v(0.25in)

Name: #underline[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]

#v(0.25in)

== Introduction
<introduction>
In this worksheet, you will derive the normal equations for a simple
linear model and loss function.

== Preliminaries
<preliminaries>
=== Squared Error
<squared-error>

$ cal(L)_n = (t_n - f (x_n ; w_0 , w_1))^2 $
<eq:loss_fn>

=== Mean Squared Error
<mean-squared-error>
$ cal(L) = 1 / N sum_(n = 1)^N cal(L)_n (t_n , f (x_n ; w_0 , w_1)) $<eq:mse>

== Least Mean Squares solution for single variable, 2 parameter linear model
<least-mean-squares-solution-for-single-variable-2-parameter-linear-model>

=== Our model
<our-model>
$ f (x ; w_0 , w_1) = w_0 + w_1 x $
<eq:model>

#strong[Step 1:] Start by writing down the mean squared error expression
from @eq:mse;.

#rect(width: 100%, height: 0.5in, stroke: 0.5pt)
#strong[Step 2:] Substitute in our specific loss function from
@eq:loss_fn

#rect(width: 100%, height: 0.5in, stroke: 0.5pt)
#strong[Step 3:] Substitute in our specific model family from
@eq:model

#rect(width: 100%, height: 0.5in, stroke: 0.5pt)
#strong[Step 4:] Multiply out and re-arrange the terms to obtain
@eq:step_4;.

$ cal(L) = 1 / N sum_(n = 1)^N (w_1^2 x_n^2 + 2 w_1 x_n (w_0 - t_n) + w_0^2 - 2 w_0 t_n + t_n^2) $
<eq:step_4>

At the minimum of $cal(L)$, the partial derivatives of $cal(L)$ with
respect to $w_0$ and $w_1$ must be 0.#footnote[To take the partial
derivative of $cal(L)$ with respect to $w_0$, just compute
$dvcp(cal(L), w_0)$, treating all variables other than $w_0$ as constants
(and similarly for $w_1$).] Thus, we need to find values of $w_0$ and
$w_1$ such that the following equations are satisfied#footnote[In this course we
will often use the compact derivative notation $(dvcp(f,x))$ in place of the
Leibniz notation used in #ssc[fcml] $(dvp(f,x))$]:

$ dvcp(cal(L), w_0) & = 0\
dvcp(cal(L), w_1) & = 0 $

#strong[Step 5:] Let us start by computing the partial derivative of
$cal(L)$ with respect to $w_0$, i.e.,
$dvcp(cal(L), w_0)$. You could do it directly if you
want to, but steps 5, 6, 7 break it up into smaller steps if you are
unsure of how to proceed.

First, take the RHS of @eq:step_4 and remove any
terms that do not contain $w_0$:

#rect(width: 100%, height: 0.7in, stroke: 0.5pt)

#strong[Step 6:] Take the expression in step 5 and move the summation
sign inward, e.g.,
$sum_(n = 1)^N (a_n + b_n) = sum_(n = 1)^N a_n + sum_(n = 1)^N b_n$.


#box(height: 0.7in,
stroke:0.5pt,
inset:20pt,
block[
$  dvcp(cal(L), w_0) = $
]
)

#strong[Step 7:] Finally, take the derivative of the remaining terms of
the RHS (i.e., what you have in Step 6) with respect to $w_0$:

#box(height: 0.7in,
stroke:0.5pt,
inset:20pt,
block[
$  dvcp(cal(L), w_0) = $
])

#strong[Step 8:] Solve the equation $dvcp(cal(L), w_0) = 0$ to
obtain $w_0$.

#box(height: 1.5in,
stroke:0.5pt,
inset: 20pt,
block[
$  w_0 = $
])


#strong[Step 9:] Repeat steps 5, 6, 7, and 8, but this time with $w_1$
instead of $w_0$. This will give you an expression for $w_1$.

#strong[Step 10:] Rewrite the equations you obtained in Steps 8 and 9,
with the following notation for the mean of an expression $a$:

$ overline(a) & = 1 / N (sum_(n = 1)^N a_n) $

#block[
]
In the end, you should have the following so-called #strong[normal
equations];:

$ w_0 & = overline(t) - w_1 overline(x)\
w_1 & = frac(overline(x t) - overline(x) overline(t), overline(x^2) - (overline(x)^2)) $
