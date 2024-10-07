from matplotlib import pyplot as plt
from data_handler import get_atom_dict


def long_periodic_table():
    elements_data = get_atom_dict('long')
    fig, ax = plt.subplots(figsize=(22, 13))
    for symbol, (x, y) in elements_data.items():
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=None, edgecolor='black', lw=1))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=12, weight='bold',
                zorder=2, alpha=0.7)

    ax.set_aspect('equal')
    x_margin = 3
    y_margin = 2
    ax.set_xlim(0.5 - x_margin, 32.5 + x_margin)
    ax.set_ylim(0.5 - y_margin, 7.5 + y_margin)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    return ax


def short_periodic_table():
    elements_data = get_atom_dict('short')
    fig, ax = plt.subplots(figsize=(22, 13))
    for symbol, (x, y) in elements_data.items():
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=None, edgecolor='black', lw=1))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=18, weight='bold',
                zorder=2, alpha=0.7)

    ax.set_aspect('equal')
    x_margin = 3
    y_margin = 2
    ax.set_xlim(0.5 - x_margin, 18.5 + x_margin)
    ax.set_ylim(0.5 - y_margin, 10 + y_margin)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    return ax


def periodic_table_visual(table_type):
    if table_type == 'long':
        return long_periodic_table()
    elif table_type == 'short':
        return short_periodic_table()
