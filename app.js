const STORAGE_KEY = "mcq-quiz-session";
const GUIDE_ANCHORS = {
  L1: "lecture-1-introduction-and-agents",
  L2: "lecture-2-uninformed-search",
  L3: "lecture-3-informed-search",
  L4A: "lecture-4-local-search-and-csps",
  L4B: "lecture-4-local-search-and-csps",
  L5: "lecture-5-machine-learning-basics",
  L6: "lecture-6-linear-models",
  L7: "lecture-7-feed-forward-neural-networks",
  L8: "lecture-8-model-selection-and-regularisation",
  L9: "lecture-9-decision-trees",
  L10: "lecture-10-bayes-nets",
  L11: "lecture-11-mdps-and-reinforcement-learning",
  Lab5: "lecture-5-machine-learning-basics",
  Lab6: "lecture-6-linear-models",
  Lab7: "lecture-7-feed-forward-neural-networks",
  Lab8: "lecture-7-feed-forward-neural-networks",
  Lab9: "lecture-9-decision-trees",
  A1: "lecture-4-local-search-and-csps",
  A2: "lecture-8-model-selection-and-regularisation",
};

const state = {
  bank: null,
  screen: "setup",
  selected: new Set(),
  types: new Set(["mcq", "tf"]),
  mode: "all",
  n: 20,
  quiz: [],
  answers: {},
  index: 0,
};

const app = document.getElementById("app");

function sectionTitle(id) {
  const section = state.bank.sections.find((item) => item.id === id);
  return section ? section.title : id;
}

function questionType(question) {
  return question.type || "mcq";
}

function lettersFor(question) {
  return questionType(question) === "tf" ? ["T", "F"] : ["A", "B", "C", "D"];
}

function pool() {
  return state.bank.questions.filter((question) => (
    state.selected.has(question.sectionId) && state.types.has(questionType(question))
  ));
}

function shuffle(items) {
  const copy = items.slice();
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    const swap = copy[i];
    copy[i] = copy[j];
    copy[j] = swap;
  }
  return copy;
}

function balancedSample(questions, type, count) {
  const groups = new Map();
  questions
    .filter((question) => questionType(question) === type)
    .forEach((question) => {
      if (!groups.has(question.sectionId)) {
        groups.set(question.sectionId, []);
      }
      groups.get(question.sectionId).push(question);
    });

  groups.forEach((items, id) => groups.set(id, shuffle(items)));
  const sectionIds = shuffle(Array.from(groups.keys()));
  const chosen = [];
  let round = 0;
  while (chosen.length < count) {
    let added = false;
    for (const id of sectionIds) {
      const items = groups.get(id);
      if (round < items.length) {
        chosen.push(items[round]);
        added = true;
        if (chosen.length === count) {
          break;
        }
      }
    }
    if (!added) {
      break;
    }
    round += 1;
  }
  return chosen;
}

function clampN(value, max) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed < 1) {
    return Math.min(1, max);
  }
  return Math.min(parsed, max);
}

function saveSession() {
  const payload = {
    screen: state.screen,
    selected: Array.from(state.selected),
    types: Array.from(state.types),
    mode: state.mode,
    n: state.n,
    quizIds: state.quiz.map((question) => question.id),
    answers: state.answers,
    index: state.index,
  };
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function restoreSession() {
  const raw = sessionStorage.getItem(STORAGE_KEY);
  if (!raw) {
    state.selected = new Set(state.bank.sections.map((section) => section.id));
    return;
  }
  try {
    const saved = JSON.parse(raw);
    state.selected = new Set(saved.selected || []);
    state.types = new Set(Array.isArray(saved.types) && saved.types.length ? saved.types : ["mcq", "tf"]);
    state.mode = ["all", "random", "balanced"].includes(saved.mode) ? saved.mode : "all";
    state.n = Number.isFinite(saved.n) ? saved.n : 20;
    state.answers = saved.answers || {};
    state.index = saved.index || 0;
    const byId = new Map(state.bank.questions.map((question) => [question.id, question]));
    state.quiz = (saved.quizIds || []).map((id) => byId.get(id)).filter(Boolean);
    if ((saved.screen === "quiz" || saved.screen === "results") && state.quiz.length) {
      state.screen = saved.screen;
      state.index = Math.min(state.index, state.quiz.length - 1);
    }
  } catch (err) {
    state.selected = new Set(state.bank.sections.map((section) => section.id));
  }
}

function startQuiz() {
  const available = pool();
  if (!available.length) {
    return;
  }
  const nInput = document.querySelector("#sample-n");
  if (state.mode === "random" && nInput) {
    state.n = clampN(nInput.value, available.length);
  }
  let chosen = available;
  if (state.mode === "random") {
    const count = clampN(state.n, available.length);
    state.n = count;
    chosen = shuffle(available).slice(0, count);
  } else if (state.mode === "balanced") {
    const mcqs = balancedSample(available, "mcq", 10);
    const trueFalse = balancedSample(available, "tf", 10);
    if (mcqs.length < 10 || trueFalse.length < 10) {
      return;
    }
    chosen = shuffle([...mcqs, ...trueFalse]);
  }
  state.quiz = chosen;
  state.answers = {};
  state.index = 0;
  state.screen = "quiz";
  saveSession();
  render();
}

function retrySame() {
  state.answers = {};
  state.index = 0;
  state.screen = "quiz";
  saveSession();
  render();
}

function newSetup() {
  state.screen = "setup";
  state.quiz = [];
  state.answers = {};
  state.index = 0;
  saveSession();
  render();
}

function currentAnswered() {
  const question = state.quiz[state.index];
  return Boolean(question && state.answers[question.id]);
}

function goNext() {
  if (!currentAnswered()) {
    return;
  }
  if (state.index >= state.quiz.length - 1) {
    state.screen = "results";
  } else {
    state.index += 1;
  }
  saveSession();
  render();
}

function goPrev() {
  if (state.index <= 0) {
    return;
  }
  state.index -= 1;
  saveSession();
  render();
}

function pick(letter) {
  const question = state.quiz[state.index];
  state.answers[question.id] = letter;
  saveSession();
  render();
}

function shownAnswer(question, letter) {
  if (!letter) {
    return "none";
  }
  const text = question.choices[letter];
  return text ? `${letter}. ${text}` : letter;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderSetup() {
  const groups = [
    ["exam", "Exam drill"],
    ["lecture", "Lectures"],
    ["lab", "Labs"],
    ["assignment", "Assignments"],
  ];
  const available = pool().length;
  const availableMcq = pool().filter((question) => questionType(question) === "mcq").length;
  const availableTf = pool().filter((question) => questionType(question) === "tf").length;
  const balancedReady = availableMcq >= 10 && availableTf >= 10;
  const nValue = available ? clampN(state.n, available) : state.n;
  const groupsHtml = groups.map(([kind, label]) => {
    const items = state.bank.sections.filter((section) => section.kind === kind);
    if (!items.length) return "";
    const list = items.map((section) => {
      const count = state.bank.questions.filter((q) => (
        q.sectionId === section.id && state.types.has(questionType(q))
      )).length;
      const checked = state.selected.has(section.id) ? "checked" : "";
      return `<li><label><input type="checkbox" data-section="${section.id}" ${checked}>
        <span>${escapeHtml(section.title)} <span class="meta">(${count})</span></span></label></li>`;
    }).join("");
    return `<h2>${label}</h2><ul class="section-list card">${list}</ul>`;
  }).join("");

  app.innerHTML = `
    <h1>2802ICT Study MCQs</h1>
    <aside class="disclaimer">
      <p>This is an unofficial revision aid made by a student. It is not affiliated with, endorsed by, or provided by Griffith University, the 2802ICT convenor, or the teaching team.</p>
      <p>The questions, answers, and study guide were drafted with AI from the author's own notes. They can be wrong, incomplete, or out of date. Use them as a guide only, and check anything you rely on against the lectures, labs, and assignment briefs.</p>
    </aside>
    <aside class="exam-note">
      <p><strong>Exam, as said in the lectures.</strong> 22 questions: 10 true/false, 10 multiple choice, 2 longer answers. 2 hours plus 10 minutes reading, and you may write during the reading. The paper is 40 marks, and you need 16 of those 40 to pass the course. Closed book, one blank sheet. The sample paper shows the format, not which topics will appear. Most students sit on 19 October. Book the slot in ProctorU.</p>
      <p>Questions follow the labs, the lecture examples, and the weekly exercises. There may be one on what an assignment function does. The example he read out was Assignment 1 <code>revise</code>: it changes the domain of x in place and returns whether that domain changed. You are not asked to derive complexity, to memorise the information-gain formula, or to recite MRV. Week 11 is about 4 marks and is meant to be simple. A correct Bayes-net calculation is accepted even if a shorter one exists.</p>
    </aside>
    <p class="lede">Learn a topic in the guide, practise it here, then use a balanced session or the final exam drill to check whether you can apply it. Scoring happens after you submit.</p>
    <div class="row-actions">
      <button type="button" id="select-all">Select all</button>
      <button type="button" id="clear-all">Clear</button>
    </div>
    ${groupsHtml}
    <h2>Question type</h2>
    <div class="card">
      <div class="mode">
        <label><input type="checkbox" data-type="mcq" ${state.types.has("mcq") ? "checked" : ""}> Multiple choice</label>
        <label><input type="checkbox" data-type="tf" ${state.types.has("tf") ? "checked" : ""}> True / false</label>
      </div>
    </div>
    <h2>Session</h2>
    <div class="card">
      <div class="mode">
        <label><input type="radio" name="mode" value="all" ${state.mode === "all" ? "checked" : ""}> All questions in the selected sections</label>
        <label><input type="radio" name="mode" value="random" ${state.mode === "random" ? "checked" : ""}> Random sample</label>
        <label><input type="radio" name="mode" value="balanced" ${state.mode === "balanced" ? "checked" : ""}> Balanced objective practice: 10 multiple choice and 10 true/false, spread across the selected sections</label>
      </div>
      <div class="n-field" ${state.mode === "random" ? "" : "hidden"}>
        <label for="sample-n">Number of questions</label>
        <input id="sample-n" type="number" min="1" max="${Math.max(available, 1)}" value="${nValue}">
      </div>
      <p class="hint" id="pool-hint">${available} question${available === 1 ? "" : "s"} in the selected pool. ${state.mode === "balanced" ? `${availableMcq} multiple choice and ${availableTf} true/false are available; at least 10 of each are required.` : ""}</p>
      <button type="button" class="primary" id="start" ${available && (state.mode !== "balanced" || balancedReady) ? "" : "disabled"}>Start quiz</button>
    </div>
  `;

  app.querySelector("#select-all").addEventListener("click", () => {
    state.selected = new Set(state.bank.sections.map((section) => section.id));
    saveSession();
    render();
  });
  app.querySelector("#clear-all").addEventListener("click", () => {
    state.selected = new Set();
    saveSession();
    render();
  });
  app.querySelectorAll("[data-section]").forEach((input) => {
    input.addEventListener("change", () => {
      if (input.checked) {
        state.selected.add(input.dataset.section);
      } else {
        state.selected.delete(input.dataset.section);
      }
      saveSession();
      render();
    });
  });
  app.querySelectorAll("[data-type]").forEach((input) => {
    input.addEventListener("change", () => {
      if (input.checked) {
        state.types.add(input.dataset.type);
      } else {
        state.types.delete(input.dataset.type);
      }
      saveSession();
      render();
    });
  });
  app.querySelectorAll('input[name="mode"]').forEach((input) => {
    input.addEventListener("change", () => {
      state.mode = input.value;
      saveSession();
      render();
    });
  });
  const nInput = app.querySelector("#sample-n");
  if (nInput) {
    const applyN = () => {
      const availableNow = pool().length || 1;
      state.n = clampN(nInput.value, availableNow);
      nInput.value = String(state.n);
      saveSession();
    };
    nInput.addEventListener("change", applyN);
    nInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        applyN();
        startQuiz();
      }
    });
  }
  app.querySelector("#start").addEventListener("click", startQuiz);
}

function renderQuiz() {
  const question = state.quiz[state.index];
  const total = state.quiz.length;
  const picked = state.answers[question.id] || "";
  const width = Math.round(((state.index + 1) / total) * 100);
  const last = state.index === total - 1;
  const choices = lettersFor(question).map((letter) => `
    <button type="button" class="choice ${picked === letter ? "picked" : ""}" data-letter="${letter}">
      <span class="letter">${letter}</span>
      <span>${escapeHtml(question.choices[letter])}</span>
    </button>
  `).join("");

  app.innerHTML = `
    <p class="meta">${escapeHtml(sectionTitle(question.sectionId))} | ${escapeHtml(question.id)}</p>
    <p class="meta">Question ${state.index + 1} of ${total}</p>
    <div class="progress" aria-hidden="true"><span style="width:${width}%"></span></div>
    <div class="card">
      <p class="stem">${escapeHtml(question.stem)}</p>
      <div class="choices">${choices}</div>
    </div>
    <div class="nav">
      <button type="button" id="prev" ${state.index === 0 ? "disabled" : ""}>Previous</button>
      <button type="button" class="primary" id="next" ${picked ? "" : "disabled"}>${last ? "Submit" : "Next"}</button>
    </div>
    <p class="hint">${picked ? "" : "Choose an answer to continue."}</p>
  `;

  app.querySelectorAll("[data-letter]").forEach((button) => {
    button.addEventListener("click", () => pick(button.dataset.letter));
  });
  app.querySelector("#prev").addEventListener("click", goPrev);
  app.querySelector("#next").addEventListener("click", goNext);
}

function renderResults() {
  let correct = 0;
  const items = state.quiz.map((question) => {
    const yours = state.answers[question.id] || "";
    const ok = yours === question.answer;
    if (ok) {
      correct += 1;
    }
    const choices = lettersFor(question).map((letter) => {
      const marks = [];
      if (letter === question.answer) {
        marks.push("correct");
      }
      if (letter === yours && letter !== question.answer) {
        marks.push("your answer");
      }
      if (letter === yours && letter === question.answer) {
        marks.push("your answer");
      }
      const note = marks.length ? ` (${marks.join(", ")})` : "";
      return `<li><strong>${letter}.</strong> ${escapeHtml(question.choices[letter])}${note}</li>`;
    }).join("");
    const guideAnchor = GUIDE_ANCHORS[question.sectionId];
    const reviewLink = guideAnchor
      ? `<p><a href="guide.html#${guideAnchor}">Review this topic in the study guide</a></p>`
      : "";
    return `
      <article class="card review ${ok ? "correct" : "incorrect"}">
        <div class="badge">${ok ? "Correct" : "Incorrect"}</div>
        <p class="meta">${escapeHtml(sectionTitle(question.sectionId))} | ${escapeHtml(question.id)}</p>
        <p>${escapeHtml(question.stem)}</p>
        <ul>${choices}</ul>
        <p>Your answer: <span class="yours">${escapeHtml(shownAnswer(question, yours))}</span>. Correct answer: <span class="key">${escapeHtml(shownAnswer(question, question.answer))}</span>.</p>
        <p class="hint">${escapeHtml(question.explanation)}</p>
        ${reviewLink}
      </article>
    `;
  }).join("");

  const total = state.quiz.length;
  const percent = total ? Math.round((correct / total) * 100) : 0;

  app.innerHTML = `
    <h1>Results</h1>
    <p class="score">${correct} / ${total}</p>
    <p class="lede">${percent}% correct. ${total - correct} incorrect.</p>
    <div class="row-actions">
      <button type="button" class="primary" id="retry">Retry same set</button>
      <button type="button" id="setup">New setup</button>
    </div>
    ${items}
  `;

  app.querySelector("#retry").addEventListener("click", retrySame);
  app.querySelector("#setup").addEventListener("click", newSetup);
}

function render() {
  if (state.screen === "quiz" && state.quiz.length) {
    renderQuiz();
  } else if (state.screen === "results" && state.quiz.length) {
    renderResults();
  } else {
    state.screen = "setup";
    renderSetup();
  }
}

async function init() {
  try {
    const response = await fetch("questions.json");
    if (!response.ok) {
      throw new Error(`Could not load questions.json (${response.status})`);
    }
    state.bank = await response.json();
    restoreSession();
    render();
  } catch (err) {
    app.innerHTML = `<h1>2802ICT Study MCQs</h1><p class="error">${escapeHtml(err.message)}</p>
      <p class="hint">Open this folder through a local server or GitHub Pages. A file:// address cannot load questions.json.</p>`;
  }
}

init();
