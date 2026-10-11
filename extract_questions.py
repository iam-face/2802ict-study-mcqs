"""Extract Study MCQs.md and Study TF.md into questions.json for the static quiz site."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "Study MCQs.md"
TF_SOURCE = ROOT.parent / "Study TF.md"
APPLIED_SOURCE = ROOT.parent / "Study Applied.md"
OUTPUT = ROOT / "questions.json"

# Section ids in source order. Titles fill from ## headers when present.
SECTION_META = [
    ("RED", "Highlighted items", "red"),
    ("L1", "Lecture 1: Introduction", "lecture"),
    ("L2", "Lecture 2: Uninformed Search", "lecture"),
    ("L3", "Lecture 3: Informed Search", "lecture"),
    ("L4A", "Lecture 4 Part 1: Local Search", "lecture"),
    ("L4B", "Lecture 4 Part 2: CSP", "lecture"),
    ("L5", "Lecture 5: ML Basics", "lecture"),
    ("L6", "Lecture 6: Linear Models", "lecture"),
    ("L7", "Lecture 7: Feed-forward NNs", "lecture"),
    ("L8", "Lecture 8: Model selection", "lecture"),
    ("L9", "Lecture 9: Decision trees", "lecture"),
    ("L10", "Lecture 10: Bayes nets", "lecture"),
    ("L11", "Lecture 11: MDP and reinforcement learning", "lecture"),
    ("Lab2", "Lab Week 2: Uninformed search traces", "lab"),
    ("Lab3A", "Lab Week 3.1: Search strategies and heuristics", "lab"),
    ("Lab3B", "Lab Week 3.2: Heuristic design for the 8-puzzle", "lab"),
    ("Lab4", "Lab Week 4: Constraint satisfaction problems", "lab"),
    ("Lab5", "Lab 5: Learning paradigms and energy regression", "lab"),
    ("Lab6", "Lab Week 6", "lab"),
    ("Lab7", "Lab Week 7", "lab"),
    ("Lab8", "Lab Week 8", "lab"),
    ("Lab9", "Lab Week 9", "lab"),
    ("Lab10", "Lab Week 10: Bayesian networks", "lab"),
    ("Lab11", "Workshop Week 11: Q-learning", "lab"),
    ("A1", "Assignment 1", "assignment"),
    ("A2", "Assignment 2", "assignment"),
    ("EX", "Final exam drill 1 (extended)", "exam"),
    ("EX2", "Final exam drill 2", "exam"),
    ("EX3", "Final exam drill 3", "exam"),
    ("EX4", "Final exam drill 4", "exam"),
    ("EX5", "Final exam drill 5", "exam"),
    ("APL1", "Applied: Lecture 1 Agents", "applied"),
    ("APL2", "Applied: Lecture 2 Uninformed search", "applied"),
    ("APL3", "Applied: Lecture 3 Informed search", "applied"),
    ("APL4A", "Applied: Lecture 4 Local search", "applied"),
    ("APL4B", "Applied: Lecture 4 CSPs", "applied"),
    ("APL5", "Applied: Lecture 5 Learning", "applied"),
    ("APL6", "Applied: Lecture 6 Linear models", "applied"),
    ("APL7", "Applied: Lecture 7 Neural networks", "applied"),
    ("APL8", "Applied: Lecture 8 Model selection", "applied"),
    ("APL9", "Applied: Lecture 9 Decision trees", "applied"),
    ("APL10", "Applied: Lecture 10 Bayes nets", "applied"),
    ("APL11", "Applied: Lecture 11 MDPs and RL", "applied"),
    ("AP2", "Applied: Lab 2 Search traces", "applied"),
    ("AP3A", "Applied: Lab 3.1 Weighted search", "applied"),
    ("AP3B", "Applied: Lab 3.2 Puzzle heuristics", "applied"),
    ("AP4", "Applied: Lab 4 CSPs", "applied"),
    ("AP5", "Applied: Lab 5 Learning and regression", "applied"),
    ("AP6", "Applied: Lab 6 Linear models", "applied"),
    ("AP7", "Applied: Lab 7 Multilayer network", "applied"),
    ("AP8", "Applied: Lab 8 XOR network", "applied"),
    ("AP9", "Applied: Lab 9 Decision trees", "applied"),
    ("AP10", "Applied: Lab 10 Bayes nets", "applied"),
    ("AP11", "Applied: Workshop 11 Q-learning", "applied"),
]

Q_HEAD = re.compile(r"^### ([A-Za-z0-9]+-Q\d+)((?:\s+(?:red|blue))*)\s*$")
T_HEAD = re.compile(r"^### ([A-Za-z0-9]+-T\d+)((?:\s+(?:red|blue))*)\s*$")
EX_T_HEAD = re.compile(r"^### (EX(?:[2-5])?-T\d+)\s*$")
CHOICE = re.compile(r"^([A-D])\.\s+(.*)$")
ANSWER = re.compile(r"^\*\*([A-Za-z0-9]+-Q\d+):\*\*\s+([A-D])\.\s+(.*)$")
TF_ANSWER = re.compile(r"^\*\*([A-Za-z0-9]+-T\d+):\*\*\s+([TF])\.\s+(.*)$")
SECTION_HEAD = re.compile(r"^## (.+)$")


def section_id_from_qid(qid: str) -> str:
    return re.split(r"-[QT]", qid, maxsplit=1)[0]


def parse(text: str) -> dict:
    body, _, appendix = text.partition("# Appendix: Answers")
    if not appendix:
        raise SystemExit("Appendix heading not found")

    titles: dict[str, str] = {sid: title for sid, title, _ in SECTION_META}
    pending_title: str | None = None

    questions: list[dict] = []
    current: dict | None = None
    choice_letter: str | None = None
    skipping = False

    def flush() -> None:
        nonlocal current, choice_letter
        if current is None:
            return
        missing = [letter for letter in "ABCD" if not current["choices"].get(letter)]
        if missing:
            raise SystemExit(f"{current['id']} missing choices {missing}")
        if not current["stem"].strip():
            raise SystemExit(f"{current['id']} has empty stem")
        questions.append(current)
        current = None
        choice_letter = None

    for raw in body.splitlines():
        line = raw.rstrip()
        head = Q_HEAD.match(line)
        if head:
            skipping = False
            flush()
            qid = head.group(1)
            sid = section_id_from_qid(qid)
            if sid not in titles:
                raise SystemExit(f"Unknown section id {sid} from {qid}")
            if pending_title:
                titles[sid] = pending_title
                pending_title = None
            current = {
                "id": qid,
                "sectionId": sid,
                "type": "mcq",
                "stem": "",
                "choices": {"A": "", "B": "", "C": "", "D": ""},
            }
            tags = re.findall(r"red|blue", head.group(2))
            if tags:
                current["tags"] = tags
            choice_letter = None
            continue

        if line.startswith("### "):
            # True/false and short-response blocks share this file. They are not MCQs.
            flush()
            skipping = True
            continue

        sec = SECTION_HEAD.match(line)
        if sec and not line.startswith("###"):
            pending_title = sec.group(1).strip()
            skipping = False
            continue

        if skipping or current is None or not line.strip() or line.strip() == "---":
            continue

        choice = CHOICE.match(line.strip())
        if choice:
            choice_letter = choice.group(1)
            current["choices"][choice_letter] = choice.group(2).strip()
            continue

        if choice_letter:
            current["choices"][choice_letter] += " " + line.strip()
        else:
            stem = current["stem"]
            current["stem"] = (stem + " " + line.strip()).strip() if stem else line.strip()

    flush()

    answers: dict[str, tuple[str, str]] = {}
    for raw in appendix.splitlines():
        match = ANSWER.match(raw.strip())
        if not match:
            continue
        qid, letter, explanation = match.group(1), match.group(2), match.group(3).strip()
        answers[qid] = (letter, explanation)

    for question in questions:
        found = answers.get(question["id"])
        if not found:
            raise SystemExit(f"No appendix answer for {question['id']}")
        question["answer"] = found[0]
        question["explanation"] = found[1]

    extra = set(answers) - {q["id"] for q in questions}
    if extra:
        raise SystemExit(f"Appendix answers without questions: {sorted(extra)}")

    sections = [
        {"id": sid, "title": titles[sid], "kind": kind}
        for sid, _, kind in SECTION_META
    ]
    return {"sections": sections, "questions": questions}


def parse_tf(text: str) -> list[dict]:
    body, _, appendix = text.partition("# Appendix: Answers")
    if not appendix:
        raise SystemExit("True/false appendix heading not found")

    known = {sid for sid, _, _ in SECTION_META}
    questions: list[dict] = []
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        if not current["stem"].strip():
            raise SystemExit(f"{current['id']} has empty stem")
        questions.append(current)
        current = None

    for raw in body.splitlines():
        line = raw.rstrip()
        head = T_HEAD.match(line)
        if head:
            flush()
            qid = head.group(1)
            sid = section_id_from_qid(qid)
            if sid not in known:
                raise SystemExit(f"Unknown section id {sid} from {qid}")
            current = {
                "id": qid,
                "sectionId": sid,
                "type": "tf",
                "stem": "",
                "choices": {"T": "True", "F": "False"},
            }
            tags = re.findall(r"red|blue", head.group(2))
            if tags:
                current["tags"] = tags
            continue
        if current is None or not line.strip() or line.startswith("#") or line.strip() == "---":
            continue
        stem = current["stem"]
        current["stem"] = (stem + " " + line.strip()).strip() if stem else line.strip()

    flush()

    answers: dict[str, tuple[str, str]] = {}
    for raw in appendix.splitlines():
        match = TF_ANSWER.match(raw.strip())
        if not match:
            continue
        answers[match.group(1)] = (match.group(2), match.group(3).strip())

    for question in questions:
        found = answers.get(question["id"])
        if not found:
            raise SystemExit(f"No appendix answer for {question['id']}")
        question["answer"] = found[0]
        question["explanation"] = found[1]

    extra = set(answers) - {q["id"] for q in questions}
    if extra:
        raise SystemExit(f"True/false answers without questions: {sorted(extra)}")

    per_section: dict[str, int] = {}
    balance: dict[str, list[int]] = {}
    for question in questions:
        per_section[question["sectionId"]] = per_section.get(question["sectionId"], 0) + 1
        tally = balance.setdefault(question["sectionId"], [0, 0])
        tally[0 if question["answer"] == "T" else 1] += 1
    for sid, _, kind in SECTION_META:
        if kind in ("exam", "red", "applied"):
            continue
        count = per_section.get(sid, 0)
        if count != 10:
            raise SystemExit(f"{sid} has {count} true/false items, expected 10")
        trues, falses = balance[sid]
        if trues != 5 or falses != 5:
            raise SystemExit(f"{sid} true/false balance is {trues} true and {falses} false")
    return questions


def parse_exam_tf(text: str) -> list[dict]:
    """True/false items for exam drills live in Study MCQs.md, not Study TF.md."""
    body, _, appendix = text.partition("# Appendix: Answers")
    if not appendix:
        raise SystemExit("Appendix heading not found")

    questions: list[dict] = []
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        if not current["stem"].strip():
            raise SystemExit(f"{current['id']} has empty stem")
        questions.append(current)
        current = None

    for raw in body.splitlines():
        line = raw.rstrip()
        head = EX_T_HEAD.match(line)
        if head:
            flush()
            qid = head.group(1)
            sid = section_id_from_qid(qid)
            current = {
                "id": qid,
                "sectionId": sid,
                "type": "tf",
                "stem": "",
                "choices": {"T": "True", "F": "False"},
            }
            continue
        if current is None or not line.strip() or line.startswith("#") or line.strip() == "---":
            if current is not None and (line.startswith("#") or line.strip() == "---"):
                flush()
            continue
        stem = current["stem"]
        current["stem"] = (stem + " " + line.strip()).strip() if stem else line.strip()

    flush()

    answers: dict[str, tuple[str, str]] = {}
    for raw in appendix.splitlines():
        match = TF_ANSWER.match(raw.strip())
        if not match or not re.match(r"^EX(?:[2-5])?-T", match.group(1)):
            continue
        answers[match.group(1)] = (match.group(2), match.group(3).strip())

    for question in questions:
        found = answers.get(question["id"])
        if not found:
            raise SystemExit(f"No appendix answer for {question['id']}")
        question["answer"] = found[0]
        question["explanation"] = found[1]

    extra = set(answers) - {q["id"] for q in questions}
    if extra:
        raise SystemExit(f"Exam true/false answers without questions: {sorted(extra)}")

    expected = {"EX": 22, "EX2": 10, "EX3": 10, "EX4": 10, "EX5": 10}
    for sid, expected_count in expected.items():
        section_questions = [question for question in questions if question["sectionId"] == sid]
        if len(section_questions) != expected_count:
            raise SystemExit(
                f"{sid} has {len(section_questions)} true/false items, expected {expected_count}"
            )
        trues = sum(question["answer"] == "T" for question in section_questions)
        # Drills 2 to 5 use 4 true and 6 false so a paper is not a list of true definitions.
        expected_true = 11 if sid == "EX" else 4
        if trues != expected_true:
            raise SystemExit(
                f"{sid} true/false balance is {trues} true and "
                f"{expected_count - trues} false"
            )
    return questions


def parse_applied_tf(text: str) -> list[dict]:
    """Applied true/false items live in Study Applied.md beside the applied MCQs."""
    body, _, appendix = text.partition("# Appendix: Answers")
    if not appendix:
        raise SystemExit("Applied appendix heading not found")

    applied_ids = {sid for sid, _, kind in SECTION_META if kind == "applied"}
    questions: list[dict] = []
    current: dict | None = None

    def flush() -> None:
        nonlocal current
        if current is None:
            return
        if not current["stem"].strip():
            raise SystemExit(f"{current['id']} has empty stem")
        questions.append(current)
        current = None

    for raw in body.splitlines():
        line = raw.rstrip()
        head = T_HEAD.match(line)
        if head:
            flush()
            qid = head.group(1)
            sid = section_id_from_qid(qid)
            if sid not in applied_ids:
                raise SystemExit(f"Unexpected applied true/false id {qid}")
            current = {
                "id": qid,
                "sectionId": sid,
                "type": "tf",
                "stem": "",
                "choices": {"T": "True", "F": "False"},
            }
            continue
        if current is None or not line.strip() or line.startswith("#") or line.strip() == "---":
            if current is not None and (line.startswith("#") or line.strip() == "---"):
                flush()
            continue
        stem = current["stem"]
        current["stem"] = (stem + " " + line.strip()).strip() if stem else line.strip()

    flush()

    answers: dict[str, tuple[str, str]] = {}
    for raw in appendix.splitlines():
        match = TF_ANSWER.match(raw.strip())
        if not match:
            continue
        sid = section_id_from_qid(match.group(1))
        if sid not in applied_ids:
            continue
        answers[match.group(1)] = (match.group(2), match.group(3).strip())

    for question in questions:
        found = answers.get(question["id"])
        if not found:
            raise SystemExit(f"No appendix answer for {question['id']}")
        question["answer"] = found[0]
        question["explanation"] = found[1]

    extra = set(answers) - {q["id"] for q in questions}
    if extra:
        raise SystemExit(f"Applied true/false answers without questions: {sorted(extra)}")
    return questions


def check_applied(questions: list[dict]) -> None:
    lecture = {sid for sid, _, kind in SECTION_META if kind == "applied" and sid.startswith("APL")}
    expected = {}
    for sid, _, kind in SECTION_META:
        if kind != "applied":
            continue
        if sid in lecture:
            expected[sid] = (8, 6, 3)
        else:
            expected[sid] = (6, 4, 2)
    by_section: dict[str, list[dict]] = {}
    for question in questions:
        by_section.setdefault(question["sectionId"], []).append(question)
    for sid, (mcq_n, tf_n, true_n) in expected.items():
        items = by_section.get(sid, [])
        mcq = [q for q in items if q["type"] == "mcq"]
        tf = [q for q in items if q["type"] == "tf"]
        if len(mcq) != mcq_n or len(tf) != tf_n:
            raise SystemExit(f"{sid} has {len(mcq)} mcq and {len(tf)} tf, expected {mcq_n} and {tf_n}")
        trues = sum(q["answer"] == "T" for q in tf)
        if trues != true_n:
            raise SystemExit(f"{sid} true/false balance is {trues} true, expected {true_n}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    data = parse(source_text)
    tf_questions = parse_tf(TF_SOURCE.read_text(encoding="utf-8"))
    exam_tf = parse_exam_tf(source_text)
    applied_text = APPLIED_SOURCE.read_text(encoding="utf-8")
    applied_mcq = parse(applied_text)["questions"]
    applied_tf = parse_applied_tf(applied_text)
    check_applied(applied_mcq + applied_tf)
    mcq_ids = {question["id"] for question in data["questions"]}
    overlap = mcq_ids & {question["id"] for question in tf_questions}
    overlap |= mcq_ids & {question["id"] for question in exam_tf}
    overlap |= {question["id"] for question in tf_questions} & {question["id"] for question in exam_tf}
    applied_ids = {question["id"] for question in applied_mcq} | {question["id"] for question in applied_tf}
    overlap |= applied_ids & (mcq_ids | {question["id"] for question in tf_questions} | {question["id"] for question in exam_tf})
    overlap |= {question["id"] for question in applied_mcq} & {question["id"] for question in applied_tf}
    if overlap:
        raise SystemExit(f"Duplicate ids: {sorted(overlap)}")
    data["questions"].extend(tf_questions)
    data["questions"].extend(exam_tf)
    data["questions"].extend(applied_mcq)
    data["questions"].extend(applied_tf)
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    counts: dict[str, list[int]] = {}
    for question in data["questions"]:
        tally = counts.setdefault(question["sectionId"], [0, 0])
        tally[0 if question["type"] == "mcq" else 1] += 1
    highlighted = sum(
        1
        for question in data["questions"]
        if "red" in question.get("tags", []) or "blue" in question.get("tags", [])
    )
    print(f"Wrote {len(data['questions'])} questions to {OUTPUT} ({highlighted} highlighted)")
    for section in data["sections"]:
        mcq, tf = counts.get(section["id"], [0, 0])
        print(f"  {section['id']}: {mcq} mcq, {tf} tf  {section['title']}")


if __name__ == "__main__":
    main()
