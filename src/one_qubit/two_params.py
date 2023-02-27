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
    fig.clf()
    plt.close()
    logger.say(f"create: {f}")


def fixed_params():
    out = "output/one_qubit/2params"
    os.makedirs(out, exist_ok=True)

    for p2, p1 in itertools.product(np.linspace(0, 1, 6), repeat=2):
        name = f"{int(100*p2):03d}_{int(100*p1):03d}"
        schedule = Schedule([p1, p2])
        aqaoa = Aqaoa(schedule.spline)
        aqaoa.run(4)
        f = f"{out}/{name}.svg"
        plot(aqaoa, f, params=schedule.points)

def optimizing_params(n_params=2):
    out = f"output/one_qubit/{n_params}params_optimizing"
    os.makedirs(out, exist_ok=True)

    max_iteration = 100
    delta = 1e-10
    update_rate = 0.1
    working_params = np.linspace(0, 1, n_params + 2)[1:-1]
    for i in range(1, max_iteration + 1):
        print(f"Iteration: {i}")
        schedule = Schedule(working_params)
        aqaoa = Aqaoa(schedule.spline)
        aqaoa.run(4)
        base = aqaoa.result.expect[2][-1].real
        print(f"Params: {working_params}")
        print(f"Error: {base}")

        name = f"{i:03d}"
        f = f"{out}/{name}.svg"
        plot(aqaoa, f, params=schedule.points)

        diffs = np.zeros(len(schedule.params))

        for n, _ in enumerate(schedule.params):
            params = np.copy(schedule.params)
            params[n] += delta
            aqaoa1 = Aqaoa(Schedule(params).spline)
            aqaoa1.run(4)
            x = aqaoa1.result.expect[2][-1].real
            diffs[n] = x - base

        working_params -= diffs * update_rate / delta 


optimizing_params(3)
