# Probability and information theory basics

- **events**: $\Omega$ set
- **random variable**: $\Omega\to V$ function, where $V$ is a vector space
- **estimation of time series**
    - all events show up in time series $\Rightarrow \omega_n,\;n=1,\dots,N_{data}$
    - we can not/want not predict the exact series, want only statistical information
    - discrete case: probability is the rate $\omega\in\Omega$ element occurs in the data $$P(\omega)=\frac1{N_{data}}\sum_{n=1}^{N_{data}} \mathbb I(\omega_n=\omega),$$ where $\mathbb I$ is the indicator function 
    - continuous case: probability is the rate elments from $\omega\in d\Omega(\omega)\subset \Omega$ occur in the data, where $d\Omega(\omega)$ is a small volume around $\omega$ $$P(\omega)=\frac1{N_{data}}\sum_{n=1}^{N_{data}} \mathbb I(\omega_n\in d\Omega(\omega)) = p(\omega)|d\Omega|,$$ 
    where $p(\omega)$ is called the probability density if $|d\Omega|\to0$.
    - technically we take the histogram
    - expected value of a random variable $f$: $$\mathbb E_\omega(f(\omega)) = \frac1{N_{data}}\sum_{n=1}^{N_{data}} f(\omega_n) = \sum_{\omega\in\Omega} P(\omega)f(\omega)$$
        - proof: $\sum_n f(\omega_n) = \sum_{n,\omega} f(\omega_n) \mathbb I(\omega=\omega_n) = \sum_\omega f(\omega)\sum_n \mathbb I(\omega=\omega_n)$
        - time average is replaced by ensemble average

- **probability of a random variable**
    - $\xi$ random variable, the probability over the event space $\xi(\Omega)$ is the probability of a random variable
    $$P_\xi(\xi_0) = \frac1{N_{data}}\sum_{n=1}^{N_{data}} \mathbb I(\xi(\omega_n)=\xi_0) = \mathbb E_\omega(\mathbb I(\xi(\omega)=\xi_0))$$
    - expected values: $\mathbb E_\xi(f(\xi)) = \mathbb E_\omega(f\circ \xi(\omega))$

- **marginal probability**
    - probability of a single component $$P(\xi) = \sum_\eta P(\xi,\eta)$$
    - proof: $P(\xi) = \frac1N\sum_n \mathbb I(\xi) = \frac1N\sum_n \sum_\eta \mathbb I(\xi,\eta)$

- **independence**
    - a two components of a random variable are independent if $P(\xi_1,\xi_2) = P(\xi_1)P(\xi_2)$
    - expected values factorize $\mathbb E(f(\xi_1)g(\xi_2))=\mathbb E(f(\xi_1))\mathbb E(g(\xi_2))$

- **Stirling formula**
    - approximation of the factorial $$\ln n! = n\ln n - n + \frac12 \ln(2\pi n) + \mathcal o(1)$$

- **information theory**
    - assume lot of measurements both total and in each bin
    - use Stirling formula leading order
    - concepts:
        - entropy (impurity)
        - mutual information
    - bit of information: one Y/N question, binary representation
    - information content: Shannon entropy

- **Shannon entropy**
    - $e^{N_{all}H}$ counts how many microstates can make up a macrostate
    - microstates: uniform probability ensemble of a large set of $N_{all}$ elements
    - macrostates: bins with $N_n$ elments in it, $\sum_{n=1}^N N_n=N_{all}$, element order does not count
    - number of states realizing the macrostate: $$ e^{N_{all}H} = \binom {N_{all}}{N_1}\binom{N_{all}-N_1}{N_2}\dots \binom{N_{all}-\sum_{i=1}^{k-1}N_i}{N_k}\dots = \dfrac{N_{all}!}{\prod_k N_k!}.$$
    - in information theory we apply Stirling formula
    $$ H(p) = -\sum_k p_n \ln p_n,\quad p=(p_1,\dots,p_N),\;p_n=\frac{N_n}{N_{all}}$$
    - properties:
        - $H\ge 0$
        - minimal for pure sample $p_n=1,\, p_{m\neq n}=0$
        - maximal for uniform distribution $p_i=\dfrac1{N}$, there $H=\ln N$
        - concave, i.e. mixing increases entropy: $$H(\lambda p + (1-\lambda)q) \ge  \lambda H(p) + (1-\lambda)H(q)$$
    - provides the minimal average length of the prefix-free codes (c.f. twenty questions, barchoba)

- **prefix-free coding**
    - assign a unique binary code for each of the elements in a set, where a code can not be the starting code of another one
    - let the code length associated to the $i$th element $\ell_i$
    - at depth $d$ at most $2^d$ code can be distributed
    - the descendants of a code of length $\ell$ with depth $N>\ell$ is $2^{N-\ell}$ (this is the number of free bits)
    - the descendants of different length are different (prefix-free)
    - the sum of descendants of $\ell_1$, $\ell_2$, \dots to depth $N$ is at most $2^N$, i.e. $\sum_i 2^{N-\ell_i} \le 2^N$.
    - follows the Kraft’s inequality

- **Kraft's inequality**:
    - in prefix-free coding with code length $\ell_i$ we have  $$\sum_i 2^{-\ell_i}\le 1.$$

- **average length of the prefix-free codes**
    - assign a prefix-free code for elements of a set, the code length are $\ell_i$
    - the probability of each element is $p_i$
    - average code length: $$\sum_i p_i\ell_i \le -\sum_i p_i\log_2 p_i$$
    - proof: 
        - the code length set satisfies Kraft's inequality
        - in the smallest case it is an equality
        - insert Kraft's formula with $\lambda$ Langrange multiplicator, and find the minimum of
        $\sum_i p_i\ell_i + \lambda \sum_i 2^{-\ell_i}$
        - results in $\ell_i = \ln(\lambda \ln 2) - \log_2 p_i$
        - from $\sum_i p_i=1$ and Kraft's equation follows $\lambda\ln2=1$, so the prefactor is zero

- **Huffmann coding**
    - construction to achieve minimal code length
    - have $m$ elements with $p_i$ probabilities
    - merge the two smallest probability event to a single one, with probability $p_1+p_2$
    - we obtained an $m-1$ long system
    - repeat the above procedure until no elements remain
    - the prefix codes are the choices in the tree

    <img src="../Images/Huffmann_coding.png" alt="Alt text" width="200">

- **Boltzmann distribution**
    - minimize Shannon entropy with a constraint $E=\sum_iE_ip_i$
    - results in the Boltzmann distribution:$$p_i \sim e^{-\beta E_i}$$
    - proof:
        - Langrange multiplicator $\beta$ implies: $\min(\sum_i p_i(\beta E_i-\log p_i)$)
        - results in $p_i\sim e^{-\beta E_i}$

- **other entropy formulea**
    - important: positive, convex
    - Rényi-Tsallis entropy
        $$ H_\alpha = \frac1{1-\alpha}\log(\sum_i p_i^\alpha)$$
    - Gini impurity:
        $$ G = 1-\sum_ip_i^2$$
    - picture:

    <img src="../Images/alternative-entropies.png" alt="Alt text" width="200">

- **mutual information**
    - two random variables $x\in X$ and $y\in Y$
    - Shannon entropy $H(X,Y)=-\sum_{x\in X, y\in Y} p(x,y)\log p(x,y)$
    - for independent variables $p(x,y)=p(x)p(y)$, and so $H(X,Y) = H(X) + H(Y)$ where $H(X)=-\sum_{x\in X} p(x)\log p(x)$
    - non-independence measure: mutual information
    $$ I(X,Y)= H(X,Y)-H(X)-H(Y) = -\sum_{x,y} p(x,y) \ln\frac{p(x,y)}{p(x)p(y)}

- **probability of the observed sample**
    - the probabilities of bins is $q_i$
    - we draw $N$ elements
    - what is the probability that we observe $N_i$ in the bins?
        - the first $N_1$ element goes to bin 1, then $N_2$ goes to bin 2, etc.: $P = \prod_i q_i^{N_i}$
        - number of such configurations $N!/\prod_i N_i!$
        - probability of the sample
        $$ P = N! \prod_i \frac{q_i^{N_i}}{N_i!}$$
    - for large numbers use Stirling formula: $$ \log P= N D(p\mid\mid q),$$ where $D(p\mid\mid q)$ is the $Kullback-Leibler divergence and $p_i=N_i/N$

- **Kullback-Leibler divergence**, **cross-entropy**
    - measure of the distance of two probability distributions $p$ and $q$
        $$ D(p\mid\mid q) = -\sum_i p_i \ln \frac{p_i}{q_i}$$
    - for $p_i=0$ or $1$ it reduces to the cross entropy
        $$ D_{cross-entropy}(p\mid\mid q) = \sum_i p_i \ln q_i$$