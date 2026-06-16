#import "../../common.typ": *
#import "../../equations.typ": expectation

#show: info521

#align(center)[

  #text(size: 14pt, fill: chili, smallcaps[Homework 9])
]


= Fisher Information for Bernoulli distribution
<fisher-information-for-bernoulli-distribution>
#emph[(FCML Exercise 2.13)]

Compute the Fisher information for the parameter of a Bernoulli
distribution.

#answer([
  #strong[Solution] The Fisher Information Matrix (FIM) is an $M times M$
  matrix, where $M$ is the number of parameters of the distribution. Since
  the Bernoulli distribution only has one parameter, the FIM will be a
  single number. Let $Y tilde.op$Bernoulli$(r)$; then the FIM, $cal(I)$,
  is given by
  $ 
  cal(I) &=  bb(E)_(p (y | r)) {- frac(partial^2 log p (y | r), partial r^2)}\
  &=  bb(E)_(p (y | r)) {- frac(partial^2, partial r^2) (y log r + (1 - y) log (1 - r))}\
  &=  bb(E)_(p (y | r)) {- frac(partial, partial r) (y / r - frac(1 - y, 1 - r))}\
  &=  bb(E)_(p (y | r)) {y / r^2 + frac(1 - y, (1 - r)^2)}\
  &=  1 / r + frac(1, 1 - r)\
  &=  frac(1, r (1 - r)) , 
  $ 
  where we have used the fact that $bb(E)_(p (y | r)) {y} = r$.
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
