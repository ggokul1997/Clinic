"""Build 1 -- the eval harness. This file is the actual lesson.

`assert extract(page) == expected` cannot work: the model is sampling, so two
identical calls can differ. What replaces it is a set of named checks run N
times, scored as a pass RATE rather than a boolean.

Run:  python ai-lab/01-extraction/eval.py --trials 3
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.llm import MODEL, client, cost_usd  # noqa: E402
from extract import CompetitorProfile, html_to_text  # noqa: E402

HERE = Path(__file__).parent


def _service(p: CompetitorProfile, needle: str):
    """First service whose name contains `needle` (case-insensitive), or None."""
    return next((s for s in p.services if needle.lower() in s.name.lower()), None)


def _mentions(items, needle: str) -> bool:
    return any(needle.lower() in str(i).lower() for i in items)


# ---------------------------------------------------------------------------
# Checks. Each is (name, predicate). A predicate returns True if the extraction
# got this specific thing right. Write them one per failure mode you care about,
# not one per field -- you are testing behaviour, not serialisation.
#
# Several of these target deliberate traps in the fixtures. Traps are how you
# find out whether the model is reading or pattern-matching.
# ---------------------------------------------------------------------------

CHECKS = {
    "competitor-a.html": [
        ("prp_list_price_not_promo",
         lambda p: (s := _service(p, "PRP")) is not None and s.price_inr == 60000,
         "PRP list price is Rs 60,000; Rs 45,000 is a limited-time offer"),

        ("promo_captured_separately",
         lambda p: _mentions(p.promotions, "45,000") or _mentions(p.promotions, "monsoon"),
         "the discount belongs in promotions, not in the price field"),

        ("cardiology_not_invented",
         lambda p: _service(p, "cardio") is None,
         "cardiology appears only in the nav bar -- not evidence of a service"),

        ("missing_price_stays_null",
         lambda p: (s := _service(p, "Prolotherapy")) is not None and s.price_inr is None,
         "'Contact us for pricing' must not become a number"),

        ("stemcell_course_price",
         lambda p: (s := _service(p, "Stem Cell")) is not None and s.price_inr == 275000,
         "Indian digit grouping: 2,75,000 is 275000, not 2750"),

        ("satisfaction_claim_found",
         lambda p: _mentions([c.text for c in p.claims], "98"),
         "the 98% satisfaction stat is a genuine clinic claim"),

        ("testimonial_not_a_claim",
         lambda p: not _mentions([c.text for c in p.claims], "12 kg"),
         "a patient anecdote is not a claim by the clinic"),

        ("evidence_is_verbatim",
         lambda p: all(s.evidence.strip()[:25].lower() in _page("competitor-a.html").lower()
                       for s in p.services if s.evidence.strip()),
         "quoted evidence must actually appear on the page"),
    ],
    "competitor-b.html": [
        ("exosome_price",
         lambda p: (s := _service(p, "Exosome")) is not None and s.price_inr == 180000,
         None),

        ("iv_price",
         lambda p: (s := _service(p, "IV Nutrient")) is not None and s.price_inr == 9500,
         None),

        ("peptide_not_yet_available",
         lambda p: (s := _service(p, "Peptide")) is not None
                   and s.availability == "announced_not_yet_available",
         "'Launching Jan 2027' is a roadmap item, not a bookable service"),

        ("peptide_price_null",
         lambda p: (s := _service(p, "Peptide")) is not None and s.price_inr is None,
         None),

        ("pain_score_claim",
         lambda p: _mentions([c.text for c in p.claims], "61"),
         None),
    ],
}

_page_cache = {}


def _page(name: str) -> str:
    if name not in _page_cache:
        _page_cache[name] = html_to_text(HERE / "fixtures" / name)
    return _page_cache[name]


def run_once(name: str) -> tuple[CompetitorProfile, float]:
    from extract import SYSTEM
    response = client.messages.parse(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"<page source=\"{name}\">\n{_page(name)}\n</page>"}],
        output_format=CompetitorProfile,
    )
    return response.parsed_output, cost_usd(response.usage)


def main(trials: int) -> int:
    results = defaultdict(list)   # (fixture, check) -> [bool, ...]
    spend = 0.0

    for fixture, checks in CHECKS.items():
        print(f"\n{fixture}  ({trials} trial{'s' if trials > 1 else ''})")
        for t in range(trials):
            profile, c = run_once(fixture)
            spend += c
            for check_name, predicate, _ in checks:
                try:
                    ok = bool(predicate(profile))
                except Exception:
                    ok = False          # a crashing grader is a failing grader
                results[(fixture, check_name)].append(ok)
            print(f"  trial {t + 1} done", file=sys.stderr)

        for check_name, _, why in checks:
            runs = results[(fixture, check_name)]
            rate = sum(runs) / len(runs)
            mark = "PASS" if rate == 1 else ("FLAKY" if rate > 0 else "FAIL")
            print(f"  [{mark:5}] {rate:>4.0%}  {check_name}")
            if rate < 1 and why:
                print(f"           -> {why}")

    all_runs = [r for runs in results.values() for r in runs]
    flaky = sum(1 for runs in results.values() if 0 < sum(runs) / len(runs) < 1)
    print(f"\noverall {sum(all_runs)}/{len(all_runs)} checks passed"
          f"  |  {flaky} flaky  |  spend ${spend:.4f}")
    if flaky:
        print("\nFlaky checks are the interesting ones. A check that passes 2 of 3 times\n"
              "is not 'mostly working' -- in production it is a bug that fires on a third\n"
              "of your traffic, and no amount of rerunning makes it a pass.")
    return 0 if all_runs and flaky == 0 and all(all_runs) else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3,
                    help="runs per fixture; >1 is how you see non-determinism")
    sys.exit(main(ap.parse_args().trials))
