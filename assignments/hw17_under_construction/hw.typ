#import "../../common.typ": *
#import "../../equations.typ": expectation

#show: info521

#align(center)[
  #text(size: 14pt, fill: chili, smallcaps[Homework 16])

  #course | #semester | Instructor: #instructor
]

= Estimating $pi$ by sampling in 2 dimensions
#emph[(Adapted from FCML Exercise 4.4)]

Given the expression for the area of a circle with radius $r$, $A = pi r^2$, and
using only uniformly distributed random variables, devise a sampling procedure
to estimate the value of $pi$.

A few questions and hints to get you started:

- Can you derive an expression for $pi$ in terms of the area $A$? Can you think
  of a particular value of $r$ that you can choose to simplify this expression?
- What is the equation of a circle centered at the origin in Cartesian coordinates?
- What is the connection between the integral of a univariate function and the
  area under the curve in between the integration limits (#fcml Comment 2.4 in
  $section$ 2.4) ?
- The area of a circle is equal to 4 times the area of a quadrant of the
  circle.
  Can you set up the computation of the area of a circle as the computation of an expectation?
- Can you use sampling to approximate this expectation (see #fcml $section$ 2.4)?
- Over what distribution would this expectation be? 
- How would you sample from this distribution (see #fcml $section$ 2.5.1 and
  #pml2 $section$ 11.4)?

Describe the procedure you devised in the written portion of this homework. Then, implement it in the function
`estimate_pi_using_circle` in `hw.py`.

#answer(
  [

    Setting $r = 1$, we have 
    $ 
      A &= pi
    $

    We can estimate the area of a single quadrant of the circle and multiply it
    by 4 to get the area of the whole circle.

    The area of quadrant is given by 

    $ integral_(x = 0)^1 integral_(y=0)^1 (x^2 + y^2) d x d y $. 

    We can estimate this area using rejection sampling. 
    Draw samples from the uniform distribution to construct $N$ samples of 2D
    points in the square that has corners (0, 0), (1, 1). The area of the
    quadrant will be given by the ratio of the number of samples inside the
    circles (i.e., samples for which $x^2 + y^2 < 1$)  to the total number of
    samples. Once we get the area of the quadrant, multiply it by 4 to get an
    estimate of $pi$.
  ],
  []
)

= Sampling in 3 dimensions

Adapt your approach from earlier to estimate the value of $pi$ given the
expression for the volume of a sphere with radius $r$: 

$ V = frac(4, 3) pi r^3 $.

You may find it helpful to derive an analytical expression for $pi$ as a
function of the volume $V_o$ of an octant of the unit sphere. Describe how you
adapted your approach in the written portion of this homework. Implement your adapted approach in the function
`estimate_pi_using_sphere` in `hw.py`.

#answer(
  [

    Setting $r = 1$, we have 
    $ 
      V &= frac(4, 3) pi \
      => pi &= frac(3 V, 4) = frac(3, 4) dot.c 8 V_mtext("oct") = 6 V_mtext("oct")
    $.

    where $V_mtext("oct")$ is the volume of an octant of the sphere (there are
    8 octants in the sphere). We can compute the volume of the octant using
    rejection sampling like we did with the sphere, but this time we would need
    to integrate over a cube with (0, 0, 0) and (1, 1, 1) as two opposite
    corners. And the condition we would need to check for accepting samples is
    simply to check whether $norm(bold(x)) < 1$, where $bold(x)$ represents the
    position of the sample in Cartesian coordinates.

  ],
  []
)

= Sampling in $n$ dimensions

An $n$-ball is the generalization of $2D$ circles and $3D$ spheres to an
arbitrary number of dimensions $n$.
Generalize your approach to estimate the value of $pi$ given the the expression
for the 'hypervolume' $V_n$ of an $n$-ball:

$ V_n = frac(pi^frac(n, 2), Gamma(frac(n, 2) + 1)) r^n $

The generalizations of quadrants and octants to higher dimensions are known as
_orthants_. You may find it helpful to derive an analytical expression for $pi$
in terms of the volume $V_o$ of an orthant of the $n$-ball. 
Describe your generalization in the written portion of this homework, and
implement it in the `estimate_pi_using_n_ball` function in `hw.py`.

#answer(
  [

    Setting $r = 1$, we have 
    $ 
        V_n &= frac(pi^frac(n, 2), Gamma(frac(n, 2) + 1)) \
      => pi^frac(n, 2) &= V_n dot.c Gamma(frac(n, 2) + 1) \
      => pi &= (V_n dot.c Gamma(frac(n, 2) + 1))^(frac(2, n)) \
      => pi &= (2^n dot.c V_o dot.c Gamma(frac(n, 2) + 1))^frac(2, n)

    $

    where $V_o$ the volume of the 'generalized octant'
  ],
  []
)

= Curse of dimensionality

It will be instructive to see how fast we can converge (i.e., how many samples
do we need) to a precise estimate of $pi$, and how this varies with the number
of dimensions we are dealing with.

Make a plot showing the mean and variance of $|pi - hat(pi)|$ (i.e., the magnitude of the
difference between $hat(pi)$---the estimated value of $pi$ using sampling---and
the true value of $pi$) as a function of the number of samples used to
obtain $hat(pi)$. Include one curve each for 2D, 3D, 4D, and 5D sampling, and use
logarithmic scales for the axes.
Qualitatively describe what you see in the plot. 


= Workload
<workload>
How many hours did you spend on this homework assignment?

#heading(level: 1, numbering: none)[Acknowledgments]
<acknowledgments>

Cite all the people you've worked with on this homework, as well as any other
resources you used apart from the FCML textbook. If you used generative AI
tools (e.g., ChatGPT), please describe how you used them.

If you did not work with anyone else or use generative AI tools, please say so.
