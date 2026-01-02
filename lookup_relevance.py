from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional


Facts = Dict[str, Any]
Rule = Dict[str, Any]

# Load lexicon descriptions for query/result and follow-up options. This file defines
# human-readable titles and descriptions for the codes used in the rating lookup.
try:
    LEXICON = json.loads(Path("lexicon_relevance.json").read_text(encoding="utf-8"))
except Exception:
    LEXICON = {}


# ------------------- UI helpers -------------------


def ask_choice(
    prompt: str,
    options: List[str],
    default: Optional[str] = None,
    desc_map: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """Ask the user to choose one option from a list.

    If desc_map is provided, print each option with its description to aid selection.
    """
    print(f"\n{prompt}")
    # Print option descriptions if available
    for opt in options:
        # If descriptions exist for this option, show title and description
        if desc_map and opt in desc_map:
            info = desc_map[opt]
            title = info.get("title") or opt
            desc = info.get("description") or ""
            print(f"  {opt:12} – {title}: {desc}")
        else:
            print(f"  {opt}")

    hint = ""
    if default is not None:
        hint = f" (default={default})"
    while True:
        ans = input(f"Choice{hint}: ").strip().lower()
        if not ans and default is not None:
            return default
        if ans in options:
            return ans
        print(f"Invalid. Choose one of: {', '.join(options)}")


def ask_bool(prompt: str, default: Optional[bool] = None) -> bool:
    hint = " [y/n]"
    if default is not None:
        hint += f" (default={'y' if default else 'n'})"
    while True:
        ans = input(prompt + hint + ": ").strip().lower()
        if not ans and default is not None:
            return default
        if ans in ("y", "yes", "j", "jah"):
            return True
        if ans in ("n", "no", "ei"):
            return False
        print("Please answer y/n.")


# ------------------- matching -------------------


def load_rules(path: str) -> List[Rule]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def matches_value(rule_val: Any, fact_val: Any) -> bool:
    if isinstance(rule_val, list):
        return fact_val in rule_val
    return fact_val == rule_val


def rule_is_compatible(
    rule: Rule, facts: Facts
) -> Tuple[bool, int, int, List[str], List[str]]:
    """
    Compatible = no known fact contradicts the rule.
    Returns: (ok, known_matched, total_conditions, matched_keys, missing_keys)
    """
    when = rule.get("when", {})
    known_matched = 0
    matched_keys: List[str] = []
    missing_keys: List[str] = []

    for k, rule_val in when.items():
        if k not in facts:
            missing_keys.append(k)
            continue
        if not matches_value(rule_val, facts[k]):
            return (False, 0, 0, [], [])
        known_matched += 1
        matched_keys.append(k)

    return (True, known_matched, len(when), matched_keys, missing_keys)


def score_rule(known_matched: int, total_conditions: int) -> int:
    # Prefer rules that match many known facts and are specific.
    return known_matched * 10 + total_conditions


# ------------------- LI (computed) -------------------


def compute_location_intent(viewport_age: str, user_in_viewport: str, qt: str) -> str:
    """Compute the location intent based on viewport state and query type.

    - For explicit location queries (chain_city, full_addr, locality), return 'explicit'.
    - Treat missing viewport ('none') as fresh.
    - For stale viewports, default to the user’s location.
    - For fresh viewports: if user is outside, use viewport; if inside or unknown (na), use user.
    """
    # Explicit location: ignore viewport/user context
    if qt in ("chain_city", "full_addr", "locality"):
        return "explicit"
    # Normalize 'none' to 'fresh' (per guideline: missing viewport treated as fresh)
    vp = viewport_age if viewport_age != "none" else "fresh"
    if vp == "stale":
        return "user"
    if vp == "fresh":
        # 'out' → viewport; 'in' or 'na' → user (no reliable viewport relationship)
        return "viewport" if user_in_viewport == "out" else "user"
    return "unknown"


# ------------------- dynamic follow-ups -------------------


def ask_missing_field(field: str, facts: Facts) -> None:
    if field == "exact_match":
        facts["exact_match"] = ask_bool(
            "Is the result an exact name match to the query?", default=False
        )
    elif field == "same_locality":
        facts["same_locality"] = ask_bool(
            "Is the result in the queried locality/area?", default=False
        )
    elif field == "same_street":
        facts["same_street"] = ask_bool(
            "Is it the same street as in the query?", default=True
        )
    elif field == "same_address":
        facts["same_address"] = ask_bool(
            "Is it the same address as in the query?", default=True
        )
    elif field == "address_exists":
        facts["address_exists"] = ask_bool(
            "Research: does the queried full address exist in real world?", default=True
        )
    elif field == "distance_tier":
        facts["distance_tier"] = ask_choice(
            "Chain distance tier vs REAL-WORLD options in Location-Intent area",
            ["closest", "second", "third", "irrelevant"],
            default="second",
            desc_map=LEXICON.get("distance_tier")
        )
    elif field == "result_in_requested_location":
        facts["result_in_requested_location"] = ask_bool(
            "Is the result inside the requested (explicit) location?", default=True
        )
    elif field == "inside_open_count":
        facts["inside_open_count"] = ask_choice(
            "How many OPEN/EXISTS branches are inside the requested location? (Closed does NOT count)",
            ["0", "1", "2+"],
            default="2+",
            desc_map=LEXICON.get("inside_open_count")
        )
    elif field == "proximity_tier":
        facts["proximity_tier"] = ask_choice(
            "If result is outside requested location: how close is it to the requested location?",
            ["adjacent", "near", "far"],
            default="adjacent",
            desc_map=LEXICON.get("proximity_tier")
        )
    else:
        # Unknown field: ask a generic text (or skip)
        facts[field] = input(f"Provide value for {field}: ").strip()


def apply_rule(rule: Rule, facts: Facts) -> Tuple[str, str, str]:
    then = rule.get("then", {})
    gl = ", ".join(rule.get("gl", []))

    # direct rating
    if "rating" in then:
        return then["rating"], then.get("demotion_reason", "N/A"), gl

    # rating_map
    rating_map = then.get("rating_map")
    if rating_map:
        # only one key expected in this v1
        for field, mapping in rating_map.items():
            val = facts.get(field)
            if val is None:
                return "Unknown", "N/A", gl
            rating = mapping.get(val, "Unknown")
            # demotion reason mapping (optional)
            dr_map = then.get("demotion_reason_map", {}).get(field, {})
            demotion_reason = dr_map.get(val, "N/A")
            return rating, demotion_reason, gl

    return "Unknown", "N/A", gl


# ------------------- main -------------------


def main() -> None:
    rules = load_rules("rules_relevance_v1.json")
    facts: Facts = {"task": "relevance"}

    # minimal base facts
    facts["qt"] = ask_choice(
        "Query type (qt)",
        [
            "full_addr",
            "street",
            "poi_name",
            "chain_plain",
            "chain_city",
            "locality",
            "transit",
            "category_mall",
            "category",
            "other",
        ],
        default="other",
        desc_map=LEXICON.get("qt")
    )
    facts["rt"] = ask_choice(
        "Result type (rt)",
        [
            "address_only",
            "street",
            "poi",
            "dept",
            "store_in_mall",
            "mall",
            "station",
            "airport",
            "locality",
            "other",
        ],
        default="poi",
        desc_map=LEXICON.get("rt")
    )
    facts["viewport_age"] = ask_choice(
        "Viewport age", ["fresh", "stale", "none"], default="fresh", desc_map=LEXICON.get("viewport_age")
    )
    # normalize missing viewport to fresh immediately
    if facts["viewport_age"] == "none":
        facts["viewport_age"] = "fresh"
        # user_in_viewport cannot be determined; treat as not applicable
        facts["user_in_viewport"] = "na"
    else:
        if facts["viewport_age"] == "fresh":
            facts["user_in_viewport"] = ask_choice(
                "User vs Fresh Viewport",
                ["in", "out"],
                default="in",
                desc_map=LEXICON.get("user_in_viewport")
            )
        else:
            # stale viewport, user_in_viewport is not applicable
            facts["user_in_viewport"] = "na"

    facts["location_intent"] = compute_location_intent(
        facts["viewport_age"], facts["user_in_viewport"], facts["qt"]
    )

    # iterative: pick best candidates, ask missing fields for them
    for _ in range(3):  # cap follow-up rounds
        candidates: List[Tuple[int, Rule, List[str], List[str]]] = []
        for r in rules:
            if r.get("task") != facts["task"]:
                continue
            ok, known_matched, total_cond, matched_keys, missing_keys = (
                rule_is_compatible(r, facts)
            )
            if not ok:
                continue
            candidates.append(
                (score_rule(known_matched, total_cond), r, matched_keys, missing_keys)
            )

        candidates.sort(key=lambda x: x[0], reverse=True)
        top = candidates[:5]
        if not top:
            print("\nNo compatible rules found. Add a new rule.")
            return

        # collect missing keys from top candidates
        missing_set = []
        for _, r, _, missing_keys in top:
            for k in missing_keys:
                if k not in facts and k not in missing_set:
                    missing_set.append(k)

        if not missing_set:
            break  # we have enough facts to fully evaluate best rules

        # ask at most 2 missing fields per round
        for k in missing_set[:2]:
            ask_missing_field(k, facts)

    # final selection (now should have required fields)
    finals: List[Tuple[int, Rule, List[str]]] = []
    for r in rules:
        if r.get("task") != facts["task"]:
            continue
        ok, known_matched, total_cond, matched_keys, missing_keys = rule_is_compatible(
            r, facts
        )
        if not ok or missing_keys:
            continue
        finals.append((score_rule(known_matched, total_cond), r, matched_keys))

    if not finals:
        print(
            "\nNo fully-satisfied rule after follow-ups. Showing best compatible candidates:"
        )
        # fall back to top compatible
        # (reuse earlier candidates)
        return

    finals.sort(key=lambda x: x[0], reverse=True)
    top3 = finals[:3]

    print("\n--- Top 3 matched rules ---")
    for score, r, keys in top3:
        print(
            f"* score={score} id={r['id']} matched={keys} GL={','.join(r.get('gl', []))}"
        )

    best = top3[0][1]
    rating, demotion_reason, gl = apply_rule(best, facts)

    print("\n=== Suggested output ===")
    print(f"Location intent (computed): {facts['location_intent']}")
    print(f"Relevance rating: {rating}")
    print(f"Demotion reason: {demotion_reason}")
    print("Comment template:")
    print(f"- Rule: {best['id']}")
    print(f"- Why: {best.get('then', {}).get('comment', '')}")
    print(f"- GL: {gl}")


if __name__ == "__main__":
    main()
