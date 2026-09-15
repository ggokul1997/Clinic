# Build 1 — Structured extraction + your first eval

Ships toward: **Competitor Intelligence Agent** (`PROJECT_BRIEF.md` §3C.1).

The agent's first job is to read a competitor clinic's page and come back with
facts a human can act on. Before it can monitor anything on a schedule, one pass
over one page has to be trustworthy. That's this build.

## Setup

```bash
pip install -r ai-lab/requirements.txt
```

Then credentials — one of:

```bash
setx ANTHROPIC_API_KEY "sk-ant-..."
```

(new shell after `setx`), or install the `ant` CLI and run `ant auth login`.
Never put the key in the code; the SDK finds it on its own.

## Run it

```bash
cd ai-lab/01-extraction && python extract.py fixtures/competitor-a.html
```

Then the part that matters:

```bash
cd ai-lab/01-extraction && python eval.py --trials 3
```

Roughly 8 calls, a few cents.

## What's in here

- `extract.py` — Pydantic schema → `client.messages.parse()` → validated object
- `eval.py` — 13 named checks, each run N times, scored as a pass **rate**
- `fixtures/` — two synthetic competitor pages with deliberate traps

## The MERN translation

| You know | Here it is |
|---|---|
| Mongoose schema | Pydantic model — but it's sent to the model as instructions, not just used to validate |
| `zod.parse()` on a response body | `messages.parse()` → `.parsed_output` |
| Jest `expect(x).toBe(y)` | a named check scored across N trials |
| A flaky test you rerun until green | a **bug**, and rerunning hides it |

## Concepts you'll collide with, in order

**1. The schema is the prompt.** Every `Field(description=...)` in `extract.py` is
text the model reads. When an extraction is wrong, sharpen the field description
before you touch the system prompt — it's a smaller, more targeted lever and it
travels with the field it governs.

**2. Nullable means nullable.** `price_inr: Optional[float]` plus "if no price is
published, use null — never estimate" is what stops Prolotherapy's "Contact us for
pricing" from becoming a confident invented number. Models fill gaps by default.
You have to explicitly license them not to.

**3. Evidence fields.** Every `Service` and `Claim` carries a verbatim `evidence`
quote. Two payoffs: it measurably cuts fabrication, because producing a quote that
must exist is harder than inventing a fact; and it makes the output auditable —
`evidence_is_verbatim` in the eval checks quotes against the actual page, which is
a fabrication detector you can run in CI. In a clinical product this is not optional.

**4. Traps.** The fixtures contain five things designed to be got wrong:

- a promo price (₹45,000) sitting next to the list price (₹60,000)
- "Cardiology" in the nav bar with no such service on the page
- "Contact us for pricing" where a number is expected
- `2,75,000` — Indian digit grouping, which is a genuine tokenization hazard
- a patient testimonial ("I lost 12 kg") shaped exactly like a clinic statistic

Traps are how you learn whether the model is reading or pattern-matching. Write
them from real failures once you have real pages.

**5. Pass rate, not pass.** `--trials 3` exists so you see the same input produce
different output. A check at 67% is not "mostly working." It is a defect that
fires on a third of your traffic.

## Exercises

1. **Run it at `--trials 5` and find the flaky checks.** Note which ones. That list
   is your actual product risk register.
2. **Fix a flake by editing only a field description.** Don't touch `SYSTEM`. Rerun.
   Did the rate move? This is the core loop of the job — change one thing, measure.
3. **Break it on purpose.** Delete the "NOT a limited-time promotional price"
   sentence from `price_inr`. Rerun. Watch `prp_list_price_not_promo` collapse.
   Now you know what that sentence was worth, in numbers.
4. **Swap the model.** Set `MODEL = "claude-haiku-4-5"` in `common/llm.py`. Rerun.
   Compare pass rate and spend. Nearly every real cost decision is this trade,
   and you should never make it by intuition.
5. **Add a fixture with a trap I didn't think of**, plus the checks that catch it.
   Writing eval cases is the skill; the extractor is the easy half.

## Where this goes

Build 4 turns this into an autonomous loop — fetch competitor URLs on a schedule,
diff against last week, surface only what changed. None of that is worth building
until one extraction is trustworthy, and "trustworthy" is a number `eval.py` prints.
