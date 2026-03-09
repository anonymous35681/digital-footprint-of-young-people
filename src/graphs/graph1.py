import matplotlib.pyplot as plt
import pandas as pd

from config import OUTPUT_DIR, ROOT_DIR
from style import GRAY, GREEN, TEXT_COLOR


def run() -> None:
    """
    Generate graph1.png replicating the vertical bar chart style.
    Visualizes the share of graduates with 'overeducation' across top industries.
    """
    # Load dataset
    csv_path = ROOT_DIR / "data" / "raw" / "data_graduates_study_area_125_v20250709.csv"
    df = pd.read_csv(csv_path, sep=";")

    # Filter for total country, latest year (2024), and total gender
    df_plot = df[
        (df["object_level"] == "Страна")
        & (df["year"] == 2024)
        & (df["gender"] == "Всего")
    ].copy()

    # Drop NaNs and select Top 10 by graduate count to ensure data representativeness
    df_plot = df_plot.dropna(subset=["percent_employed"])
    df_plot = df_plot.sort_values("count_graduate", ascending=False).head(10)

    # Sort for visual flow (highest percentage on the left)
    df_plot = df_plot.sort_values("percent_employed", ascending=False)

    categories = df_plot["study_area"].tolist()
    values = df_plot["percent_employed"].tolist()
    avg_val = df_plot["percent_employed"].mean()

    # Append 'Average' benchmark
    categories.append("В среднем")
    values.append(avg_val)

    _fig, ax = plt.subplots(figsize=(14, 10), facecolor="#F0F0F0")
    ax.set_facecolor("#F0F0F0")

    x = range(len(categories))
    bar_width = 0.7

    for i, val in enumerate(values):
        # Draw the bar outline (empty part)
        ax.bar(
            x[i],
            100,
            width=bar_width,
            color="none",
            edgecolor=GRAY,
            linewidth=1.5,
            alpha=0.3,
        )
        # Draw the filled bar (Green)
        ax.bar(x[i], val, width=bar_width, color=GREEN, edgecolor=GREEN)

        # Vertical labels inside bars
        ax.text(
            x[i],
            2,
            categories[i],
            rotation=90,
            va="bottom",
            ha="center",
            color=TEXT_COLOR,
            fontsize=11,
            fontweight="bold",
        )

    # Horizontal average indicator
    ax.axhline(y=avg_val, color=GRAY, linestyle="--", linewidth=2, alpha=0.7)

    # Layout styling
    ax.set_ylim(0, 110)
    ax.set_xticks([])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(
        ["0", "25", "50", "75", "100%"], fontweight="bold", color=TEXT_COLOR
    )

    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_visible(False)

    # Titles and Meta Text
    plt.text(
        0,
        115,
        "Доля выпускников, работающих по специальности\n(ТОП-10 направлений подготовки)",
        fontsize=22,
        fontweight="extra bold",
        ha="left",
        va="top",
        color=TEXT_COLOR,
    )

    plt.text(
        0,
        -10,
        "Доля выпускников, чья текущая деятельность соответствует уровню и профилю\n"
        "полученного образования (по данным Мониторинга 2024 г.).",
        fontsize=12,
        ha="left",
        color=TEXT_COLOR,
    )

    plt.text(
        0,
        -18,
        "Источник: мониторинг трудоустройства выпускников Роструда.\n"
        "Проект «Если быть точным».",
        fontsize=10,
        ha="left",
        color=TEXT_COLOR,
    )

    plt.tight_layout(rect=(0.0, 0.1, 1.0, 0.9))
    plt.savefig(OUTPUT_DIR / "graph1.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    run()
