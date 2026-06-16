# Homework 0

# Objectives

By the end of this assignment, students will be able to:
- submit assignments containing both written and programming components on
  GitHub Classroom.
- Typeset basic LaTeX documents. LaTeX (https://www.latex-project.org) is a
  widely-used system for typesetting technical and scientific documents, and is
  required for papers at the most prestigious machine learning and artificial
  intelligence research publication venues (e.g., NeurIPS, ICML).

To complete this assignment, complete all the exercises described below.

# Prerequisites

You will need to install the following package if you have not already done
so:

- [Pytest](https://docs.pytest.org)

You can do so by running the command below:

```
pip install -r requirements.txt
```

# Check out the starter code

When you accepted the assignment, Github created a clone of the assignment
template for you at:

```
https://github.com/ua-info521-sp25/hw0-<your Github ID>
```

It also set up a separate `feedback` branch and a
[feedback pull request](https://docs.github.com/en/education/manage-coursework-with-github-classroom/teach-with-github-classroom/leave-feedback-with-pull-requests)
that will allow the instructional team to give you feedback on your work.

To get the assignment code on your local machine (note: you will need to edit
the code on your own computer, not in the browser via the Github web
interface!), clone the repository:

```
git clone https://github.com/ua-info521-sp25-sp24/hw0-<your Github ID>.git
```

You are now ready to begin working on the assignment.
You should do all your work in the default branch, `main`.

# Test your code for correctness

The `test_hw.py` file contains code that tests the correctness of your
implementation. With the repository root as your current working directory, run
the following command to run the tests:

```
pytest
```

When you run the tests on the freshly-cloned repository, you should see output
similar to the following (there is an intentional bug in the code!):

```
================================================= test session starts ==================================================
platform darwin -- Python 3.12.9, pytest-7.4.4, pluggy-1.3.0
rootdir: /Users/adarsh/git/ml4ai/INFO_521/2026_spring/homeworks/hw0/release
plugins: anyio-4.2.0
collected 0 items / 1 error

======================================================== ERRORS ========================================================
_____________________________________________ ERROR collecting test_hw.py ______________________________________________
/Users/adarsh/.venvs/teaching/lib/python3.12/site-packages/_pytest/python.py:617: in _importtestmodule
    mod = import_path(self.path, mode=importmode, root=self.config.rootpath)
/Users/adarsh/.venvs/teaching/lib/python3.12/site-packages/_pytest/pathlib.py:567: in import_path
    importlib.import_module(module_name)
/opt/local/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
/Users/adarsh/.venvs/teaching/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
test_hw.py:1: in <module>
    import hw
E     File "/Users/adarsh/git/ml4ai/INFO_521/2026_spring/homeworks/hw0/release/hw.py", line 2
E       ### YOUR CODE HERE ###
E                             ^
E   IndentationError: expected an indented block after function definition on line 1
=============================================== short test summary info ================================================
ERROR test_hw.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=================================================== 1 error in 0.09s ===================================================
```

**Exercise 1** Fix the error by adding the necessary code under the line in `hw.py` that says `### YOUR CODE HERE ###`, then run `pytest` again.
You should see the following output:

```
============================= test session starts =============================
platform darwin -- Python 3.12.9, pytest-7.4.4, pluggy-1.3.0
rootdir: /Users/adarsh/git/ml4ai/INFO_521/2026_spring/homeworks/hw0/release
plugins: anyio-4.2.0
collected 1 item

test_hw.py .                                                            [100%]

============================== 1 passed in 0.01s ==============================
```

# Submit your code

As you are working on the code, you should regularly commit your code to save
snapshots of your code locally. When I'm working on code, I usually commit
multiple times a day, and sometimes multiple times per hour if I am working on a
complex piece of code. I recommend committing at least once a day.

**Exercise 2** Commit and push the changes you made in Exercise 1.

(Optional) To see which files have changed, run the following command:

```
git status
```

(Optional) To see a summary of the changes, run the following command:

```
git diff
```

In order to commit the changes, you need to first stage the changes by running
`git add` for the files you've changed.

```
git add hw.py
```

(Optional) To see which files have been staged for the commit, you can run

```
git status
```

To commit the changes that you have staged, run the following command:

```
git commit -m "<commit message>"
```

Where `<commit message>` should be replaced by an appropriate commit message
summarizing your changes. Your commit message need not be too long, a sentence
will do. Note that we will typically not read your commit messages, so please
don't use them to inform us of issues with the homework (use Slack instead).

Finally, after committing, you should push your commit(s) with the following
command:

```
git push
```

You should regularly run `git push` to push all saved changes to the remote
repository on GitHub. When you commit and push regularly, it makes it easier
for us to see that you have been working on an assignment regularly, and if you
need an extension or if there is a potential academic integrity violation,
regular commits and pushes will help us give you the benefit of the doubt.

To learn more about Git and Github, you may want to try out the tutorial
[here](https://try.github.io).

Make a habit of checking the "Feedback" pull request on the GitHub page for your
repository.
You should see all your pushed commits there, as well as the status of the
"checks".
If any correctness (pytest) or quality (pylint) tests are failing, you will see
"All checks have failed" at the bottom of the pull request.
If you want to see exactly which tests have failed, click on the "Details" link.
When you have corrected all problems, you should see "All checks have passed"
at the bottom of the pull request.

You do not need to do anything beyond pushing your commits to Github to submit
your assignment.
The instructional team will grade the code of the "Feedback" pull request, and
make detailed comments there.
**Do not merge your pull request.**


# Written component

The written component of the homework must be typeset using LaTeX. If you are
not familiar with LaTeX, you may want to check out [Overleaf's 30-minute LaTeX
tutorial](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes) (but
do so after submitting HW0).

The written component of the homework will be distributed as a .tex file named
`hw.tex`. You must compile the `hw.tex` file in order to actually view the
assignment.

**Exercise 3** Compile `hw.tex` to produce the homework PDF (named `hw.pdf`).

On macOS or Linux, if you've installed the TeX Live distribution, you can do this from the
command line with the following command:
```
latexmk -pdf hw.tex
```

If you prefer to use a different compilation method (e.g., using the TeXShop
editor that is bundled with MacTeX, using Overleaf), you are welcome to do so.

**Exercise 4** Open `hw.tex` in your preferred editor, and change the author
name in the following line:

```tex
\author{Your name here}
```

**Exercise 5**: You will often be asked to include figures in your written
component. Uncomment the lines in the 'Solution' section (from `\begin{figure}`
to `\end{figure}` in `hw.tex`. This piece of code shows you how to insert a
figure into your writeup. Note that all figures must have descriptive captions.
Recompile the document and verify that the image shows up in the PDF.

**Exercise 6**: Fully read and understand the syllabus.

**Exercise 7**: Fully read and understand the policies and resources here: https://catalog.arizona.edu/syllabus-policies

**Exercise 8**: Fully read and understand the College of Information Science Academic Integrity Policy: https://infosci.arizona.edu/students-and-career/academic-integrity

**Exercise 10**: After completing exercises 6, 7, and 8, check the items in
the 'Week 1 tasks' section in `hw.tex`, by
replacing the `$\square$` in the line corresponding to the task with
`$\CheckedBox$`.

**Exercise 11**: You will need to cite anyone you work with on homework
assignments. Fill out the 'Acknowledgments' section to list all the people you
worked with on this assignment. If you did not work with anyone else, please say
so explicitly.

**Exercise 12**: In the 'Workload' section, enter the number of hours you spent
on this assignment outside the classroom.

**Exercise 13**: When you are done with editing `hw.tex`, recompile the PDF to
make sure it looks good to you. Once that is done, please commit and push both
`hw.tex` and `hw.pdf`.

This concludes this assignment!

# Grading

- 1 point: Homework is complete and correct (passes all automated correctness
    tests, PR is not merged, existing docstrings have not been
    edited or deleted, written component has no errors).
- 0.5 points: Homework is incomplete or has errors.
- 0 points: Homework was not submitted on time.

