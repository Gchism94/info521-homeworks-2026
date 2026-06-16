#import "@preview/diverential:0.3.0": *
#import "@preview/physica:0.9.5": grad, evaluated

// Page setup

// UA colors
#let azred = rgb(171, 5, 32)
#let azblue = rgb(12, 35, 75)
#let azurite = rgb(30, 82, 136)
#let oasis = rgb("378DBD")
#let coolgray = rgb("E2E9EB")
#let warmgray = rgb("F4EDE5")
#let chili = rgb("8B0015")
#let leaf = rgb("70B865")
#let river = rgb("007D84")
#let mesa = rgb("A95C42")

#let citep(key) = cite(key, form: "prose")
#let hessian(content) = [$bold(H)_(content)$]
#let jacobian(content) = [$bold(J)_(content)$]

// Spaced small caps
#let ssc(content) = {
  smallcaps(text(lower(content), tracking: 0.07em))
}

// Acronyms
#let fcml = ssc[fcml]
#let m4ml = ssc[m4ml]
#let udl = ssc[udl]
#let pml1 = ssc[pml1]
#let pml2 = ssc[pml2]
#let mle = ssc[mle]
#let pdf = ssc[pdf]
#let d2l = ssc[d2l]
#let lhs = ssc[lhs]
#let rhs = ssc[rhs]

// Other text substitutions
#let sections = [$section section$]


// Boolean switch to control whether answers are shown or not.
#let show_answers = true

#if sys.inputs.at("show_answers", default: none) == "false" {
  show_answers = false
}


#let course = [#ssc[INFO] 521]
#let semester = "Spring 2026"
#let instructor = "Adarsh Pyarelal"

// Upright text in math mode
#let mtext = text.with(font: "Arno Pro")

#let info521(doc) = {

  // Square brackets for vectors and matrices
  set math.vec(delim: "[")
  set math.mat(delim: "[")

  set math.equation(numbering: "(1)")

  set page(
    paper: "us-letter",
    number-align: center,
    numbering: "1"
  )

  set enum(numbering: "1.a.i.")
  set text(
    font: "Arno Pro", 
    number-type: "old-style"
  )


  // Using lining numbers in equations
  show math.equation: set text(font: "Euler Math", number-type: "lining")

  show math.op: it => text(font: "Arno Pro", it.text)

  show link: set text(fill: azurite)

  // Style references
  show ref: it => {
    let eq = math.equation
    let el = it.element
    if el != none {
    if el.func() == eq {
      // Override equation references.
      link(el.location(),numbering(
        el.numbering,
        ..counter(eq).at(el.location())
      ))
    } else if el.func() == heading {
      // Override section references.
      [$section$];
      link(
        el.location(),
        numbering(
          el.numbering,
          ..counter(heading).at(el.location())
        )
      )
    } else {
      // Other references as usual.
      it
    }

    } 
  }
  show ref: set text(fill: azurite)

  set list(tight: true)

  // Style headings

  show title: el => align(center)[#text(size: 14pt, smallcaps(el), weight:
  "regular", fill: chili)]

  set heading(numbering: "1.1")

  show heading.where(level: 1): it => text(
    size: 16pt,
    font: "Alegreya Sans",
    weight: "bold",
    fill: azurite,
    it
  )

  show heading.where(level: 2): it => text(
    size: 15pt,
    font: "Alegreya Sans",
    weight: "bold",
    fill: azurite,
    it
  )

  show heading.where(level: 3): it => text(
    size: 14pt,
    font: "Alegreya Sans",
    weight: "bold",
    fill: azurite,
    it
  )

  show heading.where(level: 4): it => text(
    size: 13pt,
    font: "Alegreya Sans",
    weight: "regular",
    style: "italic",
    fill: azurite,
    it
  )

  show heading.where(level: 5): it => text(
    size: 12pt,
    font: "Alegreya Sans",
    weight: "regular",
    style: "italic",
    fill: azurite,
    it
  )

  show outline.entry.where(
    level: 1
  ): it => {
    v(12pt, weak: true)
    text(font: "Alegreya Sans", weight: "bold", fill: azurite, it)
  }

  show outline.entry.where(
    level: 2
  ): it => {
    text(size: 11pt, it)
  }

  show outline.entry.where(
    level: 3
  ): it => {
    text(size: 10pt, it)
  }



  let blank(content) = {
    if show_answers [
      #underline[~#content~]
    ] else [
      #underline[~~~~~~~~~~~~~~~~~]
    ]
}

  doc
}

#let points(points) = {
  if points == 1 [
    (#underline[~~~~~]/1 point)
  ] else [
    (#underline[~~~~~]/#points points)
  ]
}

#let answer(content, alternative) = context {
  context if show_answers [
    #set text(blue)
    #content
  ] else [#alternative]
}

#let blank(content) = {
  context if show_answers [
    #box[#underline[~#text(blue)[#content]~]]
  ] else [
    #box[#underline[~~~~~~~~~~~~~~~~~]]
  ]
}
