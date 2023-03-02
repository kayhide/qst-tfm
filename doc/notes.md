### 03/01

- Next
  - Do the same for two-qubit states
- Done
  - By gradient descent, optimize schedule functions with
    - 2-param [#](https://github.com/kayhide/qst-tfm/tree/main/output/one_qubit/2params_optimizing)
    - 3-param [#](https://github.com/kayhide/qst-tfm/tree/main/output/one_qubit/3params_optimizing)

### 02/24

- Next
  - Optimize schedule function for one-qubit case
  - By whatever method (gradient descent, genetic approach or...)
- Done
  - For various 2-param piece-wise cubic splines, run simulations and plot variables [#](https://github.com/kayhide/qst-tfm/tree/main/src/one_qubit#2-param-piece-wise-cubic-interpolations)

### 02/20

- Next
  - Optimize schedule function for one-qubit case
    - Use $\epsilon_R$ at $T = 4$ as a cost function
    - Optimze by gradient descent method
  - Try two-qubit case as I did at one-qubit example
    - With $\lambda(t) = t$ or $\lambda(t) = \sin^2(...)$...
- Discussion
  - More than two qubit (N = 5, for example)

$$
H_f = \sum_{i \neq j = 1}^N \sigma_z^i \sigma_z^j
$$

- Done
  - Simultate time evolution for single qubit [#](https://github.com/kayhide/qst-tfm/tree/main/src/one_qubit#simulated-time-evolution)
- Question
  - With a linear schedule function, it does not seem reproducing the result by the paper...
  - The linear and something wild schedule function ended up with the lowest error. Is it expected?

### 02/17

- Next
  - Use qutip and compute U(t)
  - Reproduce the result of the case of single pauli operator on the paper

Koushik told that $\sigma_z \sigma_z^2$ has a lot of applications.
Here are some of them:

- Applications
  - travelling salesman
  - portfolio optimization
  - maxent
  - SK model
  - P-Spin model
  - TFIM
  - LFIM

- Done
  - Install qutip
  - See an example of time-dependent hamiltonian work [#](https://github.com/kayhide/qst-tfm/tree/main/src/qutip_sandbox)

### 02/12

We discussed with Prof. Xi, and Pranan.

- Discussion
  - Xi suggested that energy variance can be a good cost function.
  - He also told that there is a case of digitization with non-constant time step

Energy variance

$$
(\Delta E)^2 = \langle E^2 \rangle - \langle E \rangle ^2
$$

- Next
  - Anyway, find a way to compute U(t)
  - Try QuTip
    [Solving Problems with Time-dependent Hamiltonians](https://qutip.org/docs/latest/guide/dynamics/dynamics-time.html)

- Done
  - Investigate Torotterization [#](https://github.com/kayhide/qst-tfm/tree/main/doc/trotterization.md)

### 02/10

- Next
  - Think about how to implement the continuous version of U(t)
    - Take 1 week
  - Explain what Trotterization is
    - What is Trotterization?
    - What are Trotterization errors?
    - 1st and 2nd ordeer

- Done
  - See Trotterization

$$
e^{-i (H_1 + H_2) t} = \lim_{N -> \infty} \left( e^{H_1 t \over N} e^{H_2 t \over N} \right) ^ N
$$

### 02/08

- Next:
  - Study trotterization
  - Think about how to compute exponential integrals seen in time evolution

- Done:
  - Draw schedule function by piece-wise cubic interpolation [#](https://github.com/kayhide/qst-tfm/tree/main/src/cubic_hermite_spline)
 
### 02/03

- Next
  - Draw schedule function, see how it goes for various set of parameters
  - Randomely generate the parameters

- Done:
  - Expand the exponential operator

$$
\begin{align*}
e^{i \theta \sigma_x} & = \sum_{n=0}^\infty {(i \theta \sigma_x)^n \over n!}\\
               & = \mathit{I} + i \theta \sigma_x - {1 \over 2!} (\theta \sigma_x)^2 - i {1 \over 3!} (\theta \sigma_x)^3 + ...\\
               & = \mathit{I} + i \theta \sigma_x - {\theta^2 \over 2!} \mathit{I} - i {\theta^3 \sigma_x \over 3!} + ...\\
               & = \mathit{I} \left( 1 - {\theta^2 \over 2!} + {\theta^4 \over 4!} - ... \right) + i \sigma_x \left( \theta - {\theta^3 \over 3!} + {\theta^5 \over 5!} - ... \right) \\
               & = \left( \matrix{ \cos \theta & i \sin \theta \cr i \sin \theta & \cos \theta} \right)
\end{align*}
$$


### 02/01

- Next:
  - Think how to make the following exponential operator into 2x2 matrix (in 24 hours)

$$ e^{i \sigma_x}  = {\left\lbrack \matrix{? & ? \cr ? & ?} \right\rbrack}
, \text{where } \sigma_x = {\left\lbrack \matrix{0 & 1 \cr 1 & 0} \right\rbrack}
$$

- Done:
  - Investigate numerical integration

- Questions:
  - I looked into numerical integrations.  
    They are for a single integration at a time and does not seem to solve exponential form of integral as we have.
    Am I missing something?
  - As for the methods suggested by Koushik, they are already available at [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

- Ref:
  - [Trapezoidal rule](https://en.wikipedia.org/wiki/Trapezoidal_rule)
  - [Simpson's rule](https://en.m.wikipedia.org/wiki/Simpson's_rule)
  - Maybe useful? [Solving Problems with Time-dependent Hamiltonians](https://qutip.org/docs/latest/guide/dynamics/dynamics-time.html)

### 01/30

- Next:
  - Numerical integration
    - Trapezoidal
    - Simpson's 1/3

- Done:
  - Randomely generate U
  - Test cost function

- Questions:
  - How can we derive U? It has the form of: 

$$ U(t) = e^{-i \int_0^\tau H(t) d\tau} $$

  - If we try to deal with it squarely, we face multiple integrals nested infinitely.  
    The following discussion describes it:  
    [Evolution operator for time-dependent Hamiltonian](https://physics.stackexchange.com/questions/45455/evolution-operator-for-time-dependent-hamiltonian)
 
### 01/27

- Next:
  - Try One qubit case

- Done:
  - Understand the piece-wise cubic interpolation

### 01/25

1st meeting

[Analog Quantum Approximate Optimization Algorithm](https://arxiv.org/abs/2112.07461)

- Todo:
  - Read the paper and understand the piece-wise cubic interpolation
