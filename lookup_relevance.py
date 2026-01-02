from __future__ import annotations

"""
Rule-based interactive helper for relevance rating practice.

Fix: treat `then.rating_map` selector fields (e.g., distance_tier, proximity_tier)
as REQUIRED inputs, not optional. Otherwise rules can "match" but still return
rating="Unknown" because the selector fact was never collected.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

Facts = Dict[str, Any]
Rule = Dict[str, Any]


# ------------------- Lexicon (optional) -------------------

def _load_lexicon(path: str = "lexicon_relevance.json") -> Dict[str, Any]:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


LEXICON: Dict[str, Any] = _load_lexicon()


# ------------------- UI helpers -------------------


def ask_choice(
    prompt: str,
    options: List[str],
    *,
    default: Optional[str] = None,
    desc_map: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """Ask the user to choose one option from a list."""
    print(f"\n{prompt}")
    for opt in options:
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


def ask_bool(prompt: str, *, default: Optional[bool] = None) -> bool:
    """Ask yes/no."""
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


# ------------------- Matching -------------------


def load_rules(path: str) -> List[Rule]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def matches_value(rule_val: Any, fact_val: Any) -> bool:
    if isinstance(rule_val, list):
        return fact_val in rule_val
    return fact_val == rule_val


def rule_is_compatible(
    rule: Rule, facts: Facts
) -> Tuple[bool, int, int, List[str], List[str]]:
    """Compatible = no known fact contradicts the rule (checked only against `when`)."""
    when = rule.get("when", {})
    known_matched = 0
    matched_keys: List[str] = []
    missing_when_keys: List[str] = []

    for k, rule_val in when.items():
        if k not in facts:
            missing_when_keys.append(k)
            continue
        if not matches_value(rule_val, facts[k]):
            return (False, 0, 0, [], [])
        known_matched += 1
        matched_keys.append(k)

    return (True, known_matched, len(when), matched_keys, missing_when_keys)


def score_rule(known_matched: int, total_conditions: int) -> int:
    """Prefer rules that match many known facts and are specific."""
    return known_matched * 10 + total_conditions


def required_fields_for_rule(rule: Rule) -> List[str]:
    """Fields required to *evaluate* a rule (when + rating_map selectors)."""
    required = set(rule.get("when", {}).keys())
    then = rule.get("then", {})

    rating_map = then.get("rating_map")
    if isinstance(rating_map, dict):
        required.update(rating_map.keys())

    demotion_reason_map = then.get("demotion_reason_map")
    if isinstance(demotion_reason_map, dict):
        required.update(demotion_reason_map.keys())

    return sorted(required)


def is_rule_fully_evaluable(rule: Rule, facts: Facts) -> bool:
    return all(k in facts for k in required_fields_for_rule(rule))


# ------------------- Location intent (computed) -------------------


def compute_location_intent(viewport_age: str, user_in_viewport: str, qt: str) -> str:
    """
    - Explicit-location queries ignore viewport/user context.
    - Missing viewport is treated as fresh.
    - Stale viewport -> user.
    - Fresh viewport -> viewport if user outside; otherwise user.
    """
    if qt in ("chain_city", "full_addr", "locality"):
        return "explicit"

    vp = viewport_age if viewport_age != "none" else "fresh"
    if vp == "stale":
        return "user"
    if vp == "fresh":
        return "viewport" if user_in_viewport == "out" else "user"
    return "unknown"


# ------------------- Follow-ups -------------------


def ask_missing_field(field: str, facts: Facts) -> None:
    """
    For distance/proximity judgments: you MUST research the REAL WORLD (e.g., official store locator),
    not only the returned results list.
    """

    if field == "exact_match":
        facts["exact_match"] = ask_bool(
            "Research: Is the result an exact name match to the query?",
            default=False,
        )
        return

    if field == "same_locality":
        facts["same_locality"] = ask_bool(
            "Research: Is the result in the queried locality/area?",
            default=False,
        )
        return

    if field == "same_street":
        facts["same_street"] = ask_bool(
            "Research: Is the result on the same street as in the query?",
            default=True,
        )
        return

    if field == "same_address":
        facts["same_address"] = ask_bool(
            "Research: Does the result exactly match the queried full address?",
            default=True,
        )
        return

    if field == "address_exists":
        facts["address_exists"] = ask_bool(
            "Research: Does the queried full address exist in the real world?",
            default=True,
        )
        return

    if field == "distance_tier":
        li = facts.get("location_intent", "unknown")
        facts["distance_tier"] = ask_choice(
            "Research (CHAIN distance): Based on location intent = "
            f"{li}. Use an official chain store locator and determine how many "
            "real-world locations are clearly closer than THIS result.\n"
            "Choose the distance tier:",
            ["closest", "second", "third", "irrelevant"],
            default=None,  # force explicit choice
            desc_map=LEXICON.get("distance_tier"),
        )
        return

    if field == "result_in_requested_location":
        facts["result_in_requested_location"] = ask_bool(
            "Research: Is the result inside the requested (explicit) location?",
            default=True,
        )
        return

    if field == "inside_open_count":
        facts["inside_open_count"] = ask_choice(
            "Research: How many OPEN/EXISTS branches of the chain are inside the requested location?\n"
            "(Closed branches do NOT count.)",
            ["0", "1", "2+"],
            default=None,
            desc_map=LEXICON.get("inside_open_count"),
        )
        return

    if field == "proximity_tier":
        facts["proximity_tier"] = ask_choice(
            "Research (CHAIN + CITY): If the result is outside the requested location, how close is it?",
            ["adjacent", "near", "far"],
            default=None,
            desc_map=LEXICON.get("proximity_tier"),
        )
        return

    facts[field] = input(f"Provide value for {field}: ").strip()


# ------------------- Applying a rule -------------------


def apply_rule(rule: Rule, facts: Facts) -> Tuple[str, str, str]:
    then = rule.get("then", {})
    gl = ", ".join(rule.get("gl", []))

    if "rating" in then:
        return then["rating"], then.get("demotion_reason", "N/A"), gl

    rating_map = then.get("rating_map")
    if isinstance(rating_map, dict) and rating_map:
        for field, mapping in rating_map.items():
            val = facts.get(field)
            if val is None:
                return "Unknown", "N/A", gl
            rating = mapping.get(val, "Unknown")
            dr_map = then.get("demotion_reason_map", {}).get(field, {})
            demotion_reason = dr_map.get(val, "N/A")
            return rating, demotion_reason, gl

    return "Unknown", "N/A", gl


def build_comment_template(rule: Rule, facts: Facts, rating: str, demotion_reason: str) -> str:
    """Return a comment template (English) when comment is required (Good/Acceptable/Bad)."""
    if rating not in ("Good", "Acceptable", "Bad"):
        return "(No comment required for this rating.)"

    rule_id = rule.get("id", "")
    li = facts.get("location_intent", "unknown")

    if rule_id == "REL.CHAIN.PLAIN.POI_DISTANCE_TIER":
        tier = facts.get("distance_tier", "unknown")
        tier_to_closer = {
            "closest": "0 closer locations",
            "second": "1 closer location",
            "third": "2+ closer locations",
            "irrelevant": "many closer locations / far outside reasonable area",
        }
        closer_txt = tier_to_closer.get(tier, "unknown number of")
        return (
            f"User intent: find the nearest chain location (LI={li}). "
            f"This result is not the closest option: there are {closer_txt} in the real world. "
            f"Demoted to {rating} for {demotion_reason}. "
            "Evidence: [link to official store locator or authoritative source]."
        )

    why = rule.get("then", {}).get("comment", "").strip()
    if why:
        why = f"Reasoning: {why} "
    return (
        f"User intent: [describe]. {why}Demoted to {rating} for {demotion_reason}. "
        "Evidence: [cite authoritative source / locator / map]."
    )


# ------------------- Main -------------------


def main() -> None:
    rules = load_rules("rules_relevance_v1.json")
    facts: Facts = {"task": "relevance"}

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
        desc_map=LEXICON.get("qt"),
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
        desc_map=LEXICON.get("rt"),
    )

    facts["viewport_age"] = ask_choice(
        "Viewport age",
        ["fresh", "stale", "none"],
        default="fresh",
        desc_map=LEXICON.get("viewport_age"),
    )

    if facts["viewport_age"] == "fresh":
        facts["user_in_viewport"] = ask_choice(
            "User vs Fresh Viewport",
            ["in", "out"],
            default="in",
            desc_map=LEXICON.get("user_in_viewport"),
        )
    else:
        facts["user_in_viewport"] = "na"

    facts["location_intent"] = compute_location_intent(
        facts["viewport_age"], facts["user_in_viewport"], facts["qt"]
    )

    # Iterative follow-ups: ask missing required fields from top candidates
    for _ in range(3):
        candidates: List[Tuple[int, Rule, List[str]]] = []
        for r in rules:
            if r.get("task") != facts["task"]:
                continue
            ok, known_matched, total_cond, matched_keys, _ = rule_is_compatible(r, facts)
            if not ok:
                continue
            candidates.append((score_rule(known_matched, total_cond), r, matched_keys))

        candidates.sort(key=lambda x: x[0], reverse=True)
        top = candidates[:5]
        if not top:
            print("\nNo compatible rules found. Add a new rule.")
            return

        missing_set: List[str] = []
        for _, r, _ in top:
            for k in required_fields_for_rule(r):
                if k not in facts and k not in missing_set:
                    missing_set.append(k)

        if not missing_set:
            break

        for k in missing_set[:2]:
            ask_missing_field(k, facts)

    # Final selection: compatible + fully evaluable
    finals: List[Tuple[int, Rule, List[str]]] = []
    for r in rules:
        if r.get("task") != facts["task"]:
            continue
        ok, known_matched, total_cond, matched_keys, _ = rule_is_compatible(r, facts)
        if not ok:
            continue
        if not is_rule_fully_evaluable(r, facts):
            continue
        finals.append((score_rule(known_matched, total_cond), r, matched_keys))

    if not finals:
        print("\nNo fully-evaluable rule after follow-ups.")
        return

    finals.sort(key=lambda x: x[0], reverse=True)
    top3 = finals[:3]

    print("\n--- Top 3 matched rules ---")
    for score, r, keys in top3:
        print(f"* score={score} id={r['id']} matched={keys} GL={','.join(r.get('gl', []))}")

    best = top3[0][1]
    rating, demotion_reason, gl = apply_rule(best, facts)
    comment = build_comment_template(best, facts, rating, demotion_reason)

    print("\n=== Suggested output ===")
    print(f"Location intent (computed): {facts['location_intent']}")
    print(f"Relevance rating: {rating}")
    print(f"Demotion reason: {demotion_reason}")
    print("Comment template:")
    print(comment)
    print(f"Rule: {best['id']}")
    print(f"Why: {best.get('then', {}).get('comment', '')}")
    print(f"GL: {gl}")


if __name__ == "__main__":
    main()
