import itertools
import matplotlib.pyplot as plt
import numpy as np
import os

import prelude
from one_qubit.aqaoa import Aqaoa
from schedule import Schedule

logger = prelude.logger


def plot(aqaoa, f, params=None):
    ts = aqaoa.ts
    result = aqaoa.result

    fig, axs = plt.subplots(2, 2, sharex=False)

    ax = axs[0, 0]
    ax.set_title("Error")
    ax.set_ylim(-0.05, 1.05)
    # ax.set_ymargin(0.1)
    ax.plot(ts, result.expect[2])

    ax = axs[0, 1]
    ax.set_title("Fidelity")
    ax.plot(ts, result.expect[3])

    ax = axs[1, 0]
    ax.set_title("Cost")
    ax.plot(ts, result.expect[1])

    ax = axs[1, 1]
    if params:
        n = len(params)
        xs = np.linspace(0, 1, n)
        ax.plot(xs, params, "o")

    xs = np.linspace(0, 1, len(ts))
    ys = [aqaoa.schedule(x) for x in xs]
    ax.plot(xs, ys)
    ax.set_title("Schedule function")

    plt.subplots_adjust(hspace=0.30)
    plt.savefig(f)
    logger.say(f"create: {f}")


out = "output/one_qubit/2params"
os.makedirs(out, exist_ok=True)

for p2, p1 in itertools.product(np.linspace(0, 1, 6), repeat=2):
    name = f"{int(100*p2):03d}_{int(100*p1):03d}"
    schedule = Schedule([p1, p2])
    aqaoa = Aqaoa(schedule.spline)
    aqaoa.run(4)
    f = f"{out}/{name}.svg"
    plot(aqaoa, f, params=schedule.params)
