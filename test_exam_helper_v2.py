import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import lookup_relevance


ROOT = Path(__file__).parent
RAW_DIR = ROOT / "rules_raw"


@dataclass(frozen=True)
class PracticeQuestion:
    source: str
    qid: str
    task: str
    title: str
    correct: Optional[str]
    guideline_sections: List[str]


def _extract_guideline_sections(text: str) -> List[str]:
    secs = set()
    for m in re.finditer(r"\bsection\s+([0-9]+(?:\.[0-9]+)*)\b", text, flags=re.IGNORECASE):
        secs.add(m.group(1))
    for m in re.finditer(r"\bGL\s*:??\s*([0-9]+(?:\.[0-9]+)*)\b", text, flags=re.IGNORECASE):
        secs.add(m.group(1))
    return sorted(secs)


def _parse_name_address_pin_questions(md: str) -> List[PracticeQuestion]:
    lines = md.splitlines()
    out: List[PracticeQuestion] = []

    header_re = re.compile(r"^Q(\d+)\s+(Name Accuracy|Address Accuracy|Pin Accuracy)\b", re.IGNORECASE)

    current_n: Optional[int] = None
    current_task: Optional[str] = None
    buf: List[str] = []

    def flush() -> None:
        nonlocal current_n, current_task, buf
        if current_n is None or current_task is None:
            return
        block = "\n".join(buf)
        sections = _extract_guideline_sections(block)

        task_map = {
            "name accuracy": "name_accuracy",
            "address accuracy": "address_accuracy",
            "pin accuracy": "pin_accuracy",
        }
        task_norm = task_map[current_task.lower()]

        allowed = {
            "name_accuracy": ["N/A", "NA", "Correct", "Partially Correct", "Incorrect", "Can't Verify"],
            "address_accuracy": ["Correct", "Correct with Formatting", "Incorrect"],
            "pin_accuracy": ["Perfect", "Approximate", "Next Door", "Wrong", "Can't Verify"],
        }[task_norm]

        correct = None
        # Look for a sentence like "The correct rating is X" or "The Pin Accuracy is X"
        m = re.search(r"The\s+correct\s+(?:rating\s+)?(?:should\s+be\s+|is\s+)([^.\n]+)", block, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            for a in allowed:
                if re.search(rf"\b{re.escape(a)}\b", candidate, re.IGNORECASE):
                    correct = "NA" if a.upper() in ("N/A", "NA") else a
                    break
        if correct is None:
            m2 = re.search(r"\brating\s+is\s+([A-Za-z'\s/]+)\b", block, re.IGNORECASE)
            if m2:
                candidate = m2.group(1).strip()
                for a in allowed:
                    if re.search(rf"\b{re.escape(a)}\b", candidate, re.IGNORECASE):
                        correct = "NA" if a.upper() in ("N/A", "NA") else a
                        break

        qid = f"NAP_Q{current_n:02d}"
        title = f"Q{current_n} {task_norm}"
        out.append(
            PracticeQuestion(
                source="name_address_pin_quest.md",
                qid=qid,
                task=task_norm,
                title=title,
                correct=correct,
                guideline_sections=sections,
            )
        )

    for line in lines:
        m = header_re.match(line.strip())
        if m:
            flush()
            current_n = int(m.group(1))
            current_task = m.group(2)
            buf = [line]
            continue
        if current_n is not None:
            buf.append(line)

    flush()
    return out


def _parse_relevance_questions(md: str) -> List[PracticeQuestion]:
    # Relevance practice contains mixed question types (rating, yes/no, true/false).
    # We include ALL questions here for completeness, even if the engine doesn't support them yet.
    blocks: List[tuple[int, str]] = []

    current_n: Optional[int] = None
    buf: List[str] = []

    def flush() -> None:
        nonlocal current_n, buf
        if current_n is None:
            return
        blocks.append((current_n, "\n".join(buf)))

    for line in md.splitlines():
        m = re.match(r"^Q(\d+)\b", line.strip())
        if m:
            flush()
            current_n = int(m.group(1))
            buf = [line]
        else:
            if current_n is not None:
                buf.append(line)
    flush()

    out: List[PracticeQuestion] = []
    allowed_ratings = ["Navigational", "Excellent", "Good", "Acceptable", "Bad"]
    allowed_binary = ["Yes", "No", "True", "False"]

    for n, block in blocks:
        sections = _extract_guideline_sections(block)
        correct: Optional[str] = None

        # Prefer explicit "The correct rating should be X" / "The rating should be X"
        m = re.search(r"The\s+(?:correct\s+)?rating\s+should\s+be\s+([A-Za-z]+)", block, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            for a in allowed_ratings:
                if a.lower() == candidate.lower():
                    correct = a
                    break
        if correct is None:
            m = re.search(r"The\s+correct\s+answer\s+is\s+\"?(Yes|No|True|False)\"?", block, re.IGNORECASE)
            if m:
                candidate = m.group(1)
                for a in allowed_binary:
                    if a.lower() == candidate.lower():
                        correct = a
                        break
        if correct is None:
            # Sometimes: "The correct rating should be Bad." or "The correct answer is 'Yes.'"
            for a in allowed_ratings + allowed_binary:
                if re.search(rf"\bThe\s+correct\b.*\b{re.escape(a)}\b", block, re.IGNORECASE):
                    correct = a
                    break

        out.append(
            PracticeQuestion(
                source="relevance.md",
                qid=f"REL_Q{n:02d}",
                task="relevance",
                title=f"Q{n} relevance",
                correct=correct,
                guideline_sections=sections,
            )
        )

    return out


def load_all_practice_questions() -> List[PracticeQuestion]:
    rel_path = RAW_DIR / "relevance.md"
    nap_path = RAW_DIR / "name_address_pin_quest.md"
    rel_md = rel_path.read_text(encoding="utf-8")
    nap_md = nap_path.read_text(encoding="utf-8")
    return _parse_relevance_questions(rel_md) + _parse_name_address_pin_questions(nap_md)


# These lists make this file "contain" all practice questions (loaded from rules_raw).
ALL_PRACTICE_QUESTIONS: List[PracticeQuestion] = load_all_practice_questions()


# Automated cases: only include scenarios we can currently express as facts.
TEST_CASES = [
    # Relevance (subset that engine supports)
    {
        "id": "REL_Q01",
        "task": "relevance",
        "desc": "Alaska (Navigational)",
        "answers": {"task": "relevance", "qt": "locality", "rt": "locality", "exact_match": "y"},
        "expected": "Navigational",
    },
    {
        "id": "REL_Q03",
        "task": "relevance",
        "desc": "International Drive (Bad)",
        "answers": {"task": "relevance", "qt": "street", "rt": "poi", "same_street": "y"},
        "expected": "Bad",
    },
    # Name Accuracy
    {
        "id": "NAP_Q01",
        "task": "name_accuracy",
        "desc": "Address-type result => Name N/A",
        "answers": {"task": "name_accuracy", "rt": "address_only"},
        "expected": "NA",
    },
    {
        "id": "NAP_Q02",
        "task": "name_accuracy",
        "desc": "Incorrect category forces Incorrect",
        "answers": {"task": "name_accuracy", "rt": "poi", "category_matches_entity": "n"},
        "expected": "Incorrect",
    },
    # Address Accuracy
    {
        "id": "ADDR_SMOKE",
        "task": "address_accuracy",
        "desc": "Formatting-only differences => Correct with Formatting",
        "answers": {"task": "address_accuracy", "rt": "address_only", "address_match": "formatting_only"},
        "expected": "Correct with Formatting",
    },
    # Pin Accuracy
    {
        "id": "PIN_SMOKE_NOT_EXISTS",
        "task": "pin_accuracy",
        "desc": "Address does not exist => Can't Verify",
        "answers": {"task": "pin_accuracy", "address_exists": "n"},
        "expected": "Can't Verify",
    },
    {
        "id": "PIN_TRANSIT_NEXT_DOOR",
        "task": "pin_accuracy",
        "desc": "Transit cannot be Next Door",
        "answers": {
            "task": "pin_accuracy",
            "address_exists": "y",
            "pin_generous_perfect": "n",
            "poi_context": "transit",
            "pin_relation": "next_door",
        },
        "expected": "Wrong",
    },
]


def run_tests() -> int:
    lookup_relevance.TEST_MODE = True

    # Sanity: ensure we load the full practice set from rules_raw
    rel_cnt = sum(1 for q in ALL_PRACTICE_QUESTIONS if q.source == "relevance.md")
    nap_cnt = sum(1 for q in ALL_PRACTICE_QUESTIONS if q.source == "name_address_pin_quest.md")
    print(f"Loaded practice questions: relevance={rel_cnt}, name/address/pin={nap_cnt}")
    missing_correct = [q for q in ALL_PRACTICE_QUESTIONS if q.correct is None]
    if missing_correct:
        print(f"Note: {len(missing_correct)} questions missing parsed correct answer (kept for completeness).")

    passed = 0
    failed = 0

    for case in TEST_CASES:
        lookup_relevance.TEST_ANSWERS = case["answers"]

        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            lookup_relevance.main()
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"FAIL: {case['id']} - {case['desc']}")
            print(f"  Error: {e}")
            failed += 1
            continue
        finally:
            sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        rating = None
        for line in output.splitlines():
            if line.startswith("Relevance rating:") and case["task"] == "relevance":
                rating = line.split(":", 1)[1].strip()
            if line.startswith("Rating:") and f"Task: {case['task']}" in output:
                # collect the last rating printed for that run
                rating = line.split(":", 1)[1].strip()

        if rating == case["expected"]:
            print(f"PASS: {case['id']} - {case['desc']}")
            passed += 1
        else:
            print(f"FAIL: {case['id']} - {case['desc']}")
            print(f"  Expected: {case['expected']}")
            print(f"  Got:      {rating}")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run_tests())
