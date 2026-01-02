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
    """Load a list of rule dictionaries from a JSON file.

    If the file does not exist or is empty, return an empty list. This helper
    allows merging multiple rule files by simply extending the returned list.
    """
    p = Path(path)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def matches_value(rule_val: Any, fact_val: Any) -> bool:
    if isinstance(rule_val, list):
        return fact_val in rule_val
    return fact_val == rule_val


def rule_is_compatible(
    rule: Rule, facts: Facts
) -> Tuple[bool, int, int, List[str], List[str]]:
    """
    Determine if a rule is compatible with the current facts.

    A rule is compatible if none of its `when` conditions contradict the facts. This
    returns a tuple of:
    - ok: True if compatible, False otherwise
    - known_matched: number of `when` conditions satisfied by known facts
    - total_conditions: total number of conditions in `when`
    - matched_keys: list of condition keys that were matched
    - missing_keys: list of condition keys that were missing from facts
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


def required_fields_for_rule(rule: Rule) -> List[str]:
    """Return a list of fields required to fully evaluate the rule.

    This includes both the keys in `when` and any selectors used in `rating_map`
    or `demotion_reason_map`. Without these fields present in `facts`, the rule
    cannot produce a non-Unknown rating.
    """
    required = set(rule.get("when", {}).keys())
    then = rule.get("then", {})
    rating_map = then.get("rating_map")
    if isinstance(rating_map, dict):
        required.update(rating_map.keys())
    demotion_reason_map = then.get("demotion_reason_map")
    if isinstance(demotion_reason_map, dict):
        required.update(demotion_reason_map.keys())
    return sorted(required)


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
        # Ask the user to research whether the station or POI name matches exactly
        facts["exact_match"] = ask_bool(
            "Research: Is the result an exact name match to the query?", default=False
        )
    elif field == "same_locality":
        # For transit or locality queries, verify via research whether the result is in the same city/area
        facts["same_locality"] = ask_bool(
            "Research: Is the result in the queried locality/area?", default=False
        )
    elif field == "same_street":
        # For partial-address queries, confirm whether the result lies on the same street as the query
        facts["same_street"] = ask_bool(
            "Research: Is the result on the same street as in the query?", default=True
        )
    elif field == "same_address":
        # For full-address queries, verify whether the returned address exactly matches the query
        facts["same_address"] = ask_bool(
            "Research: Is the returned address exactly the same as the query address?", default=True
        )
    elif field == "address_exists":
        facts["address_exists"] = ask_bool(
            "Research: does the queried full address exist in real world?", default=True
        )
    elif field == "distance_tier":
        # Chain queries require determining how close this result is relative to all real-world locations in the location‑intent area
        facts["distance_tier"] = ask_choice(
            "Research: determine the distance tier for this result (closest, second, third, irrelevant) based on real-world chain locations in the location-intent area",
            ["closest", "second", "third", "irrelevant"],
            default="second",
        )
    elif field == "result_in_requested_location":
        # For chain + general location queries, ask whether the result is actually inside the requested city/area
        facts["result_in_requested_location"] = ask_bool(
            "Research: Is the result inside the requested (explicit) location?", default=True
        )
    elif field == "inside_open_count":
        # Determine the number of open/existing branches of the chain within the requested location (closed locations do not count)
        facts["inside_open_count"] = ask_choice(
            "Research: how many OPEN/EXISTS branches of the chain are inside the requested location? (Closed branches do NOT count)",
            ["0", "1", "2+"],
            default="2+",
        )
    elif field == "proximity_tier":
        # If no branch exists inside the requested location, ask how close the result is to that location
        facts["proximity_tier"] = ask_choice(
            "Research: if the result is outside the requested location, how close is it (adjacent, near, far)?",
            ["adjacent", "near", "far"],
            default="adjacent",
        )
    # Name/Category accuracy fields
    elif field == "result_is_address_type":
        # Identify whether the result is an address-type (address/street/locality) rather than a POI
        facts["result_is_address_type"] = ask_bool(
            "Is the result an address-type entity (address/street/locality) rather than a business/POI?",
            default=False,
        )
    elif field == "category_correct":
        # Check if the result's category/classification matches the intended entity
        facts["category_correct"] = ask_bool(
            "Research: Is the result category/classification correct?",
            default=True,
        )
    elif field == "name_match_quality":
        # Determine how closely the result's name matches the intended entity
        facts["name_match_quality"] = ask_choice(
            "Research: Name match quality?",
            ["exact", "minor_variation", "major_mismatch", "cant_verify"],
            default=None,
        )
    elif field == "is_parking_feature":
        # Is this result a parking lot/garage type feature?
        facts["is_parking_feature"] = ask_bool(
            "Is the result a parking feature (parking lot/garage/structure)?",
            default=False,
        )
    elif field == "name_includes_parking_term":
        # For parking features, does the name include a parking descriptor?
        facts["name_includes_parking_term"] = ask_bool(
            "Does the result name include a parking descriptor (Parking/Lot/Garage)?",
            default=True,
        )
    # Address accuracy fields
    elif field == "poi_address_expected_level":
        facts["poi_address_expected_level"] = ask_choice(
            "What address level is expected for this POI (full_expected, locality_only_ok, no_official_address)?",
            ["full_expected", "locality_only_ok", "no_official_address"],
            default="full_expected",
        )
    elif field == "address_component_issue":
        facts["address_component_issue"] = ask_choice(
            "Research: Identify the address component issue (none, formatting_only, locality, street_name, street_number, postal_code, does_not_exist, cant_verify)",
            [
                "none",
                "formatting_only",
                "locality",
                "street_name",
                "street_number",
                "postal_code",
                "does_not_exist",
                "cant_verify",
            ],
            default="none",
        )
    # Pin accuracy fields
    elif field == "pin_relation":
        facts["pin_relation"] = ask_choice(
            "Research: Where does the pin land relative to the intended feature?",
            ["precise", "within_feature", "next_door_same_block", "outside", "cant_verify"],
            default=None,
        )
    elif field == "shared_space":
        facts["shared_space"] = ask_bool(
            "Is the business located in a shared complex/strip mall where multiple businesses share a roof or parking?",
            default=False,
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
    # Determine which task the user wants to perform. Default to relevance if they simply press enter.
    task_options = ["relevance", "name_category", "address_accuracy", "pin_accuracy"]
    task = ask_choice(
        "Which task do you want to evaluate? (relevance, name_category, address_accuracy, pin_accuracy)",
        task_options,
        default="relevance",
    )
    facts: Facts = {"task": task}

    # Load rules from all available rule files. Relevance rules always exist. Additional rules
    # are merged when evaluating data accuracy tasks.
    rules: List[Rule] = []
    rules.extend(load_rules("rules_relevance_v1.json"))
    # Load data accuracy rules if the file exists
    rules.extend(load_rules("rules_data_accuracy_v1.json"))

    # If performing relevance, collect base location facts
    if task == "relevance":
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
        # Normalize missing viewport to fresh immediately
        if facts["viewport_age"] == "none":
            facts["viewport_age"] = "fresh"
            facts["user_in_viewport"] = "na"
        else:
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
    else:
        # For non-relevance tasks we do not compute location intent
        facts["location_intent"] = "unknown"

    # iterative: pick best candidates, ask missing fields for them
    for _ in range(3):  # cap follow-up rounds
        candidates: List[Tuple[int, Rule, List[str]]] = []
        for r in rules:
            if r.get("task") != facts["task"]:
                continue
            ok, known_matched, total_cond, matched_keys, missing_keys = rule_is_compatible(
                r, facts
            )
            if not ok:
                continue
            candidates.append((score_rule(known_matched, total_cond), r, matched_keys))

        candidates.sort(key=lambda x: x[0], reverse=True)
        top = candidates[:5]
        if not top:
            print("\nNo compatible rules found. Add a new rule.")
            return

        # Determine which fields are missing across top candidates by looking at required fields
        missing_set: List[str] = []
        for _, r, _ in top:
            for k in required_fields_for_rule(r):
                if k not in facts and k not in missing_set:
                    missing_set.append(k)
        if not missing_set:
            break  # we have enough facts to evaluate
        # Ask at most two missing fields per round
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
        if not ok:
            continue
        # ensure all required fields are present
        if any(k not in facts for k in required_fields_for_rule(r)):
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
    # Only show location intent when relevant (relevance task)
    if task == "relevance":
        print(f"Location intent (computed): {facts['location_intent']}")
        print(f"Relevance rating: {rating}")
        print(f"Demotion reason: {demotion_reason}")
    else:
        print(f"Rating: {rating}")
    # show rule info and guideline citations
    print("Comment template:")
    print(f"- Rule: {best['id']}")
    why_comment = best.get('then', {}).get('comment', '').strip()
    print(f"- Why: {why_comment}")
    print(f"- GL: {gl}")


if __name__ == "__main__":
    main()