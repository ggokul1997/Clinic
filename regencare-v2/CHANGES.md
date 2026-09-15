# Regencare — Design 2, revised

Base: `desings/RegenCare Design 2.html` (chosen over the other four; see rationale below).
`index.before.html` is the unmodified extraction, for side-by-side comparison.

## Why Design 2 was the pick

- Its nav had already dropped the internal label "Our verticals".
- Its copy already carried the surgery-avoidance thesis — *"Most people are offered
  two choices. Live with it, or have surgery."* — which speaks to the highest-value
  patient segment. That insight was already there; it needed promoting, not inventing.
- It already had an `#evidence` section, "The record behind the practice".
- It leads with mechanism honesty ("It is not a new drug. It is your own biology")
  rather than "harness your body's healing" mysticism.
- Design 3 was rejected mainly for AI-generated sci-fi imagery (glowing wireframe knee,
  particle face) — the wrong register for a clinic whose constraint is credibility.
- Design 1 (v1/v2/v3) kept the current site's institutional nav and generic headline.

## Structural repairs (these were broken before any UX work)

1. **The page did not run.** Its only script was `class Component extends DCLogic` —
   a design-tool React runtime shipped as a gzipped `.bin` that a normal server
   serves raw, so the browser threw `SyntaxError` and *nothing* executed: no hero
   carousel, no counters, no rail, no mobile menu. Replaced with ~9 KB of
   self-contained vanilla JS. External dependency removed.
2. **Unresolved template syntax.** `<sc-if value="{{ menuOpen }}">` and
   `sc-camel-on-click="{{ toggleMenu }}"` are builder directives, not HTML. The mobile
   menu is now real markup with a working toggle and `aria-expanded`.
3. **Broken SVG grain filter.** The builder mangled `baseFrequency` into
   `sc-camel-base-frequency`, so the hero texture never rendered. Unmangled.
4. **22 MB single file → editable folder.** Markup was JSON-encoded inside a bundler
   wrapper with 53 assets keyed by UUID. Extracted to `index.html` + `assets/`.

## UX and IA changes (from the Candidacy-First assessment)

| # | Change |
|---|--------|
| 1 | **Utility bar** with WhatsApp primacy, a published response window ("within 15 minutes, 8am–9pm IST"), the three centres, and an EN / മലയാളം / தமிழ் switcher |
| 2 | **Nav inverted to condition-first**: Conditions · How it works · Treatments & evidence · Results · Our doctors · Visiting us. "Stories" removed |
| 3 | **The fork** — Orthopaedics / Dermatology as equal choices, plus "Already have an MRI or scan report?" → report review |
| 4 | **Condition tiles** in patient language (knee osteoarthritis, hip AVN, hair loss…) instead of procedure acronyms |
| 5 | **Evidence tiers** on all seven procedures — Established / Emerging / Investigational — with a legend, encoded in shape *and* colour, not colour alone |
| 6 | **Outcomes table** added to "The record behind the practice": patients treated, mean change on a named instrument, follow-up duration, loss to follow-up, onward-surgery rate |
| 7 | **Testimonials replaced** by a candidacy router ("usually worth assessing" / "usually not, and we will say so") |
| 8 | **Diabetic foot ulcer fast path** — the one time-sensitive exception, with same-day contact |
| 9 | **Practical questions** block: cost, insurance reality, session counts, recovery, out-of-station and overseas patients |
| 10 | **A real booking form** — there was none, only a newsletter input. Now captures who-it-is-for (proxy enquiries are common), centre, vertical, and a preference window rather than a raw `YYYY-MM-DD` date, with a DPDP-shaped consent notice |
| 11 | Button reads **"Request a callback"**, not "Book" — a person answers it. The label is a promise |
| 12 | **Palette**: pure `#ff0000` → `#C0261B`. White-on-red went from 3.99:1 (fails AA) to **5.94:1**. Logo untouched |
| 13 | **Accessibility floor** for the 55–75 cohort: 17px body, 44–60px targets, visible focus rings, `prefers-reduced-motion` honoured, content visible at rest |
| 14 | Hero no longer `100vh`; sized to content. Patient count added to the credibility line |

## Verified

- Console clean, no errors. Single script, no external dependencies.
- Contrast: body 19.4:1 · CTA 5.94:1 · evidence tiers 5.81 / 6.36 / 6.28 — all pass AA.
- One `h1`. Form blocks on empty submit with a useful message; confirms when valid;
  status announced via `role="status"`.
- Mobile at 375px: no horizontal overflow, every grid collapses to one column,
  desktop nav hidden, WhatsApp still visible.

## Still needs a human decision

1. **Evidence tier assignments are placeholders.** Dr Vineeth and Dr Aswathi must set
   them, with legal review. ICMR's 2017 guidelines classify non-haematopoietic stem
   cell use as investigational; the stem cell, SVF and cultured-osteoblast pages need
   restructuring around that before this goes live.
2. **Outcomes table is empty** (`to fill` markers). Needs the ten-year dataset.
   If follow-up data is not extractable, publish a smaller honest version.
3. **Condition tiles link to the booking form**, as placeholders. Each needs its own
   page with candidacy criteria, session count, timeline, cost range, evidence tier.
4. **Cost and insurance answers** are marked `to fill` in the practical block.
5. **Form needs a backend**, file upload for imaging, and a retention policy.
6. **Malayalam and Tamil** switchers are inert placeholders — human translation only,
   never machine translation, for clinical content.
