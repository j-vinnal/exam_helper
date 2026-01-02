from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

Facts = Dict[str, Any]
Rule = Dict[str, Any]

# ------------------- Test Infrastructure -------------------
TEST_MODE = False
# Preferred: fact-id -> value (e.g., {"qt": "locality", "exact_match": "y"})
TEST_ANSWERS: Dict[str, str] = {}
# -----------------------------------------------------------


def _load_lexicon(path: str = "lexicon_relevance.json") -> Dict[str, Any]:
    try:
        file_path = Path(__file__).parent / path
        if file_path.exists():
            return json.loads(file_path.read_text(encoding="utf-8"))
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


LEXICON: Dict[str, Any] = _load_lexicon()


@dataclass(frozen=True)
class DecisionOutput:
    rating: str
    demotion_reason: str = "N/A"


def _load_json(path: str) -> Any:
    file_path = Path(__file__).parent / path
    if file_path.exists():
        return json.loads(file_path.read_text(encoding="utf-8"))
    return json.loads(Path(path).read_text(encoding="utf-8"))


SCHEMA: Dict[str, Any] = _load_json("rules_v2.json")


def _enum_options(enum_name: str) -> List[str]:
    return list(SCHEMA.get("enums", {}).get(enum_name, []))


def _question_def(fact_id: str) -> Dict[str, Any]:
    q = SCHEMA.get("questions", {}).get(fact_id)
    if not q:
        raise KeyError(f"Unknown question/fact id: {fact_id}")
    return q


def _normalize_bool_answer(val: str) -> bool:
    return val.strip().lower() in ("y", "yes", "j", "jah", "true", "1")


def _test_answer_for_fact(fact_id: str, prompt: str) -> Optional[str]:
    if fact_id in TEST_ANSWERS:
        return TEST_ANSWERS[fact_id]

    # Back-compat: allow older tests to match by aliases or prompt substring
    aliases = _question_def(fact_id).get("test_aliases", [])
    for key, val in TEST_ANSWERS.items():
        key_l = key.lower()
        if any(a.lower() == key_l for a in aliases):
            return val
        if key_l in prompt.lower():
            return val
    return None


def ask_enum(
    fact_id: str,
    *,
    options: List[str],
    prompt: str,
    default: Optional[str],
    desc_map: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    if TEST_MODE:
        ans = _test_answer_for_fact(fact_id, prompt)
        if ans is None:
            if default is None:
                raise RuntimeError(f"TEST_MODE: missing answer for '{fact_id}'")
            return default
        ans = ans.strip()
        return ans

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
        raw = input(f"Choice{hint}: ").strip()
        if not raw and default is not None:
            return default
        raw_l = raw.lower()
        if raw_l in options:
            return raw_l
        print(f"Invalid. Choose one of: {', '.join(options)}")


def ask_bool(fact_id: str, *, prompt: str, default: Optional[bool]) -> bool:
    if TEST_MODE:
        ans = _test_answer_for_fact(fact_id, prompt)
        if ans is None:
            if default is None:
                raise RuntimeError(f"TEST_MODE: missing answer for '{fact_id}'")
            return default
        return _normalize_bool_answer(ans)

    hint = " [y/n]"
    if default is not None:
        hint += f" (default={'y' if default else 'n'})"
    while True:
        raw = input(prompt + hint + ": ").strip().lower()
        if not raw and default is not None:
            return default
        if raw in ("y", "yes", "j", "jah"):
            return True
        if raw in ("n", "no", "ei"):
            return False
        print("Please answer y/n.")


def ask_fact(fact_id: str, facts: Facts) -> None:
    if fact_id in facts:
        return

    q = _question_def(fact_id)
    q_type = q.get("type")
    prompt = q.get("prompt", fact_id)

    if q_type == "bool":
        default = q.get("default")
        facts[fact_id] = ask_bool(fact_id, prompt=prompt, default=default)
        return

    if q_type == "enum":
        default = q.get("default")
        if "options" in q:
            options = list(q["options"])
        else:
            enum_name = q.get("enum")
            if not enum_name:
                raise KeyError(f"Question '{fact_id}' missing 'options' or 'enum'")
            options = _enum_options(enum_name)
        if default is None:
            default_opt: Optional[str] = None
        else:
            default_opt = str(default)
        lex_key = q.get("lexicon_key")
        desc_map = LEXICON.get(lex_key) if isinstance(lex_key, str) else None
        facts[fact_id] = ask_enum(
            fact_id,
            options=options,
            prompt=prompt,
            default=default_opt,
            desc_map=desc_map,
        )
        return

    raise ValueError(f"Unsupported question type for '{fact_id}': {q_type}")


def matches_value(rule_val: Any, fact_val: Any) -> bool:
    if isinstance(rule_val, list):
        return fact_val in rule_val
    return fact_val == rule_val


def rule_is_compatible(rule: Rule, facts: Facts) -> Tuple[bool, int, int, List[str]]:
    when = rule.get("when", {})
    known_matched = 0
    matched_keys: List[str] = []

    for k, rule_val in when.items():
        if k not in facts:
            continue
        if not matches_value(rule_val, facts[k]):
            return (False, 0, 0, [])
        known_matched += 1
        matched_keys.append(k)

    return (True, known_matched, len(when), matched_keys)


def score_rule(known_matched: int, total_conditions: int) -> int:
    return known_matched * 10 + total_conditions


def required_fields_for_rule(rule: Rule) -> List[str]:
    required = set(rule.get("when", {}).keys())

    then = rule.get("then", {})
    decision = then.get("decision")
    if isinstance(decision, dict):
        selector = decision.get("selector")
        if selector:
            required.add(selector)

    # Back-compat with v1 rating_map/demotion_reason_map
    rating_map = then.get("rating_map")
    if isinstance(rating_map, dict):
        required.update(rating_map.keys())

    demotion_reason_map = then.get("demotion_reason_map")
    if isinstance(demotion_reason_map, dict):
        required.update(demotion_reason_map.keys())

    return sorted(required)


def is_rule_fully_evaluable(rule: Rule, facts: Facts) -> bool:
    return all(k in facts for k in required_fields_for_rule(rule))


def compute_location_intent(viewport_age: str, user_in_viewport: str, qt: str) -> str:
    if qt in ("chain_city", "full_addr", "locality"):
        return "explicit"
    vp = viewport_age if viewport_age != "none" else "fresh"
    if vp == "stale":
        return "user"
    if vp == "fresh":
        return "viewport" if user_in_viewport == "out" else "user"
    return "unknown"


def _apply_decision(decision: Dict[str, Any], facts: Facts) -> DecisionOutput:
    d_type = decision.get("type")
    if d_type != "map":
        return DecisionOutput(rating="Unknown", demotion_reason="N/A")

    selector = decision.get("selector")
    if not selector:
        return DecisionOutput(rating="Unknown", demotion_reason="N/A")

    value = facts.get(selector)
    mapping = decision.get("map", {})
    if value is None:
        return DecisionOutput(rating="Unknown", demotion_reason="N/A")

    out = mapping.get(value)
    if isinstance(out, dict):
        return DecisionOutput(
            rating=str(out.get("rating", "Unknown")),
            demotion_reason=str(out.get("demotion_reason", "N/A")),
        )

    return DecisionOutput(rating=str(out or "Unknown"), demotion_reason="N/A")


def apply_rule(rule: Rule, facts: Facts) -> Tuple[str, str, str, str]:
    then = rule.get("then", {})

    refs = rule.get("refs", [])
    refs_str = ", ".join(
        [
            str(r.get("section"))
            for r in refs
            if isinstance(r, dict)
            and r.get("source") == "guidelines"
            and r.get("section")
        ]
    )

    comment = str(then.get("comment", ""))

    if "rating" in then:
        return (
            str(then["rating"]),
            str(then.get("demotion_reason", "N/A")),
            refs_str,
            comment,
        )

    decision = then.get("decision")
    if isinstance(decision, dict):
        out = _apply_decision(decision, facts)
        return out.rating, out.demotion_reason, refs_str, comment

    # Back-compat
    rating_map = then.get("rating_map")
    if isinstance(rating_map, dict) and rating_map:
        for field, mapping in rating_map.items():
            val = facts.get(field)
            if val is None:
                return "Unknown", "N/A", refs_str, comment
            rating = mapping.get(val, "Unknown")
            dr_map = then.get("demotion_reason_map", {}).get(field, {})
            demotion_reason = dr_map.get(val, "N/A")
            return rating, demotion_reason, refs_str, comment

    return "Unknown", "N/A", refs_str, comment


def evaluate_task(task: str, facts: Facts) -> Tuple[str, Rule, str, str, str]:
    rules = [r for r in SCHEMA.get("rules", []) if r.get("task") == task]
    if not rules:
        raise RuntimeError(f"No rules found for task '{task}'")

    # Ask baseline facts per task
    if task == "relevance":
        # Match v1 prompts + defaults + viewport logic
        ask_fact("qt", facts)
        ask_fact("rt", facts)

        ask_fact("viewport_age", facts)
        if facts.get("viewport_age") == "fresh":
            ask_fact("user_in_viewport", facts)
        else:
            facts["user_in_viewport"] = "na"

        facts["location_intent"] = compute_location_intent(
            facts.get("viewport_age", "none"),
            facts.get("user_in_viewport", "na"),
            facts.get("qt", "other"),
        )

    elif task in ("name_accuracy", "address_accuracy"):
        ask_fact("rt", facts)

    elif task == "pin_accuracy":
        # Guidelines-first: if the place/address doesn't exist, pin is Can't Verify.
        # Also support the Satellite vs Vector generosity rule.
        ask_fact("address_exists", facts)
        facts["location_exists"] = facts.get("address_exists")
        if facts.get("address_exists") is True:
            ask_fact("pin_generous_perfect", facts)

        # Only collect geometry/context details if we still need them.
        if (
            facts.get("address_exists") is True
            and facts.get("pin_generous_perfect") is not True
        ):
            ask_fact("poi_context", facts)
            ask_fact("pin_relation", facts)

            if facts.get("pin_relation") == "next_door":
                ask_fact("cross_street_between", facts)

    # Iteratively collect missing required fields for best-matching candidates
    for _ in range(20):
        candidates: List[Tuple[int, Rule]] = []
        for r in rules:
            ok, known, total, _ = rule_is_compatible(r, facts)
            if not ok:
                continue
            candidates.append((score_rule(known, total), r))

        if not candidates:
            break

        candidates.sort(key=lambda x: x[0], reverse=True)

        # prefer fully evaluable
        best_rule = None
        for _, r in candidates:
            if is_rule_fully_evaluable(r, facts):
                best_rule = r
                break
        if best_rule is None:
            best_rule = candidates[0][1]

        missing = [k for k in required_fields_for_rule(best_rule) if k not in facts]
        if not missing:
            rating, demotion_reason, refs, comment = apply_rule(best_rule, facts)
            return rating, best_rule, demotion_reason, refs, comment

        # ask next missing (one at a time keeps it simple)
        ask_fact(missing[0], facts)

    # fallback: pick best compatible rule and return unknown
    candidates = []
    for r in rules:
        ok, known, total, _ = rule_is_compatible(r, facts)
        if ok:
            candidates.append((score_rule(known, total), r))
    if not candidates:
        raise RuntimeError(f"No compatible rules for task '{task}' with facts={facts}")

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_rule = candidates[0][1]
    rating, demotion_reason, refs, comment = apply_rule(best_rule, facts)
    return rating, best_rule, demotion_reason, refs, comment


def main() -> None:
    facts: Facts = {}

    # Task choice
    ask_fact("task", facts)
    task = facts["task"]

    tasks = ["relevance", "name_accuracy", "address_accuracy", "pin_accuracy"]
    if task == "all":
        selected = tasks
    else:
        selected = [task]

    for t in selected:
        if t == "relevance":
            rating, rule, demotion_reason, refs, comment = evaluate_task(t, facts)

            # Build v1-like top3 debug view based on current facts
            rules = [r for r in SCHEMA.get("rules", []) if r.get("task") == "relevance"]
            finals: List[Tuple[int, Rule, List[str]]] = []
            for r in rules:
                ok, known, total, matched = rule_is_compatible(r, facts)
                if not ok:
                    continue
                if not is_rule_fully_evaluable(r, facts):
                    continue
                finals.append((score_rule(known, total), r, matched))
            finals.sort(key=lambda x: x[0], reverse=True)
            top3 = finals[:3]

            print("\n--- Top 3 matched rules ---")
            for score, r, keys in top3:
                print(
                    f"* score={score} id={r.get('id','')} matched={keys} GL={refs_for_rule(r)}"
                )

            comment_template = build_comment_template_v1(
                rule, facts, rating, demotion_reason
            )

            print("\n=== Suggested output ===")
            print(
                f"Location intent (computed): {facts.get('location_intent','unknown')}"
            )
            print(f"Relevance rating: {rating}")
            print(f"Demotion reason: {demotion_reason}")
            print("Comment template:")
            print(comment_template)
            print(f"Rule: {rule.get('id','')}")
            print(f"Why: {rule.get('then', {}).get('comment', '')}")
            print(f"GL: {refs}")
            _print_research_checklist(t)
            continue

        rating, rule, demotion_reason, refs, comment = evaluate_task(t, facts)
        print(f"\nTask: {t}")
        print(f"Rule: {rule.get('id', '')}")
        print(f"Rating: {rating}")
        if refs:
            print(f"Guidelines: {refs}")
        if comment:
            print(f"Comment: {comment}")
        _print_research_checklist(t)


def _print_research_checklist(task: str) -> None:
    checklists = SCHEMA.get("research_checklists", {})
    items = checklists.get(task)
    if not items:
        return

    print("\nMandatory research prompts:")
    for item in items:
        print(f"- {item}")


def refs_for_rule(rule: Rule) -> str:
    refs = rule.get("refs", [])
    sections = [
        str(r.get("section"))
        for r in refs
        if isinstance(r, dict) and r.get("source") == "guidelines" and r.get("section")
    ]
    return ",".join(sections)


def build_comment_template_v1(
    rule: Rule, facts: Facts, rating: str, demotion_reason: str
) -> str:
    """Mirror v1 behavior: only require comment for Good/Acceptable/Bad."""
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

    why = str(rule.get("then", {}).get("comment", "")).strip()
    if why:
        why = f"Reasoning: {why} "
    return (
        f"User intent: [describe]. {why}Demoted to {rating} for {demotion_reason}. "
        "Evidence: [cite authoritative source / locator / map]."
    )


if __name__ == "__main__":
    main()
