# 2802ICT Study MCQ quiz

Static quiz for the multiple-choice questions in `../Study MCQs.md` and the true/false questions in `../Study TF.md`. It runs in the browser only. There is no account and no saved history beyond the current tab session (a refresh keeps the sitting you are in).

## Use it locally

From this folder:

```
python -m http.server 8080
```

Open `http://localhost:8080/`. Loading `index.html` as a file will fail, because the page fetches `questions.json`.

## Quiz

1. Learn one topic in the study guide and answer its Check yourself questions from memory.
2. Tick the matching lecture, lab, or assignment. Select all and Clear apply to every section.
3. Tick multiple choice, true/false, or both. Counts next to each section follow that filter.
4. Choose every question, a random sample, or balanced objective practice. Balanced practice draws 10 multiple-choice and 10 true/false questions across the selected sections.
5. Answer one question at a time. Next stays disabled until you choose. On the last question, Next becomes Submit.
6. The results page shows the score, each answer, an explanation, and a link back to the matching guide section.
7. Explain each mistake before retrying it. Retry same set keeps the questions and order. New setup returns to the section list.

The Exam drill is the more applied readiness set: 21 multiple choice and 22 true/false. The study guide includes the two unscored long-response prompts. The setup page states the paper shape described in the lectures: 10 true/false, 10 multiple choice, 2 longer answers, 40 marks with a 16-mark hurdle.

## Update the question bank

The home page links to the study guide. That page is `guide.html`, which renders `study-guide.md`.

After you edit `Study MCQs.md`, `Study TF.md`, or `Study Guide.md`:

```
python extract_questions.py
```

That rewrites `questions.json` and copies `Study Guide.md` to `study-guide.md`. Commit those files with the site. GitHub Pages does not run the Python script.

## GitHub Pages

Simplest setup: a public repository whose root is this folder (`index.html`, `app.js`, `styles.css`, `questions.json`, `.nojekyll`).

1. Create an empty public GitHub repository.
2. Copy these files into it (not the parent course folder) and push to `main`.
3. In the repository, open Settings, then Pages. Set the source to Deploy from a branch, branch `main`, folder `/ (root)`.
4. The site URL is `https://<user>.github.io/<repo>/`.

`.nojekyll` stops GitHub from running Jekyll on the site.

Answers sit in `questions.json`, so anyone with the URL can read them. That is normal for a static study page.

If this folder stays inside a larger repository, GitHub Pages can only publish `/` (root) or `/docs`. To publish this folder you would move or copy it to `docs/` on the branch Pages uses, or use a separate repository as above.
