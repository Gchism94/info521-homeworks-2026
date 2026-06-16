#import "../../common.typ": *
#import "../../equations.typ": expectation
#import "@preview/fletcher:0.5.7" as fletcher: diagram, node, edge

#show: info521

#align(center)[

  #text(size: 14pt, fill: chili, smallcaps[Homework 13])
]

= Drawing probabilistic graphical models

Draw the probabilistic graphical model corresponding to the task of inferring
the model parameters from training data for the Bayesian logistic regression
model with a Gaussian prior on the parameters we are studying in class. Use
plate notation wherever appropriate.

#answer([

  *Solution*:

  #set text(blue)
The joint probability distribution of the model parameters
$bold(w)$ and the outputs $bold(t)$ is given below, along with its
factorization into the product of the prior and likelihood.

$
  p(bold(w), bold(t) | bold(X), sigma^2)
  = p(bold(w)|sigma^2)product_(n = 1)^N p(t_n|bold(x)_n, bold(w))
$

The PGM should look like the one below. If the layout is slightly different but
the diagram's semantics are accurate, that is ok.

  #set text(black)

  #diagram(
    node-stroke: .1em,
    node-shape: circle,
    node((0, 0), align(right)[$sigma^2$], name: <sigma>),
    node((0, 1), $bold(w)$, name: <w>),
    node((1, 2), $bold(x)_n$, name: <xn>, fill: gray),
    node((0, 2), $t_n$, name: <tn>, fill: gray),
    node((1.5, 2.5), $N$, name: <N>, stroke: none),
    edge(<xn>, <tn>, "->"),
    edge(<sigma>, <w>, "->"),
    edge(<w>, <tn>, "->"),
    node(shape: rect, enclose: (<xn>, <tn>, <N>), inset: 10pt),
  )


], v(4in))
