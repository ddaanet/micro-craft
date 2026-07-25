"""Shared loader: raters' verdicts plus run-1 labels, as feature rows.

Both `fit.py` and `evaluate.py` need the same table — one row per
labelled item, carrying the five metrics, the label, and the weight
that says how many corpus items the row stands for. Parsing it twice
would let the two scripts disagree about what the dataset is.
"""

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
RATERS = "ABCDEFG"
METRICS = ["comments", "reactions", "participants", "related_items", "span_years"]

BLOCK = re.compile(
    r"slot:\s*(\d+).*?verdict:\s*(signal|no-signal).*?"
    r"topic:\s*(\S+).*?confidence:\s*(high|medium|low)",
    re.DOTALL,
)


@dataclass
class Row:
    """One labelled item: its metrics, its label, and its sample weight."""

    number: int
    x: list[float]
    y: int
    weight: float
    block: str
    rater: str
    confidence: str
    topic: str
    score: float
    rank: int


def _verdicts() -> dict[int, dict[str, str]]:
    """Parse every rater's returned blocks, keyed by slot."""
    out: dict[int, dict[str, str]] = {}
    for rater in RATERS:
        path = HERE / f"verdicts-{rater}.md"
        if not path.exists():
            continue
        for chunk in re.split(r"\n(?=slot:)", path.read_text()):
            m = BLOCK.search(chunk)
            if m:
                slot, verdict, topic, conf = m.groups()
                out[int(slot)] = {
                    "verdict": verdict,
                    "topic": topic,
                    "confidence": conf,
                    "rater": rater,
                }
    return out


def load() -> tuple[list[Row], list[dict[str, object]], dict[int, dict[str, str]]]:
    """Return (fit rows, the sample with verdicts attached, verdicts by slot).

    The fit rows are the modelling population only: CONTRAST, PLATEAU
    and UNIFORM draws plus run 1's rank-uniform strata. CAL items are
    excluded because they are routed, so they are not part of the
    untriaged corpus the weights will rank. REPLICATE duplicates are
    excluded because a second opinion on an item already in the table
    is a measurement of the raters, not another draw from the corpus.
    """
    sample = json.loads((HERE / "sample.json").read_text())
    calls = _verdicts()
    for p in sample:
        call = calls.get(int(str(p["slot"])))
        if call:
            p["verdict"] = call["verdict"]
            p["confidence"] = call["confidence"]
            p["called_topic"] = call["topic"]
            p["rater"] = call["rater"]

    rows: list[Row] = []
    seen: set[int] = set()
    for p in sample:
        if p["block"] not in ("CONTRAST", "PLATEAU", "UNIFORM"):
            continue
        if "verdict" not in p or int(str(p["number"])) in seen:
            continue
        seen.add(int(str(p["number"])))
        rows.append(
            Row(
                number=int(str(p["number"])),
                x=[float(str(p[m])) for m in METRICS],
                y=int(p["verdict"] == "signal"),
                weight=float(str(p["weight"])),
                block=str(p["block"]),
                rater=str(p["rater"]),
                confidence=str(p["confidence"]),
                topic=str(p["called_topic"]),
                score=float(str(p["score"])),
                rank=int(str(p["rank"])),
            )
        )

    heat = {int(r["number"]): r for r in csv.DictReader(open(HERE / "heat.csv"))}
    prior = json.loads((HERE / "prior-labels.json").read_text())
    for num_s, lab in prior.items():
        num = int(num_s)
        if num in seen:
            continue
        seen.add(num)
        rows.append(
            Row(
                number=num,
                x=[float(lab[m]) for m in METRICS],
                y=int(lab["verdict"] == "signal"),
                weight=float(lab["weight"]),
                block="RUN1-" + str(lab["stratum"]),
                rater="1" + str(lab["rater"]),
                confidence=str(lab["confidence"]),
                topic=str(lab["topic"]),
                score=float(lab["score"]),
                rank=list(heat).index(num),
            )
        )
    return rows, sample, calls


def corpus_untriaged() -> list[dict[str, str]]:
    """The untriaged corpus rows, in heat order, from the CSV snapshot."""
    import sqlite3

    rows = list(csv.DictReader(open(HERE / "heat.csv")))
    con = sqlite3.connect(HERE.parents[3] / "corpus" / "cache.sqlite")
    routed = {
        n
        for (n,) in con.execute(
            "select i.number from route r join issue_or_pr i on i.id = r.item_id"
        )
    }
    return [r for r in rows if int(r["number"]) not in routed]
