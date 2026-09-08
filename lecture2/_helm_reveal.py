"""SPOILER: Allocation Helm scoring. Open only after freezing a submission.

Adapted from abstractapplic (H-B-P), public-domain source:
https://github.com/H-B-P/d-and-d-sci-sep-2022/blob/main/gen.py
See data/ALLOCATION_HELM_LICENSE. These offsets match the generator and
interactive's score table; the LessWrong prose has different Serpentyne offsets.
"""

import numpy as np
import pandas as pd
from IPython.display import Markdown, display

HOUSES = ("Dragonslayer", "Thought-Talon", "Serpentyne", "Humblescrumble")


def expected_ratings(students):
    """Return the author's expected outcome for every student and House."""
    intellect, integrity, courage, reflexes, patience = (
        students[column].to_numpy(dtype=float)
        for column in ("Intellect", "Integrity", "Courage", "Reflexes", "Patience")
    )
    potentials = np.column_stack([
        np.maximum(
            5 * (np.minimum.reduce([intellect, integrity, courage, reflexes, patience]) - 1),
            3 * np.minimum(courage - 9, reflexes + 9),
        ),
        np.maximum(
            5 * (np.minimum.reduce([intellect, integrity, courage, patience]) - 3),
            3 * np.minimum(intellect - 4, patience + 4),
        ),
        np.maximum(
            3 * np.minimum(intellect + 7, reflexes - 7),
            3 * np.minimum(intellect + 8, patience - 8),
        ),
        np.maximum(
            3 * np.minimum(integrity - 6, intellect + 6),
            35 + np.maximum(patience, integrity),
        ),
    ])
    # The original generator rolls range(Potential) dice: negative values roll none.
    return pd.DataFrame(np.maximum(potentials, 0) / 4, index=students.index, columns=HOUSES)


def reveal(allocation, incoming):
    if (allocation.index.has_duplicates or set(allocation.index) != set(incoming.index)
            or not allocation["House"].isin(HOUSES).all()):
        raise ValueError("Expected one valid House choice for each incoming student")
    expected = expected_ratings(incoming)
    table = allocation.loc[incoming.index].copy(deep=True)
    indices = [HOUSES.index(house) for house in table["House"]]
    table["Expected rating"] = expected.to_numpy()[np.arange(len(table)), indices]
    table["Best possible rating"] = expected.max(axis=1)
    table["Regret"] = table["Best possible rating"] - table["Expected rating"]
    display(Markdown("""
### The revealed rule

Each House offers two possible potentials; a student receives the larger one.
Expected rating is nonnegative potential divided by four. Historical ratings
include random variation; this final score uses the expectation.

Let I = Intellect, G = Integrity, C = Courage, R = Reflexes, P = Patience.

| House | First potential | Second potential |
|---|---|---|
| Dragonslayer | 5 × (min(I,G,C,R,P) − 1) | 3 × min(C−9, R+9) |
| Thought-Talon | 5 × (min(I,G,C,P) − 3) | 3 × min(I−4, P+4) |
| Serpentyne | 3 × min(I+7, R−7) | 3 × min(I+8, P−8) |
| Humblescrumble | 3 × min(G−6, I+6) | 35 + max(P,G) |

Scoring follows the author's [generator and interactive](https://github.com/H-B-P/d-and-d-sci-sep-2022),
whose Serpentyne offsets differ from the prose in the
[published explanation](https://www.lesswrong.com/posts/wNPSFgcB93wLhgbKh/d-and-d-sci-september-2022-evaluation-and-ruleset).
"""))
    return {
        "class_rating": float(table["Expected rating"].mean()),
        "random_reference": float(expected.to_numpy().mean()),
        "optimal_reference": float(expected.max(axis=1).mean()),
        "table": table,
    }
