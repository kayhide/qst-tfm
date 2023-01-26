from scipy.interpolate import CubicHermiteSpline
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy as sp

verbose = False
quiet = False
if not verbose:
    info = lambda msg: None
else:
    info = lambda msg: print(msg)

if quiet:
    say = lambda msg: None
else:
    say = lambda msg: print(msg)

n_params = 1
params = [0.0, *[random.uniform(-2.0, 2.0) for _ in range(0, n_params)], 1.0]
spline = CubicHermiteSpline(
    np.linspace(0, 1, len(params)),
    params,
    np.repeat(0.0, len(params)),
    extrapolate=False,
)


def plot(f):
    fig, ax = plt.subplots()
    n = len(params)
    xs = np.linspace(0, 1, n)
    ax.plot(xs, params, 'o')
    
    n = 1000
    xs = np.linspace(0, 1, n)
    ys = [spline(x) for x in xs]
    ax.plot(xs, ys)
    plt.savefig(f)
    say(f"create: {f}")


f = "output/main.png"
plot(f)
