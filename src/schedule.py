from scipy.interpolate import CubicHermiteSpline
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy as sp


class Schedule:
    def __init__(self, params):
        self.n = len(params)
        self.params = [0.0, *params, 1.0]
        self.spline = CubicHermiteSpline(
            np.linspace(0, 1, len(self.params)),
            self.params,
            np.repeat(0.0, len(self.params)),
            extrapolate=False,
        )
