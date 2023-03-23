import statistics

import matplotlib.pyplot as plt

from dk_analyzer.models import Event


def plot_graph(events: list[Event]) -> None:
    hp_list: list[float] = []
    rp_list: list[float] = []
    for event in events:
        if not event.is_cast_by_player():
            continue
        hp_list.append(event.hp_percent())
        rp_list.append(event.rp())

    plt.grid(zorder=-1.0)
    plt.scatter(
        x=rp_list,
        y=hp_list,
        marker="o",
        zorder=4.0,
    )
    plt.xlabel("RP")
    plt.ylabel("HP%")
    add_visual_aid()
    add_title(hp_list, rp_list)
    plt.show()


def add_visual_aid():
    plt.vlines(95, ymin=0, ymax=100, colors="#FE2A17", linewidth=3.0, zorder=3.0, label="95 RP")
    plt.hlines(70, xmin=35, xmax=95, colors="#FEBD0D", linewidth=3.0, zorder=2.0, label="70% HP")
    plt.fill_between([35, 95], 70, 100, color="black", alpha=0.1)


def add_title(hp_list: list[float], rp_list: list[float]) -> None:
    mean_rp = statistics.mean(rp_list)
    mean_hp = statistics.mean(hp_list)
    plt.title(f"DS Usage (mean RP: {round(mean_rp)}, mean HP: {round(mean_hp)}%)")
