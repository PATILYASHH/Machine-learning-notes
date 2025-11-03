# Quetions

# *UNIT 1*

### Unit 1 - 4 marks 
---
Q. Explain diffrent phases of predictive modeling (8 phases) [Click Here](4Q1.md)

Q. Advantages and Disadvantages of K-nearest neighbor algorithm [Click Here](4Q2.md)

Q. Define Machine Learning and explain features of machine learning [Click Here](4Q3.md)


### Unit 1 - 8 marks
---
Q. Explain Diffrence between Artificial Intelligence and Machine learning [Click Here](Q4.md)

Q. Explain Development steps in Machine Learning [Click Here](Q5.md)

Q. Explain K-nearest nighbor algorithm in detail [Click Here](Q6.md)

---


# *UNIT 2*

### Unit 2 - 4 marks
---
Q. State the goals of Machine Learning [Click Here](Q7md)

Q. Write a note on speech Recognition and production recommendations [click here](Q8.md)

Q. Advantages and Disadvantages of machine learning [Click Here](Q9.md)

Q. Write a note on function approximation [Click Here](Q10.md)

### Unit 2 - 8 Marks
---
Q. Explain in detail the application of Machine learning [Click Here](Q11.md)

Q. What is the need for ML? Explain in detail classification of ML [Click Here](Q12.md)

Q. Explain steps to design a learning system [Click Here](Q13.md)

---
# *UNIT 3*
### Unit 3 - 4 marks
---
Q. Explain bias and variance with example[Click here](Q14.md)

Q. Write a short note on confusion matrix [Click here](Q15.md)

Q. How to treat data in ML [Click here](Q16.md)

Q. What is Data pre-processing? Why do we need it ? [Click here](Q17.md)

Q. Explain performance measures of ML [Click here](Q18.md)

Q. Write a note on bootstrap sampling [Click here](Q19.md)

Q. Difference between bagging and boosting [Click here](Q20.md)

Q. Write a note on bagging aggregatiion [Click here](Q21.md)

---
### Unit 3 - 8 marks
---

Q. Explain in detail types of ML [Click here](Q22.md)

Q. what is bias and variance ? Explain in detail [Click here](Q23.md)

Q. What is bias and variance and what is Bias-variance tradeof ? [Click here](Q24.md)

Q. Explain overfitting and underfitting in ML [Click here](Q25.md)


---
# *UNIT 4*
---

Q. State and prove baye's theorem with example [Click here](Q26.md)

Q. What is probability ? What are the rules of probability  [Click here](Q27.md)

Q. Difference between permutation and combination  [Click here](Q28.md)

---

## Notes website generator

This repository now includes a small static site generator to turn these markdown notes into a browsable website.

Quick start to build the site locally:

1. (Optional but recommended) create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Build the site:

```bash
python3 build.py
```

The generated site will be written to the `site/` directory. Open `site/index.html` in your browser to view.

Files added:

- `build.py` — generator script that converts each top-level `.md` into an HTML page and creates `site/index.html`.
- `templates/base.html` — simple HTML template used for pages.
- `static/style.css` — basic styling for the notes site.
- `requirements.txt` — minimal Python dependencies (markdown, pygments).

If you want a different layout, front-matter, tags, or search, tell me and I can extend the generator.