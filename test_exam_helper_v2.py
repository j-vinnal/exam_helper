import io
import sys

import lookup_relevance


TEST_CASES = [
    # Relevance (reuse a couple of existing practice questions)
    {
        "id": "REL_Q1",
        "task": "relevance",
        "desc": "Alaska (Navigational)",
        "answers": {
            "task": "relevance",
            "qt": "locality",
            "rt": "locality",
            "exact_match": "y",
        },
        "expected": "Navigational",
    },
    {
        "id": "REL_Q3",
        "task": "relevance",
        "desc": "International Drive (Bad)",
        "answers": {
            "task": "relevance",
            "qt": "street",
            "rt": "poi",
            "same_street": "y",
        },
        "expected": "Bad",
    },
    # Name Accuracy
    {
        "id": "NAME_Q1",
        "task": "name_accuracy",
        "desc": "POI query but address-only result => Name N/A",
        "answers": {"task": "name_accuracy", "rt": "address_only"},
        "expected": "NA",
    },
    {
        "id": "NAME_Q2",
        "task": "name_accuracy",
        "desc": "Category mismatch forces Incorrect",
        "answers": {
            "task": "name_accuracy",
            "rt": "poi",
            "category_matches_entity": "n",
        },
        "expected": "Incorrect",
    },
    # Address Accuracy
    {
        "id": "ADDR_Q1",
        "task": "address_accuracy",
        "desc": "Formatting-only differences => Correct with Formatting",
        "answers": {
            "task": "address_accuracy",
            "rt": "address_only",
            "address_match": "formatting_only",
        },
        "expected": "Correct with Formatting",
    },
    # Pin Accuracy
    {
        "id": "PIN_Q1",
        "task": "pin_accuracy",
        "desc": "Does not exist => Can't Verify",
        "answers": {"task": "pin_accuracy", "location_exists": "n"},
        "expected": "Can't Verify",
    },
    {
        "id": "PIN_Q2",
        "task": "pin_accuracy",
        "desc": "Transit cannot be Next Door",
        "answers": {
            "task": "pin_accuracy",
            "location_exists": "y",
            "poi_context": "transit",
            "pin_relation": "next_door",
        },
        "expected": "Wrong",
    },
]


def run_tests() -> int:
    lookup_relevance.TEST_MODE = True

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
