import itertools
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.optimize as opt

import prelude
from ising.aqaoa import Aqaoa
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

class Runner:
    def __init__(self, n_params):
        self.n_params = n_params
        self.iter = 0
        self.out = f"output/ising/{n_params}params_optimizing"
        os.makedirs(self.out, exist_ok=True)

    def fun(self, ps):
        schedule = Schedule(ps)
        aqaoa = Aqaoa(schedule.spline)
        return aqaoa.evaluate(4)

    def cb(self, ps):
        self.iter += 1
        i = self.iter
        print(f"Iteration: {i}")
        schedule = Schedule(ps)
        aqaoa = Aqaoa(schedule.spline)
        aqaoa.run(4)
        err = aqaoa.result.expect[2][-1].real
        print(f"Params: {ps}")
        print(f"Error: {err}")

        f = f"{self.out}/{i:03d}.svg"
        plot(aqaoa, f, params=schedule.points)
        return True

    def execute(self):
        init = np.linspace(0, 1, self.n_params + 2)[1:-1]
        res = opt.minimize(self.fun, init, callback=self.cb, method="BFGS", options={'disp': True})
        print(res)

Runner(2).execute()
