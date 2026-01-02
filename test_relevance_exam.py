import sys
import io
import lookup_relevance

# Define test cases based on relevance.md
TEST_CASES = [
    {
        "id": "Q1",
        "desc": "Alaska (Navigational)",
        "answers": {
            "Query type": "locality",
            "Result type": "locality",
            "exact name match": "y",
        },
        "expected": "Navigational",
    },
    {
        "id": "Q2",
        "desc": "Sugarloaf Key St (Acceptable)",
        "answers": {
            "Query type": "full_addr",
            "Result type": "street",
            "same street": "y",
        },
        "expected": "Acceptable",
    },
    {
        "id": "Q3",
        "desc": "International Drive (Bad)",
        "answers": {"Query type": "street", "Result type": "poi", "same street": "y"},
        "expected": "Bad",
    },
    {
        "id": "Q4",
        "desc": "Menlo Park Mall (Bad)",
        "answers": {"Query type": "category_mall", "Result type": "store_in_mall"},
        "expected": "Bad",
    },
    {
        "id": "Q6",
        "desc": "Sam's Club (Bad)",
        "answers": {"Query type": "chain_plain", "Result type": "dept"},
        "expected": "Bad",
    },
    {
        "id": "Q7",
        "desc": "Met Museum (Bad)",
        "answers": {"Query type": "poi_name", "Result type": "address_only"},
        "expected": "Bad",
    },
    {
        "id": "Q8",
        "desc": "Orlando (Good)",
        "answers": {"Query type": "locality", "Result type": "airport"},
        "expected": "Good",
    },
    {
        "id": "Q9",
        "desc": "Fremont Station (Navigational)",
        "answers": {
            "Query type": "transit",
            "Result type": "station",
            "exact name match": "y",
        },
        "expected": "Navigational",
    },
    {
        "id": "Q10",
        "desc": "Fremont Station - Other (Excellent)",
        "answers": {
            "Query type": "transit",
            "Result type": "station",
            "exact name match": "n",
            "queried locality": "y",
        },
        "expected": "Excellent",
    },
    {
        "id": "Q11",
        "desc": "Starbucks Inside FVP (Excellent)",
        "answers": {
            "Query type": "chain_plain",
            "Result type": "poi",
            "Viewport age": "fresh",
            "User in viewport": "out",
            "distance tier": "closest",
        },
        "expected": "Excellent",
    },
    {
        "id": "Q12",
        "desc": "Starbucks Outside FVP (Good)",
        "answers": {
            "Query type": "chain_plain",
            "Result type": "poi",
            "Viewport age": "fresh",
            "User in viewport": "out",
            "distance tier": "second",
        },
        "expected": "Good",
    },
    {
        "id": "Q13",
        "desc": "Wegmans Far (Bad)",
        "answers": {
            "Query type": "chain_city",
            "Result type": "poi",
            "result inside the requested": "n",
            "how many open/exists branches": "1",
            "how close is it": "far",
        },
        "expected": "Bad",
    },
    {
        "id": "Q14",
        "desc": "Wegmans Adjacent (Good)",
        "answers": {
            "Query type": "chain_city",
            "Result type": "poi",
            "result inside the requested": "n",
            "how many open/exists branches": "1",
            "how close is it": "adjacent",
        },
        "expected": "Good",
    },
    {
        "id": "Q15",
        "desc": "Applebee's Closest (Excellent)",
        "answers": {
            "Query type": "chain_plain",
            "Result type": "poi",
            "Viewport age": "fresh",
            "User in viewport": "in",
            "distance tier": "closest",
        },
        "expected": "Excellent",
    },
    {
        "id": "Q16",
        "desc": "Applebee's 1 Closer (Good)",
        "answers": {
            "Query type": "chain_plain",
            "Result type": "poi",
            "Viewport age": "fresh",
            "User in viewport": "in",
            "distance tier": "second",
        },
        "expected": "Good",
    },
    {
        "id": "Q17",
        "desc": "Applebee's 1 Much Closer (Good)",
        "answers": {
            "Query type": "chain_plain",
            "Result type": "poi",
            "Viewport age": "fresh",
            "User in viewport": "in",
            "distance tier": "second",
        },
        "expected": "Good",
    },
    {
        "id": "Q18",
        "desc": "Applebee's 3 Closer (Acceptable)",
        "answers": {
            "Query type": "chain_plain",
            "Result type": "poi",
            "Viewport age": "fresh",
            "User in viewport": "in",
            "distance tier": "third",
        },
        "expected": "Acceptable",
    },
    {
        "id": "Q19",
        "desc": "Marshalls Tavern (Excellent)",
        "answers": {
            "Query type": "chain_city",
            "Result type": "poi",
            "result inside the requested": "n",
            "how many open/exists branches": "0",
            "how close is it": "adjacent",
        },
        "expected": "Excellent",
    },
    {
        "id": "Q20",
        "desc": "133 Spring Hill Ave (Excellent)",
        "answers": {
            "Query type": "full_addr",
            "Result type": "address_only",
            "exactly match the queried": "y",
            "exist in the real world": "n",
        },
        "expected": "Excellent",
    },
    {
        "id": "Q21",
        "desc": "16th Street Mission (Bad)",
        "answers": {
            "Query type": "transit",
            "Result type": "station",
            "exact name match": "n",
            "same locality": "y",
        },
        "expected": "Bad",
    },
]


def run_tests():
    lookup_relevance.TEST_MODE = True
    passed = 0
    failed = 0

    print(f"Running {len(TEST_CASES)} tests...\n")

    for case in TEST_CASES:
        lookup_relevance.TEST_ANSWERS = case["answers"]

        # Capture stdout
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

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Parse output for rating
        rating = "Unknown"
        for line in output.splitlines():
            if line.startswith("Relevance rating:"):
                rating = line.split(":")[1].strip()
                break

        if rating == case["expected"]:
            print(f"PASS: {case['id']} - {case['desc']}")
            passed += 1
        else:
            print(f"FAIL: {case['id']} - {case['desc']}")
            print(f"  Expected: {case['expected']}")
            print(f"  Got:      {rating}")
            # print(f"  Output:\n{output}")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed.")


if __name__ == "__main__":
    run_tests()
