// INFO 521 unit intros — Typst accents (PDF only).
// Red (#AB0520) is reserved for accents: a thin rule under each section heading,
// and a left border on blockquotes. Heading/link text colour comes from _brand.yml.
#show heading.where(level: 1): it => {
  it
  v(-0.5em)
  line(length: 100%, stroke: 1pt + rgb("#AB0520"))
}
#show quote.where(block: true): it => block(
  width: 100%,
  inset: (left: 0.9em, top: 0.5em, bottom: 0.5em),
  stroke: (left: 2pt + rgb("#AB0520")),
  it.body,
)
