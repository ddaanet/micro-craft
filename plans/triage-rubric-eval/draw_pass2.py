"""Draw the blinded pass-2 slice and render its worksheet.

Pass 2 measures recall, which is invisible to pass 1: you cannot grade a
route that was never made. The only place a recall failure can hide is
the set of items a Sonnet rater called `no-signal`, so the slice is
weighted there, with `signal` items mixed in as controls — a one-sided
pile drifts a human labeller lenient.

Writes `worksheet.md` (blinded, for my human partner) and `slice.json`
(the key, holding each item's Sonnet verdict). Reading the key before
labelling defeats the measurement.
"""

import json
import random
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
CALIB = HERE.parent.parent / "tools/ghmem/calibration/weights-2026-07-25"
SEED = 20260908
N_NO_SIGNAL, N_SIGNAL = 16, 6

# Named in `findings.md` and in both rubrics as the canonical
# under-harvesting miss, so its verdict is not blind to a labeller who
# has read either. Excluding it costs a slot; keeping it costs the slot
# anyway and buys a label that measures nothing.
CONTAMINATED = {1445}

BLOCK = re.compile(
    r"slot:\s*(\d+)\s*\nnumber:\s*(\d+).*?verdict:\s*(signal|no-signal).*?"
    r"topic:\s*(\S+).*?confidence:\s*(high|medium|low).*?why:\s*(.*?)\n",
    re.DOTALL,
)


def calibration_labels() -> dict[int, list[dict[str, str]]]:
    """Merge the seven raters' verdicts with run 1's pooled labels."""
    rows: dict[int, list[dict[str, str]]] = {}
    for rater in "ABCDEFG":
        text = (CALIB / f"verdicts-{rater}.md").read_text()
        for m in BLOCK.finditer(text):
            rows.setdefault(int(m.group(2)), []).append(
                {
                    "rater": rater,
                    "verdict": m.group(3),
                    "topic": m.group(4),
                    "confidence": m.group(5),
                    "why": m.group(6).strip(),
                }
            )
    for number, row in json.loads((CALIB / "prior-labels.json").read_text()).items():
        rows.setdefault(int(number), []).append(
            {
                "rater": row.get("rater", "?"),
                "verdict": row["verdict"],
                "topic": row.get("topic", "-"),
                "confidence": row.get("confidence", "?"),
                "why": "(run-1 pooled label)",
            }
        )
    return rows


def draw(rows: dict[int, list[dict[str, str]]]) -> list[int]:
    """Sample the slice, weighted toward the recall-critical cell."""
    verdicts = {
        n: {label["verdict"] for label in ls}
        for n, ls in rows.items()
        if n not in CONTAMINATED
    }
    no_signal = sorted(n for n, v in verdicts.items() if v == {"no-signal"})
    signal = sorted(n for n, v in verdicts.items() if v == {"signal"})
    split = sorted(n for n, v in verdicts.items() if len(v) > 1)
    rng = random.Random(SEED)
    picked = rng.sample(no_signal, N_NO_SIGNAL) + rng.sample(signal, N_SIGNAL) + split
    rng.shuffle(picked)
    return picked


def render(number: int) -> str:
    """Render one item's whole thread, read-only."""
    for cmd in (["ghmem", "show"], ["ghmem", "discussion"]):
        done = subprocess.run([*cmd, str(number)], capture_output=True, text=True)
        if done.returncode == 0:
            return done.stdout
    return f"(could not render #{number})"


HEADER = """# Pass 2 worksheet — hand-labelled ground truth

Read each thread to its end and record a verdict. The Sonnet rater's own
verdict is deliberately withheld; it is in `slice.json`, which is the key.

The rubric is `tools/ghmem/calibration/weights-2026-07-25/rubric.md` —
the same one the raters saw. In short: **would a triage pass extract
anything a topic doc would use?** A decision, a rationale, a contested
position, or durable evidence for an open question is `signal`. A bare
bug report, a mechanical change, a support question, a dead one-liner,
or an unengaged feature request is `no-signal`.

Fill in the `verdict:` and `why:` lines below each thread. Leave
`confidence:` as one of high / medium / low — a slot full of `low` is
itself a finding.
"""


def main() -> None:
    rows = calibration_labels()
    picked = draw(rows)
    key = [{"slot": i, "number": n, "raters": rows[n]} for i, n in enumerate(picked, 1)]
    (HERE / "slice.json").write_text(json.dumps(key, indent=1) + "\n")

    parts = [HEADER]
    for slot, number in enumerate(picked, 1):
        parts.append(
            f"\n---\n\n## slot {slot} — #{number}\n\n"
            f"{render(number).strip()}\n\n"
            f"```\nslot: {slot}\nnumber: {number}\n"
            f"verdict: \ntopic: \nconfidence: \nwhy: \n```\n"
        )
    (HERE / "worksheet.md").write_text("".join(parts))
    print(f"{len(picked)} slots -> worksheet.md, key -> slice.json")


if __name__ == "__main__":
    main()
