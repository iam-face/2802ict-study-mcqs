# 2802ICT Study MCQ quiz

Static quiz for the questions in `../Study MCQs.md`. It runs in the browser only. There is no account and no saved history beyond the current tab session (a refresh keeps the sitting you are in).

## Use it locally

From this folder:

```
python -m http.server 8080
```

Open `http://localhost:8080/`. Loading `index.html` as a file will fail, because the page fetches `questions.json`.

## Quiz

1. Tick the lectures, labs, and assignments you want. Select all and Clear apply to every section.
2. Choose every question in those sections, or a random sample of n. n is limited to the size of the selected pool.
3. Answer one question at a time. Next stays disabled until you pick A, B, C, or D. On the last question, Next becomes Submit.
4. The results page shows correct / total, a percentage, and each question marked correct or incorrect, with your letter, the right letter, the choice text, and the short appendix note.
5. Retry same set keeps the same questions and order. New setup returns to the section list.

## Update the question bank

After you edit `Study MCQs.md`:

```
python extract_questions.py
```

That rewrites `questions.json`. Commit the new JSON with the site. GitHub Pages does not run the Python script.

## GitHub Pages

Simplest setup: a public repository whose root is this folder (`index.html`, `app.js`, `styles.css`, `questions.json`, `.nojekyll`).

1. Create an empty public GitHub repository.
2. Copy these files into it (not the parent course folder) and push to `main`.
3. In the repository, open Settings, then Pages. Set the source to Deploy from a branch, branch `main`, folder `/ (root)`.
4. The site URL is `https://<user>.github.io/<repo>/`.

`.nojekyll` stops GitHub from running Jekyll on the site.

Answers sit in `questions.json`, so anyone with the URL can read them. That is normal for a static study page.

If this folder stays inside a larger repository, GitHub Pages can only publish `/` (root) or `/docs`. To publish this folder you would move or copy it to `docs/` on the branch Pages uses, or use a separate repository as above.
