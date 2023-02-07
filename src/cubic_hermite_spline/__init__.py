from scipy.interpolate import CubicHermiteSpline
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy as sp

import prelude

logger = prelude.logger

class Schedule:
  def __init__(self, n):
    self.n = n
    self.params = [0.0, *[random.uniform(-1.0, 2.0) for _ in range(0, n)], 1.0]
    self.spline = CubicHermiteSpline(
            np.linspace(0, 1, len(self.params)),
            self.params,
            np.repeat(0.0, len(self.params)),
            extrapolate=False,
        )


def plot(f, schedules):
    fig, ax = plt.subplots()
    
    for schedule in schedules:
        color = next(ax._get_lines.prop_cycler)['color']
        ax.set_title(f"Schedule function (N={schedule.n})")
        
        xs = np.linspace(0, 1, schedule.n + 2)
        ax.plot(xs, schedule.params, "o", color=color)

        n = 1000
        xs = np.linspace(0, 1, n)
        ys = [schedule.spline(x) for x in xs]
        ax.plot(xs, ys, color=color)
        
        ax.set_ylim([-1.2, 2.2])
    plt.savefig(f)
    logger.say(f"create: {f}")


for n in [1, 2, 4, 8]:
    f = f"output/cubic_hermite_spline-{n}.png"
    plot(f, [Schedule(n) for _ in range(3)])
