# 2802ICT Study MCQ quiz

Static quiz for the multiple-choice questions in `../Study MCQs.md` and the true/false questions in `../Study TF.md`. It runs in the browser only. There is no account and no saved history beyond the current tab session (a refresh keeps the sitting you are in).

## Use it locally

From this folder:

```
python -m http.server 8080
```

Open `http://localhost:8080/`. Loading `index.html` as a file will fail, because the page fetches `questions.json`.

## Quiz

1. Tick the lectures, labs, and assignments you want. Select all and Clear apply to every section.
2. Tick multiple choice, true/false, or both. Counts next to each section follow that filter.
3. Choose every question in those sections, or a random sample of n. n is limited to the size of the selected pool.
4. Answer one question at a time. Multiple choice uses A to D. True/false uses True and False. Next stays disabled until you choose. On the last question, Next becomes Submit.
5. The results page shows correct / total, a percentage, and each question marked correct or incorrect, with your choice, the right choice, and the short appendix note.
6. Retry same set keeps the same questions and order. New setup returns to the section list.

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
