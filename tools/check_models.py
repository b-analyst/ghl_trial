"""Validate the model roster against OpenRouter's live catalogue.

    python tools/check_models.py [roster]
    python tools/check_models.py --search fable

Reads OPENROUTER_API_KEY from the environment. Prints one line per roster entry
and exits non-zero if any id is unknown, so a retired slug fails in a second
rather than after a batch has burned tokens on 404s.

`--search TERM` lists every catalogue id and name matching TERM, which is how
you resolve a model you know by marketing name but not by slug. Providers
rename freely and a guessed slug is a silently missing cell, so resolve rather
than guess.

The key is read from the environment and never printed, logged, or written to
disk by this script.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = "https://openrouter.ai/api/v1/models"


def read_roster(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [s.strip() for s in lines if s.strip() and not s.lstrip().startswith("#")]


def fetch_catalogue(key: str | None) -> dict[str, str]:
    """Return {model_id: human name} for every model OpenRouter serves."""
    req = urllib.request.Request(CATALOGUE, headers={"Accept": "application/json"})
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    return {m["id"]: m.get("name", "") for m in payload.get("data", [])}


def fetch_tool_support(key: str | None) -> dict[str, bool]:
    """Return {model_id: serves tool calls}.

    A resolving id is not a runnable one. The solver here is
    basic_agent(bash, text_editor), so a model with no tool-calling endpoint
    cannot run a single episode -- OpenRouter answers 404 with 'No endpoints
    found that support tool use'. Two models picked for a cluster sweep on
    price and lineage, microsoft/phi-4 and nousresearch/hermes-4-70b, failed
    exactly that way after the batch had started, because resolving the id
    was the only thing this tool checked.
    """
    req = urllib.request.Request(CATALOGUE, headers={'Accept': 'application/json'})
    if key:
        req.add_header('Authorization', f'Bearer {key}')
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    return {
        m['id']: 'tools' in set(m.get('supported_parameters') or [])
        for m in payload.get('data', [])
    }


def _tokens(text: str) -> set[str]:
    """Split an id or name into lowercase alphanumeric tokens."""
    out, cur = set(), ""
    for ch in text.lower():
        if ch.isalnum():
            cur += ch
        else:
            if cur:
                out.add(cur)
            cur = ""
    if cur:
        out.add(cur)
    return out


def near_matches(wanted: str, known: dict[str, str], limit: int = 5) -> list[str]:
    """Catalogue ids sharing the most distinctive tokens with `wanted`.

    Token overlap rather than a prefix test: a rename usually keeps the family
    word and moves the version ("claude-fable-5.1" -> "claude-fable-5-1"), and a
    prefix test misses exactly that case. Provider and common version tokens are
    dropped so "anthropic" alone does not match the whole Anthropic catalogue.
    """
    noise = {"anthropic", "openai", "google", "meta", "x", "ai", "latest", "preview"}
    want = _tokens(wanted) - noise
    if not want:
        return []
    scored = []
    for model_id, name in known.items():
        shared = want & (_tokens(model_id) | _tokens(name))
        # A shared version number is not evidence: "gpt-6-astra" and
        # "claude-opus-4.6" both contain "6". Require at least one shared word.
        if not any(not tok.isdigit() for tok in shared):
            continue
        if shared:
            scored.append((len(shared), model_id))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [m for _, m in scored[:limit]]


def search_term_for(model_id: str) -> str:
    """The most distinctive word in a slug, for a --search suggestion.

    The longest alphabetic token in the final path segment: "gpt-6-astra"
    gives "astra", not "6", and "claude-fable-5.1" gives "fable", not "claude"
    (which would match the whole family).
    """
    generic = {"claude", "gpt", "gemini", "llama", "qwen", "grok", "deepseek"}
    words = [t for t in _tokens(model_id.split("/")[-1]) if not t.isdigit()]
    specific = [w for w in words if w not in generic]
    pool = specific or words
    return max(pool, key=len) if pool else model_id


def search(term: str, known: dict[str, str]) -> int:
    hits = sorted(
        model_id for model_id, name in known.items()
        if term.lower() in model_id.lower() or term.lower() in name.lower()
    )
    if not hits:
        print(f"no catalogue entry matches {term!r}.")
        print("the model may not be served by OpenRouter, or may be named")
        print("differently there -- try a shorter term.")
        return 1
    print(f"{len(hits)} match(es) for {term!r}:")
    for model_id in hits:
        label = known[model_id]
        print(f"  {model_id}" + (f"    ({label})" if label else ""))
    return 0


def main() -> int:
    args = sys.argv[1:]

    search_term = None
    if args and args[0] == "--search":
        if len(args) < 2:
            print("usage: python tools/check_models.py --search TERM")
            return 2
        search_term = args[1]
        args = args[2:]

    if search_term is not None:
        try:
            known = fetch_catalogue(os.environ.get("OPENROUTER_API_KEY"))
        except Exception as exc:
            print(f"could not reach OpenRouter: {exc}")
            return 2
        return search(search_term, known)

    roster_path = Path(args[0]) if args else ROOT / "tools" / "models.txt"
    if not roster_path.exists():
        print(f"roster not found: {roster_path}")
        return 2

    roster = read_roster(roster_path)
    if not roster:
        print("roster is empty")
        return 2

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("note: OPENROUTER_API_KEY unset -- the catalogue is public, so this")
        print("      still validates ids, but it will not confirm your key works.")

    try:
        known = fetch_catalogue(key)
    except Exception as exc:
        print(f"could not reach OpenRouter: {exc}")
        print("check the id list by hand at https://openrouter.ai/models")
        return 2

    try:
        tools = fetch_tool_support(key)
    except (OSError, ValueError, KeyError) as exc:
        print(f"  note: tool-support lookup unavailable ({exc}); ids only")
        tools = {}

    bad = []
    notools = []
    for model_id in roster:
        if model_id not in known:
            bad.append(model_id)
            print(f"  UNKNOWN  {model_id}")
            for candidate in near_matches(model_id, known):
                print(f"             maybe: {candidate}")
        elif tools and not tools.get(model_id, True):
            notools.append(model_id)
            print(f"  NO TOOLS {model_id}")
        else:
            print(f"  ok       {model_id}")

    print(f"\n{len(roster) - len(bad)} of {len(roster)} ids resolve.")
    if notools:
        print(f"{len(notools)} resolve but serve no tool-calling endpoint.")
        print("The solver is basic_agent(bash, text_editor), so these cannot")
        print("run a single episode -- OpenRouter answers 404 on the first")
        print("call with \"No endpoints found that support tool use\":")
        for model_id in notools:
            print(f"  {model_id}")
        print("Drop them from the roster. Otherwise the batch spends its")
        print("startup discovering this one model at a time, mid-run.")

    if bad:
        print("\nThe batch will not start until these resolve. To find one:")
        width = max(len(search_term_for(m)) for m in bad)
        for model_id in bad:
            term = search_term_for(model_id)
            print(f"  python tools/check_models.py --search {term:<{width}}"
                  f"   # for {model_id}")
        print(f"Then paste the real id over that line in {roster_path.name}.")

    return 1 if (bad or notools) else 0


if __name__ == "__main__":
    sys.exit(main())
