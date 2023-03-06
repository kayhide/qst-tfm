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


class Aqaoa:
    def __init__(self, schedule, sites=2, omega=1.0):
        self.schedule = schedule
        self.sites = sites
        self.omega = omega

        I, X, Y, Z = qeye(2), sigmax(), sigmay(), sigmaz()
        N = self.sites
        singles = sum(tensor(replace_at(i, Z, [I] * N)) for i in range(0, N))
        doubles = sum(
            tensor(replace_at(i, Z, [I] * N)) * tensor(replace_at(i + 1, Z, [I] * N))
            for i in range(0, N - 1)
        )
        self.H0 = self.omega / 2.0 * tensor([sigmax()] * N)
        self.H1 = self.omega / 2.0 * singles - 2 * self.omega * doubles

        # Initial state
        vs, kets = self.H0.eigenstates()
        self.psi0 = kets[list(vs).index(min(vs))]

        # Final state
        vs, kets = self.H1.eigenstates()
        self.psi1 = kets[list(vs).index(min(vs))]

    def error(self, t, state):
        return np.abs((expect(self.H1, state) - self.exp1) / self.exp1)

    def fidelity(self, t, state):
        return (self.psi1.dag() * state).norm() ** 2

    def run(self, t_final):
        c_ops = []
        e_ops = [self.H0, self.H1, self.error, self.fidelity]

        self.exp1 = expect(self.H1, self.psi1)
        self.ts = np.linspace(0, t_final, 1001)

        self.H = [
            [self.H0, lambda t, args: 1 - self.schedule(t / t_final)],
            [self.H1, lambda t, args: self.schedule(t / t_final)],
        ]

        self.result = mesolve(self.H, self.psi0, self.ts, c_ops, e_ops)

    def evaluate(self, t_final):
        c_ops = []
        e_ops = [self.error]

        self.exp1 = expect(self.H1, self.psi1)
        self.ts = np.linspace(0, t_final, 1001)

        self.H = [
            [self.H0, lambda t, args: 1 - self.schedule(t / t_final)],
            [self.H1, lambda t, args: self.schedule(t / t_final)],
        ]
        self.result = mesolve(self.H, self.psi0, self.ts, c_ops, e_ops)
        return self.result.expect[0][-1].real
