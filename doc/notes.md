### 

- Done:
  - Investigate numerical integration

- Questions:
  - I looked into numerical integrations.  
    They are for a single integration at a time and does not seem to solve exponential form of integral as we have.
    Am I missing something?
  - As for the methods suggested by Koshik, they are already available at [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

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
