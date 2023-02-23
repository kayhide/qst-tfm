from qutip import *
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import random

from scipy.linalg import qr
from scipy.integrate import quad

import prelude

logger = prelude.logger


class Aqaoa:
    def __init__(self, schedule, omega=1.0):
        self.schedule = schedule
        self.omega = omega
        self.H0 = sigmax()
        self.H1 = sigmaz()
        self.psi0 = self.H0.groundstate()[1]  # Initial state
        self.psi1 = self.H1.groundstate()[1]  # Final state

    def error(self, t, state):
        return np.abs((expect(self.H1, state) - self.exp1) / self.exp1)

    def fidelity(self, t, state):
        return (self.psi1.dag() * state).norm() ** 2

    def run(self, t_final):
        c_ops = []
        e_ops = [self.H0, self.H1, self.error, self.fidelity]

        self.exp1 = expect(self.H1, self.psi1)
        self.ts = np.linspace(0, t_final, 1001)

        a = self.omega / 2.0
        self.H = [
            [a * self.H0, lambda t, args: 1 - self.schedule(t / t_final)],
            [a * self.H1, lambda t, args: self.schedule(t / t_final)],
        ]

        self.result = mesolve(self.H, self.psi0, self.ts, c_ops, e_ops)
