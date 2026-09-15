"""Build 1 -- Competitor Intelligence Agent, step one: structured extraction.

Run:  python ai-lab/01-extraction/extract.py fixtures/competitor-a.html
"""
import json
import sys
from pathlib import Path
from typing import List, Literal, Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.llm import MODEL, client, report  # noqa: E402


# ---------------------------------------------------------------------------
# The schema IS the prompt.
#
# Every `description` below is instruction text the model actually reads. This
# is the highest-leverage surface in the whole file: nine times out of ten a bad
# extraction is fixed by sharpening a field description, not by rewriting the
# system prompt.
# ---------------------------------------------------------------------------

class Service(BaseModel):
    name: str = Field(description="The treatment or programme name as the clinic writes it.")
    price_inr: Optional[float] = Field(
        description=(
            "Standard list price in INR for the unit described in `price_basis`. "
            "Use the clinic's own regular price, NOT a limited-time promotional or "
            "discounted price. If no price is published, use null -- never estimate."
        )
    )
    price_basis: Optional[str] = Field(
        description="What the price buys, e.g. 'per session', 'full 3-session course'. Null if no price."
    )
    availability: Literal["available", "announced_not_yet_available"] = Field(
        description=(
            "'available' if patients can book it today. "
            "'announced_not_yet_available' for anything marked coming soon, launching, or with a future start date."
        )
    )
    evidence: str = Field(
        description="A short VERBATIM quote from the page that supports this entry. Copy exactly; do not paraphrase."
    )


class Claim(BaseModel):
    text: str = Field(description="The claim, stated concisely.")
    kind: Literal["outcome_statistic", "credential", "differentiator"] = Field(
        description="What sort of claim this is."
    )
    evidence: str = Field(description="VERBATIM quote from the page.")


class CompetitorProfile(BaseModel):
    """Everything worth knowing about one competitor clinic page.

    Only record what the page actually states. An empty list is a correct and
    useful answer; an invented entry is not.
    """
    clinic_name: str
    city: Optional[str] = Field(description="City of operation, null if not stated.")
    services: List[Service]
    claims: List[Claim] = Field(
        description=(
            "Claims made BY THE CLINIC about itself. Do NOT include patient "
            "testimonials or quoted patient experiences -- those are anecdotes, not clinic claims."
        )
    )
    promotions: List[str] = Field(
        description="Any limited-time offer or discount, quoted verbatim. Empty list if none."
    )


SYSTEM = """You are a competitive intelligence analyst for a regenerative medicine clinic.

You read a competitor's public web page and extract only what it verifiably states.

Rules:
- Ground every entry in text that is actually on the page. If it is not there, it does not exist.
- A service mentioned only in navigation or a menu is NOT evidence that the service is offered.
- Never infer, average, or estimate a price.
- Prefer omitting an uncertain entry over including a wrong one."""


def html_to_text(path: Path) -> str:
    """Strip markup. Tags are tokens you pay for and the model rarely needs them.

    Tradeoff worth knowing: you lose structural signal (a `class="promo-banner"`
    told you that price was promotional). When extraction quality depends on
    layout, send the HTML. Here the words carry it.
    """
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return soup.get_text(separator="\n", strip=True)


def extract(path: Path) -> CompetitorProfile:
    page = html_to_text(path)
    response = client.messages.parse(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"<page source=\"{path.name}\">\n{page}\n</page>"}],
        output_format=CompetitorProfile,
    )
    print(report(response.usage), file=sys.stderr)
    return response.parsed_output


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fixtures/competitor-a.html")
    if not target.is_absolute() and not target.exists():
        target = Path(__file__).parent / target
    profile = extract(target)
    print(json.dumps(profile.model_dump(), indent=2, ensure_ascii=False))
