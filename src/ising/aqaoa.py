from qutip import *
from functools import reduce
from itertools import chain, repeat
import matplotlib.pyplot as plt
import numpy as np
import random

from scipy.linalg import qr
from scipy.integrate import quad

import prelude

logger = prelude.logger


def replace_at(i, x, xs):
    xs[i] = x
    return xs

def ising_chain(n, h, j):
    I, X, Y, Z = qeye(2), sigmax(), sigmay(), sigmaz()
    N = n
    singles = sum(tensor(replace_at(i, Z, [I] * N)) for i in range(0, N))
    doubles = sum(
        tensor(replace_at(i, Z, [I] * N)) * tensor(replace_at(i + 1, Z, [I] * N))
        for i in range(0, N - 1)
    )
    return - h * singles - j * doubles


class Aqaoa:
    def __init__(self, schedule, sites=2, omega=1.0):
        self.schedule = schedule
        self.sites = sites
        self.omega = omega

        self.H0 = self.omega / 2.0 * tensor([sigmax()] * self.sites)
        self.H1 = ising_chain(self.sites, - self.omega / 2.0, 2.0 * self.omega)

        # Initial state
        vs, kets = self.H0.eigenstates()
        self.psi0 = kets[list(vs).index(min(vs))]

        # Final state
        vs, kets = self.H1.eigenstates()
        self.psi1 = kets[list(vs).index(min(vs))]

        # Expectation of the final state
        self.exp1 = expect(self.H1, self.psi1)

    def error(self, t, state):
        return np.abs((expect(self.H1, state) - self.exp1) / self.exp1)

    def fidelity(self, t, state):
        return (self.psi1.dag() * state).norm() ** 2

    def energy_variance(self, t, state):
        H = sum(x[0] * x[1](t, {}) for x in self.H)
        return expect(H * H, state) - expect(H, state) ** 2

    def str_to_op(self, s):
        match s:
            case "error":
                return self.error
            case "energy_variance":
                return self.energy_variance
            case _ :
                raise Exception(f"Unknown expectation function: {op}")

    def run(self, t_final, e_ops=[]):
        c_ops = []
        e_ops = [self.str_to_op(op) for op in e_ops]
        if e_ops == []:
            e_ops = [self.H0, self.H1, self.error, self.fidelity, self.energy_variance]

        self.ts = np.linspace(0, t_final, 1001)
        self.H = [
            [self.H0, lambda t, args: 1 - self.schedule(t / t_final).item()],
            [self.H1, lambda t, args: self.schedule(t / t_final).item()],
        ]

        self.result = mesolve(self.H, self.psi0, self.ts, c_ops, e_ops)

    def evaluate(self, t_final, op="error"):
        self.run(t_final, e_ops=[op])
        return self.result.expect[0][-1].real
