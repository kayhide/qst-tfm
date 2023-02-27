from scipy.interpolate import CubicHermiteSpline
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy as sp


class Schedule:
    def __init__(self, params):
        self.n = len(params)
        self.params = params
        self.points = [0.0, *params, 1.0]
        self.spline = CubicHermiteSpline(
            np.linspace(0, 1, len(self.points)),
            self.points,
            np.repeat(0.0, len(self.points)),
            extrapolate=False,
        )
