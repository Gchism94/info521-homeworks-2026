# Homework 1

This homework has two components.
1. **Worksheet**. The first component is a worksheet where you derive the
   normal equations for a simple linear model with 1D inputs and 2 parameters.
   I will provide printed copies of the worksheet in class, but you are
   expected to complete it at home. Use a pen/pencil to complete the worksheet
   and submit a hard copy to me.
2. **Lab**. This repository contains a [Jupytext
   notebook](https://jupytext.readthedocs.io/en/latest/). Jupytext is a tool
   that allows you to work with regular Python files as
   [Jupyter](https://jupyter.org) notebooks.
   Jupyter notebooks are an interactive programming environment, suitable for
   exploratory analysis and teaching concepts. We will use them occasionally in
   this course.


## Lab instructions

### Prerequisites

You will need the Python packages listed in `requirements.txt`. If you don't
already have them, you can install them with the following command-line
invocation:

```
pip install -r requirements.txt
```

### Launching Jupyter Lab

Once you have installed the prerequisites, launch Jupyter Lab using the
following command-line invocation (with the root of the repository as the
current working directory):

```
jupyter lab
```

To open the Jupytext notebook in Jupyter lab, right-click on `hw.py` in the
sidebar on the left, then hover over 'Open With', then click 'Notebook'.

You can work with this notebook just like you would with a Jupyter notebook.
Any changes you make to the input cells will be reflected in the `hw.py` file
when you save the notebook (Ctrl+S on Windows/Linux, Cmd+S on macOS).
However, the outputs will not be saved. Read through the instructions in the
lab and fill in any code that you need to in order to complete the lab.

Tests have been provided for you in `test_hw.py`. You can run `pytest` (just
like in Homework 0) to see if your implementation is correct.

**Note** Alternatively, you can use VS Code with the Jupyter extension to work
on the lab (this method not officially supported by the instructor, but some
students have had success with it).


# Grading
- 1 point: Homework is complete and correct (passes all automated correctness
    tests, feedback PR is not merged, existing docstrings have not been
    edited or deleted, written component has no errors).
- 0.5 points: Homework is incomplete or has errors.
- 0 points: Homework was not submitted on time.

### Submission

In order to complete your submission, you will need to commit and push the
updated `hw.py` file. Remember, the complete homework submission includes both
the programming component (submitted via Github classroom) and the worksheet
(submitted via hard copy).
