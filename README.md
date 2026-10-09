# 2802ICT Study MCQ quiz

Static quiz for the 768 objective questions in `../Study MCQs.md` and `../Study TF.md`. It includes lecture, lab, workshop, assignment, and final-exam-drill sections. It runs in the browser only. There is no account and no saved history beyond the current tab session (a refresh keeps the sitting you are in).

## Use it locally

From this folder:

```
python -m http.server 8080
```

Open `http://localhost:8080/`. Loading `index.html` as a file will fail, because the page fetches `questions.json`.

## Quiz

1. Tick the lecture, lab, workshop, or assignment sections to practise. Select all and Clear apply to every section.
2. Tick multiple choice, true/false, or both. Counts next to each section follow that filter.
3. Choose every question, a random sample, or balanced objective practice. Balanced practice draws 10 multiple-choice and 10 true/false questions across the selected sections.
4. Choose one answer. The quiz locks it, reports whether it is correct, and shows the correct answer and rationale before enabling Next.
5. Use Cancel quiz at any time to discard the current attempt and return to setup.
6. The results page still shows the overall score and a review of every answer.
7. Retry same set keeps the questions and order. New setup returns to the section list.

The Exam drill is the more applied readiness set: 21 multiple choice and 22 true/false.

## Update the question bank

After you edit `Study MCQs.md` or `Study TF.md`:

```
python extract_questions.py
```

That rewrites `questions.json`. Commit it with the site. GitHub Pages does not run the Python script.

## GitHub Pages

Simplest setup: a public repository whose root is this folder (`index.html`, `app.js`, `styles.css`, `questions.json`, `.nojekyll`).

1. Create an empty public GitHub repository.
2. Copy these files into it (not the parent course folder) and push to `main`.
3. In the repository, open Settings, then Pages. Set the source to Deploy from a branch, branch `main`, folder `/ (root)`.
4. The site URL is `https://<user>.github.io/<repo>/`.

`.nojekyll` stops GitHub from running Jekyll on the site.

Answers sit in `questions.json`, so anyone with the URL can read them. That is normal for a static study page.

If this folder stays inside a larger repository, GitHub Pages can only publish `/` (root) or `/docs`. To publish this folder you would move or copy it to `docs/` on the branch Pages uses, or use a separate repository as above.
