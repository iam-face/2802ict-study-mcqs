"""Extract Study MCQs.md into questions.json for the static quiz site."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "Study MCQs.md"
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
]

Q_HEAD = re.compile(r"^### ([A-Za-z0-9]+-Q\d+)\s*$")
CHOICE = re.compile(r"^([A-D])\.\s+(.*)$")
ANSWER = re.compile(r"^\*\*([A-Za-z0-9]+-Q\d+):\*\*\s+([A-D])\.\s+(.*)$")
SECTION_HEAD = re.compile(r"^## (.+)$")


def section_id_from_qid(qid: str) -> str:
    return qid.rsplit("-Q", 1)[0]


def parse(text: str) -> dict:
    body, _, appendix = text.partition("# Appendix: Answers")
    if not appendix:
        raise SystemExit("Appendix heading not found")

    titles: dict[str, str] = {sid: title for sid, title, _ in SECTION_META}
    pending_title: str | None = None

    questions: list[dict] = []
    current: dict | None = None
    choice_letter: str | None = None

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
                "stem": "",
                "choices": {"A": "", "B": "", "C": "", "D": ""},
            }
            choice_letter = None
            continue

        sec = SECTION_HEAD.match(line)
        if sec and not line.startswith("###"):
            pending_title = sec.group(1).strip()
            continue

        if current is None or not line.strip() or line.strip() == "---":
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


def main() -> None:
    data = parse(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    counts: dict[str, int] = {}
    for question in data["questions"]:
        counts[question["sectionId"]] = counts.get(question["sectionId"], 0) + 1
    print(f"Wrote {len(data['questions'])} questions to {OUTPUT}")
    for section in data["sections"]:
        print(f"  {section['id']}: {counts.get(section['id'], 0)}  {section['title']}")


if __name__ == "__main__":
    main()
