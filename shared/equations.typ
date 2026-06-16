#import "@preview/diverential:0.3.0": *
#import "common.typ": mtext

= Equations
//#align(center, text(17pt)[ Equations ])

#v(1in)
#let expectation(func, dist) = {
  $bold(E)_#dist {#func}$
}

// Jacobian
#let jacobian(f, x) = {
  $dvps(#f,bold(#x)^T)$
}

// Kronecker delta
#let kdelta(i, j) = {
  $delta_(#i #j)$
}

$ #expectation([f(X)], [P(X)]) =  sum_x f(x)P(x) $
$ #expectation([f(x)], [p(x)]) =  integral f(x)p(x)dif x $
$ #mtext("var") {X} = #expectation([$X^2$], [P(x)]) - #expectation([X], [P(x)])^2 $
$ #mtext("cov") {bold(x)} = #expectation([$bold(x) bold(x)^T$], [P($bold(x)$)]) -
#expectation([$bold(x)$], [P($bold(x)$)])#expectation([$bold(x)$], [P($bold(x)$)])^T $
$ #mtext("Beta") (x|a,b) = frac(1, B(a, b)) x^(a - 1) (1 - x)^(b - 1) $
$ B(a,b) = frac(Gamma(a) Gamma(b), Gamma(a+b)) $
$ #mtext("Bernoulli") (x|r) = r^x (1-r)^(1 - x) $
$ #mtext("Binomial") (x|N, r) = binom(N, x) r^x (1-r)^(N - x) $
$ #mtext("Gaussian") (x|mu, sigma^2) = frac(1, sigma sqrt(2pi)) exp(-frac((x - mu)^2,
2sigma^2)) $
$ #mtext("Gaussian") (bold(x)|bold(mu), bold(Sigma)) =
frac(1, (2pi)^frac(D,2) abs(Sigma)^frac(1,2)) exp(-frac(1, 2)(bold(x) -
bold(mu))^T bold(Sigma)^(-1) (bold(x) - bold(mu))) $
$ p(theta|D) = frac(p(theta)p(D|theta), p(D)) $
