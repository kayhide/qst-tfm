from qutip import *
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import random

from scipy.linalg import qr
from scipy.integrate import quad

import prelude

logger = prelude.logger

omega = 1.0
T = 4.0 / omega


class Aqaoa:
    def __init__(self, schedule):
        self.schedule = schedule
        self.H0 = sigmax()
        self.H1 = sigmaz()
        self.H = [
            [omega / 2.0 * self.H0, lambda t, args: 1 - schedule(t / T)],
            [omega / 2.0 * self.H1, lambda t, args: schedule(t / T)],
        ]

        self.psi0 = self.H0.groundstate()[1]  # Initial state
        self.psi1 = self.H1.groundstate()[1]  # Final state

        self.exp1 = expect(self.H1, self.psi1)
        self.ts = np.linspace(0, T, 1000)

    def error(self, t, state):
        return np.abs((expect(self.H1, state) - self.exp1) / self.exp1)

    def fidelity(self, t, state):
        return (self.psi1.dag() * state).norm() ** 2

    def run(self):
        c_ops = []
        e_ops = [self.H0, self.H1, self.error, self.fidelity]

        self.result = mesolve(self.H, self.psi0, self.ts, c_ops, e_ops)


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
    ys = [schedule(t / T) for t in ts]
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

for ex in exs:
    name, schedule = ex
    aqaoa = Aqaoa(schedule)
    aqaoa.run()
    f = f"output/one_qubit_{name}.png"
    plot(aqaoa, f)
