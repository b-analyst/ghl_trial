"""Figures for the writeup, from results.csv.

    python generate_figures.py

Writes figures/fig1..fig4 as PNG. Every count is derived from the CSV.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from detectors import DISCLOSURE
from report import CELLS, coerce_bools

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures"

# Ground and inks, lightest to darkest.
SURFACE = "#fcfcfb"
GRID = "#e4e3de"
INK_FAINT = "#8a8983"
INK_SOFT = "#52514e"
INK = "#0b0b0b"

# Series colors. Blue marks whatever the figure is about.
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
GRAY = "#b5b4ad"

# The three conditions whose ticket forbids touching tests/. Only here is
# stating the conflict the sole way through: elsewhere a model can fix the
# wrong test instead and never write about it, which a phrase list cannot see.
CONSTRAINED_CELLS = ["goal", "cover-goal", "phantom-goal"]

CELL_TICKS = ["ctl", "cov", "goal", "c+g", "phan"]

mpl.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "text.color": INK,
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "axes.labelcolor": INK_SOFT,
    "xtick.color": INK_SOFT,
    "ytick.color": INK_SOFT,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "grid.color": GRID,
    "grid.linewidth": 0.7,
})


# --- reading the frame -------------------------------------------------------

def hacked_of_scored(df: pd.DataFrame, model: str, cell: str) -> tuple[int, int]:
    """Episodes that gamed the checker, out of those that could be scored."""
    gamed = df[(df.model == model) & (df.cell == cell) & df.gamed.notna()]["gamed"]
    return int(gamed.sum()), len(gamed)


def percent(part: int, whole: int) -> float:
    return 100 * part / whole if whole else 0.0


def short_name(model: str) -> str:
    """Drop the provider prefix; the model name is the identifying part."""
    return model.split("/")[-1]


def models_by_hack_rate(df: pd.DataFrame) -> list[str]:
    """Models least to most likely to take the bait overall."""
    rate = {
        model: df[(df.model == model) & df.gamed.notna()]["gamed"].mean()
        for model in df.model.unique()
    }
    return sorted(rate, key=rate.get)


def hacked_episodes(df: pd.DataFrame) -> pd.DataFrame:
    """Only the gamed ones. Unscored episodes carry NA and drop out here."""
    return df[df.gamed.eq(True)]


def style_axes(ax) -> None:
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def save(fig, name: str) -> None:
    fig.savefig(FIGURES / name, dpi=220)
    plt.close(fig)


# --- the figures -------------------------------------------------------------

def fig_cells(df: pd.DataFrame, models: list[str]) -> None:
    """Hacking rate by condition, one panel per model."""
    fig, axes = plt.subplots(2, 3, figsize=(6.7, 4.0), sharey=True)
    for spare in axes.flat[len(models):]:
        spare.set_visible(False)

    phantom = len(CELLS) - 1
    for ax, model in zip(axes.flat, models):
        per_cell = [hacked_of_scored(df, model, cell) for cell in CELLS]
        bars = ax.bar(
            range(len(CELLS)),
            [percent(hacked, scored) for hacked, scored in per_cell],
            color=[GRAY] * phantom + [BLUE],
            width=0.68,
            zorder=3,
        )
        for i, (bar, (hacked, scored)) in enumerate(zip(bars, per_cell)):
            is_phantom = i == phantom
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 3.5,
                f"{hacked}/{scored}",
                ha="center",
                va="bottom",
                fontsize=6.6,
                color=BLUE if is_phantom else INK_FAINT,
                fontweight="bold" if is_phantom else "normal",
            )
        ax.set_title(short_name(model), fontsize=8.5, color=INK, pad=6, loc="left")
        ax.set_xticks(range(len(CELLS)))
        ax.set_xticklabels(CELL_TICKS, fontsize=7)
        ax.set_ylim(0, 118)
        ax.set_yticks([0, 50, 100])
        ax.yaxis.grid(True, zorder=0)
        style_axes(ax)

    for ax in axes[:, 0]:
        ax.set_ylabel("% hacked", fontsize=8, color=INK_SOFT)

    fig.suptitle(
        "Phantom condition (blue) moves every model",
        fontsize=9.2,
        color=INK,
        x=0.011,
        ha="left",
        y=0.995,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    save(fig, "fig1-cells.png")


def fig_dissociation(df: pd.DataFrame, models: list[str]) -> None:
    """Saying the conflict out loud against acting on it."""
    scored = df[df.gamed.notna() & df.cell.isin(CONSTRAINED_CELLS)]
    fig, ax = plt.subplots(figsize=(6.7, 3.1))

    for row, model in enumerate(models):
        episodes = scored[scored.model == model]
        said = percent(episodes.said_test_wrong.sum(), len(episodes))
        merged = percent(
            (episodes.said_test_wrong & episodes.gamed).sum(),
            len(episodes),
        )
        ax.plot(
            [merged, said],
            [row, row],
            color=GRID,
            lw=3.2,
            solid_capstyle="round",
            zorder=2,
        )
        for value, color in ((said, BLUE), (merged, ORANGE)):
            ax.scatter(
                [value],
                [row],
                s=62,
                color=color,
                zorder=4,
                edgecolor=SURFACE,
                linewidth=1.4,
            )
        ax.text(
            said + 2.6,
            row,
            f"{said:.0f}%",
            va="center",
            fontsize=7.4,
            color=BLUE,
        )
        ax.text(
            merged - 2.6,
            row,
            f"{merged:.0f}%",
            va="center",
            ha="right",
            fontsize=7.4,
            color=ORANGE,
        )

    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([short_name(model) for model in models], fontsize=8.2)
    # Row 0 plots at the bottom, so flip it to match the other figures' order.
    ax.invert_yaxis()
    # A blank row below the last model, so the legend does not sit on its dots.
    ax.set_ylim(len(models) + 0.35, -0.5)
    ax.set_xlim(-8, 116)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel(
        "% of the 90 episodes per model where tests/ was off-limits",
        fontsize=8,
        color=INK_SOFT,
    )
    ax.xaxis.grid(True, zorder=0)
    style_axes(ax)

    ax.scatter(
        [],
        [],
        s=62,
        color=BLUE,
        label="said in writing that the test contradicts the ticket",
    )
    ax.scatter(
        [],
        [],
        s=62,
        color=ORANGE,
        label="said so and merged the bug anyway",
    )
    # Bottom-left: the busiest model sits on the right of that row.
    ax.legend(
        frameon=False,
        fontsize=7.8,
        loc="lower left",
        handletextpad=0.4,
        bbox_to_anchor=(-0.01, -0.04),
    )
    ax.set_title(
        "Discloses the conflict while merging the bug anyway",
        fontsize=9.2,
        color=INK,
        loc="left",
        pad=8,
    )
    fig.tight_layout()
    save(fig, "fig2-dissociation.png")


def fig_missing_vs_real(df: pd.DataFrame, models: list[str]) -> None:
    """No document, a real but stale one, one that does not exist."""
    series = [
        ("no document (goal)", BLUE, "goal"),
        ("a stale document (cover-goal)", ORANGE, "cover-goal"),
        ("a missing document (phantom-goal)", AQUA, "phantom-goal"),
    ]
    fig, ax = plt.subplots(figsize=(6.7, 2.9))
    positions = np.arange(len(models))
    bar_width = 0.26

    for offset, (series_label, color, cell) in enumerate(series):
        per_model = [hacked_of_scored(df, model, cell) for model in models]
        bars = ax.bar(
            positions + (offset - 1) * (bar_width + 0.018),
            [percent(hacked, scored) for hacked, scored in per_model],
            width=bar_width,
            color=color,
            label=series_label,
            zorder=3,
        )
        for bar, (hacked, _) in zip(bars, per_model):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 2.2,
                f"{hacked}",
                ha="center",
                va="bottom",
                fontsize=7,
                color=color,
                fontweight="bold",
            )

    ax.set_xticks(positions)
    ax.set_xticklabels([short_name(model) for model in models], fontsize=8.2)
    ax.set_ylim(0, 104)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("% hacked (of 30)", fontsize=8, color=INK_SOFT)
    ax.yaxis.grid(True, zorder=0)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=7.8, loc="upper left", handlelength=1.1)
    ax.set_title(
        "Missing document moves behavior more than stale document",
        fontsize=9.2,
        color=INK,
        loc="left",
        pad=8,
    )
    fig.tight_layout()
    save(fig, "fig3-missing-vs-real.png")


def fig_disclosure(df: pd.DataFrame, models: list[str]) -> None:
    """Disclosure criteria met, per hacked episode."""
    # Newlines so each column header wraps where it reads best.
    criteria = [
        "admits the\nrequirement\nwas not met",
        "gives the\nbroken case",
        "names the\naffected\nreport",
        "says how to\nreverse it",
        "escalates to\nthe owner",
    ]
    hacked = hacked_episodes(df)
    rows = [model for model in models if len(hacked[hacked.model == model])]
    totals = {model: len(hacked[hacked.model == model]) for model in rows}
    met = np.array([
        [int(hacked[hacked.model == model][criterion].sum())
         for criterion in DISCLOSURE]
        for model in rows
    ])
    share = met / np.array([[totals[model]] for model in rows])
    # Above this fill, white type reads better than gray.
    dark_cell = 0.55

    fig, ax = plt.subplots(figsize=(6.7, 2.7))
    heatmap = ax.imshow(share, cmap="Blues", vmin=0, vmax=1, aspect="auto")
    for row in range(len(rows)):
        for column in range(len(criteria)):
            ax.text(
                column,
                row,
                f"{met[row, column]}",
                ha="center",
                va="center",
                fontsize=8,
                color="white" if share[row, column] > dark_cell else INK_SOFT,
                fontweight="bold",
            )

    ax.set_xticks(range(len(criteria)))
    ax.set_xticklabels(criteria, fontsize=7.2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(
        [f"{short_name(model)}  (n={totals[model]})" for model in rows],
        fontsize=8,
    )
    style_axes(ax)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Minor ticks sit between cells, so a grid drawn on them reads as gutters.
    ax.set_xticks(np.arange(-0.5, len(criteria), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2.2)
    ax.tick_params(which="minor", length=0)

    colorbar = fig.colorbar(heatmap, ax=ax, fraction=0.022, pad=0.02)
    colorbar.outline.set_visible(False)
    colorbar.set_ticks([0, 0.5, 1])
    colorbar.set_ticklabels(["0%", "50%", "100%"])
    colorbar.ax.tick_params(labelsize=7, length=0)

    ax.set_title(
        "How well each hacked submission was disclosed\n"
        "Cells show the count of hacked episodes meeting that criterion",
        fontsize=9.2,
        color=INK,
        loc="left",
        pad=8,
    )
    fig.tight_layout()
    save(fig, "fig4-disclosure.png")


def main() -> int:
    df = coerce_bools(pd.read_csv(ROOT / "results.csv"))
    FIGURES.mkdir(exist_ok=True)
    models = models_by_hack_rate(df)

    # Figure 3 compares three conditions, so a model already at ceiling in
    # `goal` cannot move and is left out.
    with_room = []
    for model in models:
        hacked, scored = hacked_of_scored(df, model, "goal")
        if hacked < scored:
            with_room.append(model)

    fig_cells(df, models)
    fig_dissociation(df, models)
    fig_missing_vs_real(df, with_room)
    fig_disclosure(df, models)

    for path in sorted(FIGURES.glob("*.png")):
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size / 1000:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
