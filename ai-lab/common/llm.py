"""Shared Claude client + the accounting habits you want from day one.

Two things live here that you would never bother with in a MERN service, and
both matter: every call costs money, and every call is non-deterministic.
"""
import anthropic

# The SDK resolves credentials itself: ANTHROPIC_API_KEY, or an `ant auth login`
# profile. Never take an api_key argument in application code.
client = anthropic.Anthropic()

MODEL = "claude-opus-5"

# USD per million tokens. Verify against the pricing page before you quote these
# to anyone -- rates change and a stale constant becomes a wrong invoice.
PRICING = {
    "claude-opus-5":  {"in": 5.00, "out": 25.00},
    "claude-sonnet-5": {"in": 2.00, "out": 10.00},
    "claude-haiku-4-5": {"in": 1.00, "out": 5.00},
}


def cost_usd(usage, model=MODEL) -> float:
    """Dollar cost of one response's uncached tokens."""
    rates = PRICING[model]
    return (usage.input_tokens * rates["in"] + usage.output_tokens * rates["out"]) / 1_000_000


def report(usage, model=MODEL) -> str:
    cached = getattr(usage, "cache_read_input_tokens", 0) or 0
    written = getattr(usage, "cache_creation_input_tokens", 0) or 0
    line = (f"  in={usage.input_tokens} out={usage.output_tokens} "
            f"cost=${cost_usd(usage, model):.4f}")
    if cached or written:
        line += f" [cache read={cached} write={written}]"
    return line
