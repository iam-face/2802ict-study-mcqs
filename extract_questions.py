"""Extract Study MCQs.md and Study TF.md into questions.json for the static quiz site."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "Study MCQs.md"
TF_SOURCE = ROOT.parent / "Study TF.md"
GUIDE_SOURCE = ROOT.parent / "Study Guide.md"
GUIDE_OUTPUT = ROOT / "study-guide.md"
OUTPUT = ROOT / "questions.json"

# Section ids in source order. Titles fill from ## headers when present.
SECTION_META = [
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
    ("Lab5", "Lab 5: Learning paradigms and energy regression", "lab"),
    ("Lab6", "Lab Week 6", "lab"),
    ("Lab7", "Lab Week 7", "lab"),
    ("Lab8", "Lab Week 8", "lab"),
    ("Lab9", "Lab Week 9", "lab"),
    ("A1", "Assignment 1", "assignment"),
    ("A2", "Assignment 2", "assignment"),
    ("EX", "Final exam drill", "exam"),
]

Q_HEAD = re.compile(r"^### ([A-Za-z0-9]+-Q\d+)\s*$")
T_HEAD = re.compile(r"^### ([A-Za-z0-9]+-T\d+)\s*$")
EX_T_HEAD = re.compile(r"^### (EX-T\d+)\s*$")
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
        if kind == "exam":
            continue
        count = per_section.get(sid, 0)
        if count != 10:
            raise SystemExit(f"{sid} has {count} true/false items, expected 10")
        trues, falses = balance[sid]
        if trues != 5 or falses != 5:
            raise SystemExit(f"{sid} true/false balance is {trues} true and {falses} false")
    return questions


def parse_exam_tf(text: str) -> list[dict]:
    """True/false items for the exam drill live in Study MCQs.md, not Study TF.md."""
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
            current = {
                "id": qid,
                "sectionId": "EX",
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
        if not match or not match.group(1).startswith("EX-"):
            continue
        answers[match.group(1)] = (match.group(2), match.group(3).strip())

    if len(questions) != 20:
        raise SystemExit(f"Exam drill has {len(questions)} true/false items, expected 20")

    for question in questions:
        found = answers.get(question["id"])
        if not found:
            raise SystemExit(f"No appendix answer for {question['id']}")
        question["answer"] = found[0]
        question["explanation"] = found[1]

    extra = set(answers) - {q["id"] for q in questions}
    if extra:
        raise SystemExit(f"Exam true/false answers without questions: {sorted(extra)}")

    trues = sum(1 for question in questions if question["answer"] == "T")
    if trues != 10:
        raise SystemExit(f"Exam true/false balance is {trues} true and {20 - trues} false")
    return questions


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    data = parse(source_text)
    tf_questions = parse_tf(TF_SOURCE.read_text(encoding="utf-8"))
    exam_tf = parse_exam_tf(source_text)
    mcq_ids = {question["id"] for question in data["questions"]}
    overlap = mcq_ids & {question["id"] for question in tf_questions}
    overlap |= mcq_ids & {question["id"] for question in exam_tf}
    overlap |= {question["id"] for question in tf_questions} & {question["id"] for question in exam_tf}
    if overlap:
        raise SystemExit(f"Duplicate ids: {sorted(overlap)}")
    data["questions"].extend(tf_questions)
    data["questions"].extend(exam_tf)
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    counts: dict[str, list[int]] = {}
    for question in data["questions"]:
        tally = counts.setdefault(question["sectionId"], [0, 0])
        tally[0 if question["type"] == "mcq" else 1] += 1
    shutil.copyfile(GUIDE_SOURCE, GUIDE_OUTPUT)
    print(f"Wrote {len(data['questions'])} questions to {OUTPUT}")
    print(f"Copied study guide to {GUIDE_OUTPUT}")
    for section in data["sections"]:
        mcq, tf = counts.get(section["id"], [0, 0])
        print(f"  {section['id']}: {mcq} mcq, {tf} tf  {section['title']}")


if __name__ == "__main__":
    main()
