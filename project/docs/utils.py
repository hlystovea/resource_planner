import io
from typing import IO

import pandas as pd
from matplotlib import pyplot as plt


PLOT_PARAMS = ('Ug', 'If', 'Uf')


def plot_from_csv(file: IO) -> io.BytesIO:
    df = pd.read_csv(file, sep=';', decimal=',', header=1, index_col='time')
    _, ax = plt.subplots(figsize=(8, 4))

    for line in PLOT_PARAMS:
        ax.plot(df[line], label=line, lw=1)

    ax.legend()
    ax.set_ylabel('o.e.')
    ax.set_xlabel('t, c')
    ax.grid(which='major')
    ax.minorticks_on()
    ax.axhline(lw=0.6, color='#000000')

    pic = io.BytesIO()
    plt.savefig(pic, format='png', dpi=100)
    plt.close()
    pic.seek(0)

    return pic
