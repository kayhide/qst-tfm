from qutip import *
import matplotlib.pyplot as plt
import numpy as np

import prelude

logger = prelude.logger

ustate = basis(3, 0)
excited = basis(3, 1)
ground = basis(3, 2)

N = 2 # Set where to truncate Fock state for cavity
sigma_ge = tensor(qeye(N), ground * excited.dag())  # |g><e|
sigma_ue = tensor(qeye(N), ustate * excited.dag())  # |u><e|
a = tensor(destroy(N), qeye(3))
ada = tensor(num(N), qeye(3))

c_ops = []  # Build collapse operators
kappa = 1.5 # Cavity decay rate
c_ops.append(np.sqrt(kappa) * a)
gamma = 6  # Atomic decay rate
c_ops.append(np.sqrt(5*gamma/9) * sigma_ue) # Use Rb branching ratio of 5/9 e->u
c_ops.append(np.sqrt(4*gamma/9) * sigma_ge) # 4/9 e->g

t = np.linspace(-15, 15, 100) # Define time vector
psi0 = tensor(basis(N, 0), ustate) # Define initial state

state_GG = tensor(basis(N, 1), ground) # Define states onto which to project
sigma_GG = state_GG * state_GG.dag()
state_UU = tensor(basis(N, 0), ustate)
sigma_UU = state_UU * state_UU.dag()

g = 5  # coupling strength
H0 = -g * (sigma_ge.dag() * a + a.dag() * sigma_ge)  # time-independent term
H1 = (sigma_ue.dag() + sigma_ue)  # time-dependent term

def H1_coeff(t, args):
    return 9 * np.exp(-(t / 5.) ** 2)
    

H = [H0,[H1, H1_coeff]]
result = mesolve(H, psi0, t, c_ops, [ada, sigma_UU, sigma_GG])

print(f"H0\n{H0}")
print(f"H1\n{H1}")
print(ustate, excited, ground)
print(result)

def plot(f):
    fig, ax = plt.subplots()

    ax.set_title("Probability")
    ax.plot(result.expect[1])

    plt.savefig(f)
    logger.say(f"create: {f}")


f = "output/qutip_sandbox.png"
plot(f)
