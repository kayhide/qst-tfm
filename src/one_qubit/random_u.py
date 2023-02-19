from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import random

from scipy.linalg import qr
from scipy.integrate import quad

import prelude

logger = prelude.logger


def generate_hamiltonian(h0, h1, sc):
    return lambda t: sc(1.0 - t) * h0 + sc(t) * h1


def generate_random_u(h):
    return lambda t: (lambda h11, h12: np.matrix(qr([[h11, h12], [h12, -h11]])[0]))(
        random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
    )


schedule = lambda t: np.sin(np.pi / 2.0 * t)

h_initial = np.matrix(
    [
        [0.0, 1.0],
        [1.0, 0.0],
    ]
)

h_final = np.matrix(
    [
        [1.0, 0.0],
        [0.0, -1.0],
    ]
)

s0 = np.matrix([1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)]).reshape(2, 1)
s1 = np.matrix([0.0, 1.0]).reshape(2, 1)

h = generate_hamiltonian(h_initial, h_final, schedule)

u = generate_random_u(h)

cost = lambda v: (s0.H @ v.H @ h_final @ v @ s0)[0, 0]
error = lambda v: np.abs(
    ((s0.H @ v.H @ h_final @ v @ s0)[0, 0] - (s1.H @ h_final @ s1)[0, 0])
    / (s1.H @ h_final @ s1)[0, 0]
)

us = [u(0.0) for _ in range(1000)]
attempts = [(cost(u0), u0) for u0 in us]
attempts.sort(key=lambda x: -x[0])

np.set_printoptions(precision=5, suppress=True)
logger.say(f"s0: {s0.reshape(2)}")
logger.say(f"H0 * s0: {(h_initial @ s0).reshape(2)}")

u1 = attempts[-1]
logger.say(f"U1 * s0: {(u1[1] @ s0).reshape(2)}")
logger.say(f"H1 * U1 * s0: {(h_final @ (u1[1] @ s0)).reshape(2)}")
logger.say(f"cost: {u1[0]}")


def plot(f):
    n = 1000
    # fig, axs = plt.subplots(1, 2, sharex=False)
    fig, ax = plt.subplots()

    # ax = axs[0]
    ax.set_title("Cost")
    xs = range(0, len(attempts))
    ys = [x[0] for x in attempts]
    ax.plot(xs, ys)

    # ax = axs[1]
    # ax.set_title("Schedule function")
    # # n = len(params)
    # # xs = np.linspace(0, 1, n)
    # # ax.plot(xs, params, "o")

    # xs = np.linspace(0, 1, n)
    # ys = [schedule(x) for x in xs]
    # ax.plot(xs, ys)

    plt.savefig(f)
    logger.say(f"create: {f}")


f = "output/one_qubit.png"
plot(f)
