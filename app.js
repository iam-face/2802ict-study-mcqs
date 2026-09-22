const STORAGE_KEY = "mcq-quiz-session";

const state = {
  bank: null,
  screen: "setup",
  selected: new Set(),
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

function pool() {
  return state.bank.questions.filter((question) => state.selected.has(question.sectionId));
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
    state.mode = saved.mode === "random" ? "random" : "all";
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

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderSetup() {
  const groups = [
    ["lecture", "Lectures"],
    ["lab", "Labs"],
    ["assignment", "Assignments"],
  ];
  const available = pool().length;
  const nValue = available ? clampN(state.n, available) : state.n;
  const groupsHtml = groups.map(([kind, label]) => {
    const items = state.bank.sections.filter((section) => section.kind === kind);
    const list = items.map((section) => {
      const count = state.bank.questions.filter((q) => q.sectionId === section.id).length;
      const checked = state.selected.has(section.id) ? "checked" : "";
      return `<li><label><input type="checkbox" data-section="${section.id}" ${checked}>
        <span>${escapeHtml(section.title)} <span class="meta">(${count})</span></span></label></li>`;
    }).join("");
    return `<h2>${label}</h2><ul class="section-list card">${list}</ul>`;
  }).join("");

  app.innerHTML = `
    <h1>2802ICT Study MCQs</h1>
    <p class="lede">Choose sections, then work through the set. Scoring happens after you submit.</p>
    <div class="row-actions">
      <button type="button" id="select-all">Select all</button>
      <button type="button" id="clear-all">Clear</button>
    </div>
    ${groupsHtml}
    <h2>Session</h2>
    <div class="card">
      <div class="mode">
        <label><input type="radio" name="mode" value="all" ${state.mode === "all" ? "checked" : ""}> All questions in the selected sections</label>
        <label><input type="radio" name="mode" value="random" ${state.mode === "random" ? "checked" : ""}> Random sample</label>
      </div>
      <div class="n-field" ${state.mode === "random" ? "" : "hidden"}>
        <label for="sample-n">Number of questions</label>
        <input id="sample-n" type="number" min="1" max="${Math.max(available, 1)}" value="${nValue}">
      </div>
      <p class="hint" id="pool-hint">${available} question${available === 1 ? "" : "s"} in the selected pool.</p>
      <button type="button" class="primary" id="start" ${available ? "" : "disabled"}>Start quiz</button>
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
  app.querySelectorAll('input[name="mode"]').forEach((input) => {
    input.addEventListener("change", () => {
      state.mode = input.value;
      saveSession();
      render();
    });
  });
  const nInput = app.querySelector("#sample-n");
  if (nInput) {
    nInput.addEventListener("change", () => {
      state.n = clampN(nInput.value, pool().length || 1);
      saveSession();
      render();
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
  const choices = ["A", "B", "C", "D"].map((letter) => `
    <button type="button" class="choice ${picked === letter ? "picked" : ""}" data-letter="${letter}">
      <span class="letter">${letter}</span>
      <span>${escapeHtml(question.choices[letter])}</span>
    </button>
  `).join("");

  app.innerHTML = `
    <p class="meta">${escapeHtml(sectionTitle(question.sectionId))} · ${escapeHtml(question.id)}</p>
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
    const choices = ["A", "B", "C", "D"].map((letter) => {
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
    return `
      <article class="card review ${ok ? "correct" : "incorrect"}">
        <div class="badge">${ok ? "Correct" : "Incorrect"}</div>
        <p class="meta">${escapeHtml(sectionTitle(question.sectionId))} · ${escapeHtml(question.id)}</p>
        <p>${escapeHtml(question.stem)}</p>
        <ul>${choices}</ul>
        <p>Your answer: <span class="yours">${yours || "none"}</span>. Correct answer: <span class="key">${question.answer}</span>.</p>
        <p class="hint">${escapeHtml(question.explanation)}</p>
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
