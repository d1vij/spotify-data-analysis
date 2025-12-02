import seaborn as sns
import matplotlib.pyplot as plt


def double_lineplot(
    x1,
    y1,
    label_1,
    color_1,
    x2,
    y2,
    label_2,
    color_2,
    *,
    x_ticks,
    x_tick_label,
    _ax,
):
    fig = None

    if _ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    else:
        ax = _ax

    ax.axhline(y1.max(), color="#5EABD6", alpha=0.5, linestyle="--")
    ax.axhline(y2.max(), color="#EF5A6F", alpha=0.5, linestyle="--")

    sns.lineplot(x=x1, y=y1, label=label_1, color=color_1, marker=".", ax=ax)
    sns.lineplot(x=x2, y=y2, label=label_2, color=color_2, marker=".", ax=ax)

    if x_ticks:
        if not x_tick_label:
            raise RuntimeError("X tick labels must be passed if ticks are passed")
        ax.set_xticks(x_ticks, x_tick_label)

    ax.legend(
        loc="upper left",
    )
    sns.despine()

    plt.xlabel("")
    plt.ylabel("")
    plt.title("Variablilty in artists and tracks")

    if fig is not None:
        fig.tight_layout()

    if _ax is None:
        plt.show()
