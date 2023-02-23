import matplotlib.pyplot as plt
import numpy as np

import prelude
from one_qubit.aqaoa import Aqaoa

logger = prelude.logger


def plot(aqaoa, f):
    ts = aqaoa.ts
    result = aqaoa.result

    fig, axs = plt.subplots(2, 2, sharex=False)

    ax = axs[0, 0]
    ax.set_title("Error")
    ax.plot(ts, result.expect[2])

    ax = axs[0, 1]
    ax.set_title("Fidelity")
    ax.plot(ts, result.expect[3])

    ax = axs[1, 0]
    ax.set_title("Cost")
    ax.plot(ts, result.expect[1])

    ax = axs[1, 1]
    # # n = len(params)
    # # xs = np.linspace(0, 1, n)
    # # ax.plot(xs, params, "o")

    xs = np.linspace(0, 1, len(ts))
    ys = [schedule(x) for x in xs]
    ax.plot(xs, ys)
    ax.set_title("Schedule function")

    plt.subplots_adjust(hspace=0.30)
    plt.savefig(f)
    logger.say(f"create: {f}")


exs = [
    ["line", lambda t: t],
    ["sin", lambda t: np.sin(np.pi / 2 * t)],
    ["sin2", lambda t: np.sin(np.pi / 2 * t) ** 2],
    ["something", lambda t: t + np.sin(np.pi * t) ** 2 * np.cos(np.pi * 20 * t)],
]

omega = 1.0

for ex in exs:
    name, schedule = ex
    aqaoa = Aqaoa(schedule, omega=omega)
    aqaoa.run(4.0 / omega)
    f = f"output/one_qubit_{name}.png"
    plot(aqaoa, f)
