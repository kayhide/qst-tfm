# Trotterization

## Trotter formula

$$
e^{A + B} = \lim_{n -> \infty} \left( e^{A \over n} e^{B \over n} \right) ^ n
$$

### Proof

$$
\begin{align*}
e^{A \over n} & = I + {1 \over n}A + \mathcal{O}({1 \over n^2}) \\
e^{B \over n} & = I + {1 \over n}B + \mathcal{O}({1 \over n^2})
\end{align*}
$$

$$
e^{A \over n} e^{B \over n} = I + {1 \over n}(A + B) + \mathcal{O}({1 \over n^2})
$$

$$
\begin{align*}
\left( e^{A \over n} e^{B \over n} \right)^n &= \left(I + {1 \over n}(A + B) + \mathcal{O}({1 \over n^2}) \right)^n \\
   &= I + \sum_{k=1}^n \left( \matrix{n \cr k} \right) {1 \over n^k} (A + B)^k + \mathcal{O}({1 \over n^2}) \\
   &= I + \sum_{k=1}^n {1 \over k!} (A + B)^k \left( 1 + \mathcal{O}({1 \over n}) \right) + \mathcal{O}({1 \over n^2}) \\
   &= I + \sum_{k=1}^n {1 \over k!} (A + B)^k + \mathcal{O}({1 \over n})
\end{align*}
$$

Therefore

$$
\begin{align*}
\lim_{n -> \infty} \left( e^{A \over n} e^{B \over n} \right)^n &= \lim_{n -> \infty} \sum_{k}^n {1 \over k!} (A + B)^k + \mathcal{O}({1 \over n}) \\
   &= \lim_{n -> \infty} \sum_{k}^n {1 \over k!} (A + B)^k \\
   &= e^{A + B}
\end{align*}
$$

Note that

$$
\left( \matrix{n \cr k} \right) = {n (n - 1) (n - 2) \... (n - k + 1) \over k!} = {n^{\underline{k}} \over k!} 
$$

is [Binomial coeeficient](https://en.wikipedia.org/wiki/Binomial_coefficient) and

$$
\left( \matrix{n \cr k} \right) {1 \over n^k} = \left(1 + \mathcal{O}({1 \over n}) \right) {1 \over k!}
$$

### 1st order trotterization

$$
e^{(A + B) \delta} = e^{A \delta} e^{B \delta} + \mathcal{O}(\delta^2)
$$

### 2st order trotterization

$$
e^{(A + B) \delta} = e^{A \delta / 2} e^{B \delta} e^{A \delta / 2} + \mathcal{O}(\delta^3)
$$

### Error

In the case of a Trotter approximation of $p$ th order, the error is of order $\delta^{p+1}$.

When taking steps of $n = {T \over \delta}$, then the error is:

$$
\epsilon = {T \over \delta} \delta^{p + 1} = T \delta^p
$$

## References

- M.A.Nielsen, I.L.Chuang, _Quantum Computaion and Quantum Information_ (p.207)
- Wikipedia, [Time-evolving block decimation](https://en.wikipedia.org/wiki/Time-evolving_block_decimation)
