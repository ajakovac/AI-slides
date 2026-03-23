
- **linear regression**:
    > fit a linear data model to the data
    - **data**: sample data with $C\sim\mathbb R^N$, $\mathcal C\sim\mathbb R^M$
    - **basis functions**: $g_\alpha:C\to\mathcal C$ for $\alpha=1,\dots,N_{basis}$
    - **data model**: $\mathcal M(x; q) = \sum_\alpha q_\alpha g_\alpha(x_a)$
    - **matrix notation**: $X_{a\alpha} = g_\alpha(x_a)$
    - **loss**: Gaussian loss $$L(q) = \sum_{a=1}^{N_{data}} \dfrac{|\mathcal M(x_a; q)-y_a|^2} {\sigma_a^2} = (X\cdot q-y)^T C^{-1}(X\cdot q-y),$$ where $\sigma_a$ weights the importance of the given data and $C={\text{diag}}(\sigma^2)$.
    - **parameter distribution**: $$L(q) = (q-\mu_q)^T C_q^{-1}(q-\mu_q)$$ Gaussian with  $$\begin{aligned}
     & C_q = (X^T C^{-1}X)^{-1}\\
     & \mu_q = (X^T C^{-1}X)^{-1}X^T C^{-1}y.\\
    \end{aligned}$$
    - **goal**: find the optimal value of the parameter $q=\mu_q$
    - **distribution of the variables in the target space**: in vector notation $y = q\cdot g(x)$, thus it is also Gaussian with $$ \mu_y=\mu_q\cdot g(x),\quad C_y = g^T(x) C_q g(x) $$
    - **examples**
        - __line fitting__
        - __function fitting in functional basis__
        - __role of the weights__
    - **failure modes**
        - __accuracy drop__
        - __overfitting__
        - __interpolation__ problems
        - __extrapolation__
    - **improvements**
        - __pseudoinverse__
        - __regulators__ (__LASSO__, __L2 regulator__, MEM)

- **function fitting in functional basis**
    > we try to best approximate a function in a designated basis
    - **data model**: $F = \sum_{i=1}^N \omega_i g_i$
    - **optimal parameters**: $\omega_{\text{opt}} = (G^T C_x^{-1} G)^{-1} G^T C_x^{-1} y$
    - **role of covariance matrix**: __role of the weights__
    - **examples**
        - __line fitting__
        - __approximation of a random function__
        - __high order polynomial fit__


- **line fitting**
    > given the data points, fit a line (or a hyperplane) on them
    - **data model**: linear regression with $M=1$ (one dimensional output) and $g_0=1,\;g_1=x$
    - **notation**: $\langle u\rangle = \dfrac{\sum_n u_n/\sigma_n^2}{\sum_n 1/\sigma_n^2}$ and $\dfrac1{\sigma^2} = \sum_n\dfrac1{\sigma_n^2}$
    - **better representation**: $\xi = x-\langle x\rangle, \eta = y-\langle y\rangle \Rightarrow \xi = a\eta +b$
    - **from the general formula** $$C_q^{-1} = X^T C^{-1} X =  \dfrac 1{\sigma^2}\left( \begin{matrix}1 & 0 \cr 0 & \langle \xi\xi\rangle\cr \end{matrix}\right),\quad X^TC^{-1}y = \dfrac 1{\sigma^2}\left( \begin{matrix}\langle \xi\eta \rangle \cr \langle \eta\eta\rangle \cr\end{matrix}\right)$$
    - **relevant parameters**
        - $a_* = {\langle \xi\xi\rangle}^{-1}{\langle \eta\eta\rangle},\; b_* = \langle \xi\eta\rangle,\; C_y = \sigma^2(1 + \xi{\langle \xi\xi\rangle}^{-1}\xi)$
    - **example**: ![line fitting example](../Images/line-fitting.png)

- **role of the weights**
    > the weights (in general the covariance matrix) sets the importance of the individual data points
    - **example**: ![line fitting for uniform and variable weights](../Images/role-of-weight.png)

- **approximation of a random function**:
    > example for function fitting
    - **construction**
        - create random function, e.g. with recursion $x_{n+1} = K(2x_n-x_{n-1}+\sigma\xi)$ with $\xi$ uniform normal random variable. With $K=0.9, \sigma=0.1$ $\to$ ![random function](../Images/random-function.png)
        - choose a functional basis, for example $g_\alpha(t)=(\sin \alpha t, \cos\alpha t)$
        - use fit formulae from linear regression
    - **lessons**
        - observe __accuracy drop__ $\to$ ![fitting with different number of basis elements](../Images/fitting-bad-convergence.png) and ![accuracy drop in fitting](../Images/accuracy-drop.png)
        - apply __regulators__ or __pseudoinverse__ $\to$ ![pseudoinverse regulated fit](../Images/random-function-fit-pinv.png)
    
    - **coefficients with different regulator**: ![fit coefficients](../Images/fit-coefficients-regulator.png)


- **accuracy drop**:
    > symptom: while increasing the number of basis elements, accuracy drops
    - **reason**: __ill-conditioned matrix__ in the solution
    - **solution**
        - __pseudoinverse__
        - __regulators__

- **ill-conditioned matrix**
    > symptom: matrix inverse is numerically inaccurate
    - **reason** 
        - near zero modes (flat direction) of the linear coefficient matrix
        - formally $A\cdot v_{min}=\lambda_{min} v_{min}$ for $\lambda_{min}$ (relatively) small
    - **explanation**
        - if the exact solution is $A\cdot x=y$, then $$A\cdot(x + cv_{min}) = y + c\lambda_{min} v_{min}.$$
        - for $c\lambda_{min}<\varepsilon$, where $\varepsilon$ is the numerical resolution, the difference is not observable.
    - **example**: numerical precision $\varepsilon =10^{-16}$, smallest eigenvalue $\lambda_{min}\sim 10^{-16}$, then solution is uncertain $x+cv_{min}$ with $|c|\sim1$.

- **pseudoinverse**
    > change the matrix inversion process to avoid numerical instabilities
    - works for positive definite hermitian matrices
    - **formula** 
        - $\text{pinv}(A) = V \text{reg-inv}(\Lambda)V^{-1}$
        - $AV=V\Lambda$ is the eigenequation
        - $\text{reg-inv}(\Lambda) = \text{diag}\left(\Theta(\lambda_i>\varepsilon\lambda_{max}) \dfrac1{\lambda_i}\right)$, we keep only those eigenvalues that are larger than $\varepsilon$ times the largest eigenvalue
    - **background** 
        - for small eigenvalue $\lambda_{small}$ the result of $Ax=y$ can be modified by $x\to x+cv_{small}$
        - seek $c$ where the length of the result is smallest $\Rightarrow c=0$
        - results in leaving out the contribution of $v_{small}$

- **regulators**
    > add terms to the loss function to avoid numerical difficulties at the minimum
    - **problem**: minimum of the loss function is numerically problematic
    - **solution** 
        - modify the loss by adding a regulator function of the parameter with some coefficient: $$L_{reg}(q) = L(q) + \lambda_{reg} R(q)$$
        - $\lambda_{reg}=0$ falls back to unregulated case
        - $\lambda_{reg}\to\infty$ regulator dominates
        - optimal $\lambda_{reg}$ does not spoil accuracy too much
    - **result**: resolves (nearly) flat directions in $q$s, makes solution unique
    - **tradeoff**: the minimum is not exact, but numerically stable
    - **types**: __LASSO__, __L2 regulator__, MEM

- **LASSO**:
    > L1 regulator
    - **regulator term**: $R(q) = \sum_q|q|$
    - **properties**
        - prefers $q=0$
        - prefers the possibly most number of small parameters (for at least quadratic losses) $\to$ ![fit coefficients](../Images/fit-coefficients-regulator.png)
        - reason: for 2d: $(q^2-1)^2 + \lambda_{reg}(|q_1|+|q_2|)$ has a minimum at $q=(\pm 1,0)$ or $q=(0,\pm1)$ ![minimum value](../Images/LASSO_preference.png)


- **L2 regulator**
    > L2 regulator
    - **regulator term**: $R(q) = \sum_q q^2$ quadratic distance
    - **properties**
        - prefers $q=0$
        - in linear regression exactly solvable $$q = (X^T C^{-1}X+\lambda_{reg})^{-1}X^T C^{-1}y$$

- **interpolation**
    > approximate a function based on points inside the volume where the points reside
    - **description**
        - sample pairs are given inside a volume (interval) $D$
        - fit a function on $D$
        - predict values at $x\in D$ $\to$ interpolation 
    - **danger**: __overfitting__, learn the noise as data
    - **solution**: regularization $\to$ __regulators__

- **high order polynomial fit**
    > use polynomials to fit a function
    - **construction**: fit high order polynomial fit to a function
    - **dangers**
        - interpolation can produce large amplitudes, not smooth $\to$ __overfitting__
        - example: original model $y=1-x^2+\text{noise}$, fit for $N_{data}=11$ a 10th order polynomial, or regularize with L2 ![interpolation overfitting](../Images/interpolation-overfitting.png)
        - problem with __extrapolation__
    - **lesson**: avoid polynomial fits!

- **extrapolation**
    > approximate a function based on points outside the volume where the points reside
    - **dangers**
        - good interpolation, but outside the data domain function value grows large $\to$ bad asymptotic behaviour
        - example: original model $y=1-x^2+\text{noise}$ ![fit different order polynomials with L2 regularization](../Images/extrapolation-example.png)
    - **solution**
        - regulation does not help
        - control asymptotic behaviour

- **gradient descent**
    > method to find minimum of a function: go downhill!
    - recursive process to find minimum of $f(x)$
    - **algorithm**
        - recursion: start from an appropriate $x_0$, and perform recursion $$x_{n+1} = x_n - r\nabla f,$$ where $r$ is the step size (learning rate)
        - stop if $|\nabla f|$ is small, or $r$ is small (if it is changed)
    - **proof** 
        - $f(x_{n+1})= f(x_n- r\nabla f) = f(x_n)-r|\nabla f|^2 +\text{higher order terms}$
        - as long as linear approximation applies, the value decreases
    - **advantages**
        - simple
        - robust
        - scalable
    - **disadvantages**
        - can stuck in local minima in nearly flat directions
        - can overstep minimum
        - can be slow for strongly non-isotropic functions
    - **improvements**
        - use __momentum methods__ (Nesteron momentum, ADAM)
        - __change learning rate__
        - __conjugate gradient descent method__
        - second-order methods $\to$ __Newton-Raphson method__

- **change learning rate**
    > decrease step size near the minimum
    - **algorithm**
        - use a recursion with $x_{n+1}=x_n + r\delta x_n$ to find minimum of $f(x)$, $r$ is learning rate
        - systematic change: $r\to \alpha r$ where $\alpha<1$
    - **adaptive change**
        - if $f_{n+1}<f_n: \; r\to \alpha_{grow}r$, $\alpha_{grow}>1$, for example 1.2
        - if $f_{n+1}>f_n: \; r\to \alpha_{decr}r$, $\alpha_{decr}<1$, for example 0.5
    - **stopping**: propose stopping recursion if $r<r_{min}$
    - **example**: $f(x,y) =(x-2)^2+(y+1)^2 + \sin 3x \sin 3y$, use adaptive step size ![adaptive step iteration](../Images/adaptive-step-iteratio.png)

- **random algorithms**
    > find minimum of a function locally stepping in a random direction
    - **methods**
        - __coordinate descend__
        - __simulated annealing__
    - **advantages**
        - no gradient is needed
        - can escape local minima
        - parallelizable
    - **drawbacks**
        - slow convergence
        - difficult to use in batch methods $\Rightarrow$ rarely used in __DNNs__
    - **example**: $f(x,y) =(x-2)^2+(y+1)^2 + \sin 3x \sin 3y$, simulated annealing with $\alpha_{cooling}=0.98$: ![minimum finding with annealing](../Images/minimum-finding-annealing.png)
    

- **coordinate descend**
    > choose a random direction and minimize function there
    - minimize function in a random direction (line search): $$x_{n+1} = \arg\min_t f(x_n+td_n),$$ where $d_n$ is a random direction
    - optionally: only make one step towards the minimum

- **simulated annealing**
    > accept a step even if it does not decrease the function
    - **algorithm**
        - create an ensemble according to probability distribution $P(x)\sim e^{-\beta f(x)}$, where $\beta=1/T$ is the inverse "temperature" $\to$ e.g. __Metropolis algorithm__
        - high temperature: minimum is blurred
        - low temperature: distribution concentrated around global minimum
        - decrease temperature (annealing) to get into a minimum: $T\to \alpha_{cooling}T$ (e.g. $\alpha_{cooling}=0.98$)
        - reheat + repeat annealing for exploring minima

- **Metropolis algorithm**
    > algorithm to create a Markov process with given statistical properties
    - **goal** 
        - produce an ensemble with probability distribution $P(x)\sim e^{-\beta f(x)}$
        - generate a Markov process $x_n\to x_{n+1}$, the values will have the desired distribution
    - **algorithm**
        - propose step $x_{n+1}=x_n+v$ where $v$ is a random vector
        - compute the change in the function $\Delta f=f(x_{n+1})-f(x-n)$
        - accept step with probability $p_{accept}=\min(1, e^{-\beta\Delta f})$
        - if $\Delta f<0$ surely accept
        - if $\Delta f>0$ may accept
    - **thermalization**: distribution becomes stable after the first $n_{therm}$ step.

- **conjugate gradient descent method**
    > the direction we follow is not the local gradient, but we take into accout the surroundings, too
    - **objectives**
        - planned to effectively minimize a quadratic function $$f = x^TA x - b^T x + f_0,$$ where $x\in\mathbb R^N$ and $A$ is positive definite
        - gradient descend slow, if there are nearly flat directions (valleys)
    - **idea**
        - recursion $x_k$
        - each step occurs in conjugate directions
        - converges in $N$ steps (if exact)
    - **conjugate directions**: $p$ and $q$ are called $A$-conjugate if $p^TAq=0$.
    - **algorithm**: uses auxiliary quantities $r$ (residual) and $p$ (conjugate directions)
    - **algorithm steps**
        - start with $x_0$, $r_0=b-Ax_0$, $p_0=r_0$
        - step size: $\alpha_k = \dfrac{r_k^Tr_k}{p_k^TAp_k}$ (exact line minimization in direction $p_k$, using orthogonality)
        - update position: $x_{k+1}=x_k+\alpha_k p_k$
        - update residual: $r_{k+1}=b-Ax_{k+1} = r_k - \alpha_kAp_k$
        - compute conjugacy coefficient: $\beta_k = \dfrac{r_{k+1}^Tr_{k+1}}{r_k^Tr_k}$
        - update direction: $p_{k+1}=r_{k+1}+\beta_k p_k$
        - **STOP** if $r_{k+1}<\varepsilon$ (in exact case after $N$ steps)
        - **REPEAT** from 2.
    - **theory**
        - $r_i^T r_j=0$ for $i\neq j$ orthogonal
        - $p_i^TAp_j=0$ for $i\neq j$: $A$-conjugate
    - **exmaple**: ![conjugate gradient method](../Images/conjugate-gradient.png)

- **Newton-Raphson method**
    > minimization algorithm taking into account second order approximation of the function
    - **goal**: minimize a function $f:\mathbb R^N\to\mathbb R$
    - **quadratic approximation**
        - $$f(x+p) = f(x) + p\nabla f(x)+\frac12 p^TH(x) p+\dots,$$ where $H(x)$ is the Hessian $H(x)=\nabla^2f(x)$.
        - for exact quadratic form the minimum is at $p=-H(x)^{-1}\nabla f(x)$
    - **recursion**
        - $x_{k+1} = x_k - \alpha_kH(x_k)^{-1}\nabla f(x_k)$
        - $\alpha_k\le1$ is the damping factor for numerical stability
    - **advantage**: fast convergence
    - **disadvantage**: needs second derivative

- **high dimensional optimization**
    > optimization in high dimensions has special issues
    - **problems in high dimensional spaces** lot of critical points
    - **critical points**
        - saddle points (minimum in some direction, maximum in others)
        - flat regions with mixed curvature
        - wide valleys with many equivalent solutions
    - **solution**
        - locally optimal direction $p(x)$ (e.g. $p(x)=-\nabla f(x)$ in gradient descend)
        - actual update $x_{k+1}=x_k+v_k$, not exactly toward the optimal direction
    - **methods to find the actual direction**
        - stochastic gradient: $v(x)=rp(x) + \xi$ with some noise
        - __momentum methods__

- **momentum methods**
    > in minimum finding avoid shallow minima by overunning over them
    - **direction choice**: locally optimal direction $p(x)$, actual direction $v_k$ recursively determined
    - **classical momentum (Polyak)**
        - $v_{k+1} = \beta v_k + \eta p(x_k)$
        - slowly takes over new direction
        - effective in narrow valleys
    - **Nesterov accelerated gradient (NAG)**
        - $v_{k+1} = \beta v_k + \eta p(x_k+\beta v_k)$
        - anticipates future direction
    - **ADAM**
        - adaptive step size
        - most widely used
        - algorithm updates step size as well
    $$\begin{aligned}
     & v_{k+1} = \beta_1 v_k + (1-\beta_1) p(x_k)\\
     & m_{k+1} = \beta_2 m_k + (1-\beta_2) p^2(x_k)\\
     & x_{k+1} = x_k + \eta \dfrac{v_k}{\sqrt{m_k}+\varepsilon}\\
    \end{aligned}$$

