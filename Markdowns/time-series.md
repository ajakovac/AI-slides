- **time series analysis**
    > try to find features for a time series
    - **theoretical basis**
        - __time evolution__, __time evolution in a context__
    - **representation in AI**
        - __RNN__ (recurrrent neural networks)
        - __LSTM__ (Long Short-Term Memory)
        - __time series representation via embedding and prediction__
        - __PINNs__ (Physics-Informed Neural Networks)
        - __TCNs__ (Temporal Convolutional Networks)

- **time evolution**
    - **formally**: $\tau: \Omega\times dT \to \Omega$
    - **assumptions**
        - assume the complete world is fully deterministic
        - Markov process
        - depends only on the time difference (not the absolute time)
    - **consistency**: $\tau(\omega, t_{ac}) = \tau(\tau(\omega,t_{ab}),t_{bc}))$
    - **change vs conservation**
        - __goal of living beings__

- **time evolution in a context**
    > map time evolution onto a context
    - **formally**: $(\mathcal C, dt) \mapsto \Pi_\mathcal{C}(\tau(\omega, dt))$, where $\tau$ is the __time evolution__ of the system

- **goal of living beings**
  > all living beings (agents) must secure the mainanence of its own life and also the existence of its species
  - **goal**: survival in a complex environment
  - **tools**
    - must observe the world, and make decision according to the actual state: __prediction__
    - only partial observation is possible $\to$ __conceptual foundations__, observed world, __contextual prediction__
    - has to react to the environmental issues: $\text{issue}\to\text{action}$
    - changing environment $\to$ adaptation (learning)
  - **decisions**
    - __action focused decision__
    - __model based decision__

- **action focused decision**
    > sensory input leads directly to action
    - **corresponds to**
        - __direct representation__, __System I__
        - fast and accurate (if appropriate)
        - ![mental model](../Images/mental-model-System-I.png)
    - **critics**: world becomes too complicated to have a reaction to all possible environemntal situations

- **model based decision**
    > the agent maintains an up-to-date representation of the world
    - **algorithm**
        - sensory input leads to updating the representation
        - representation can be used to try model scenarios (thinking)
        - decision after tried a sufficient number of scenarios
    - **properties**: slower, general, less accurate in specific cases
    - **corresponds to**
        - __System II__
        - ![mental model](../Images/mental-model-System-II.png)
        - ![detailed mental model](../Images/mental-model-System-II-detailed.png)

- **prediction**
    > tell the future before it happens
    - __time evolution__ must be predicted in order to be able to prepare the future
    - exact prediciton is possible only from the complete world $\to$ impossible in practice
    - we need __contextual prediction__

- **contextual prediction**
    > we have limited information about the world, need to make the best possible prediction
    - **goal**
        - try to predict __time evolution in a context__ $\mathcal C$
        - must not be exact $\to$ errors in prediction
    - **time evolution model**: $M: (c, t)\mapsto (c', t')$, where $c,c'\in\mathcal C$
    - **examples**
        - mechanical motion: $c$ contains the configuration data and the velocities, $t'=t+dt$, differential equation if $dt\to0$
        - large language models: $c$ is the complete textual history, $t'$ is the next token
    - **treatment of errors**
        - expected value of the outcomes of time evolution starting from $c$ $\to$ __deterministic evolution__
        - statistical representation of the distribution around the expected value $\to$ __stochastic evolution__

- **deterministic evolution**
    > evolution of expected values of an observation
    - **strategy**
        - start from a context state $x$, and observe to possible outputs from this state after a time $dt$
        - assume no explicit time dependence (otherwise time is an element of the context)
        - everything depends on $dt$, we do not write out this dependence
    - **errors**
        - $y$ is not unique $\to P(y\mid x)$
        - we expect a lot of independent effects $\Rightarrow$ $p$ is Gaussian $$P(y\mid x) =\mathcal N(M(x), C(x))(y),$$ the expected value is described by the model
    - **construction**
        - we use a parametrized __data model__ $\mathcal M(x,\omega)$ where $\omega\in\mathcal Q$ are parameters
        - the model may come from human intuition or coming from a functional space
        - typically __differential equations__ or __differentia equations__ (recursions), for spatially distributed quantities __partial differential equations__
    - **parameter estimation**
        - approximate distribution of observed quantities $$ P(y\mid x, \omega) \sim e^{-\ell(y, \mathcal M(x,\omega))},$$ where $\ell(y,\mu) = \frac12 (y-\mu)^T C^{-1}(y-\mu)$ loss function
        - if the correlation matrix is not known, other approximate forms can be used for $\ell$ (like KL divergence)
        - __likelihood__
        - __parameter distribution__, maximum likelihood and __confidence__ levels

- **likelihood**
    > probability of measuring the observed dataset given the model $\mathcal M(x,\omega)$
    - likelihood is a $L : \mathcal Q \to [0,1]$ function
    - **calculation**
        - definition: $D$ sample data, assume independent measurements
          $L(\omega) = P(D \mid \omega)
        = \prod_{(x,y)\in D} P(x,y \mid \omega)$
        - total loss function:
            $\ell(\omega) = \sum_{(x,y)\in D} \ell(y,\mathcal M(x,\omega))$

- **parameter distribution**
    > what is the probability of a given parameter choice, if we see the observed data and know the model
    - it is not really a probability (no corresponding event space exists)
    - **goal**: find $P(\omega \mid D)$ (posterior)
    - **priors**
        - parameter prior: $P(\omega)$
        - value prior: $P(D)$
    - **Bayes relation**: $P(\omega \mid D) = \dfrac{P(D \mid \omega) P(\omega)}{P(D)}$
    - **assumptions**
        - flat priors
        - $P(\omega)=\text{const}$
        - $P(D)=\text{const}$
        - follows: $$P(\omega \mid D) \sim L(\omega)$$
    - **best parameter**: maximum likelihood
    - **normalization**: $\int_{\omega\in\mathcal Q} P(\omega \mid D)=1$

- **confidence** 
    > how well defined the optimal parameter set?
    - **confidence levels**: $S_p$ hypersurface in the parameter space ($\mathcal Q$) where $P(\omega \in S_p \mid D)=\text{const}$
    - **confidence regions**
        - volume $V_p \subset \mathcal Q$
        - boundary $\partial V_p = S_p$
    - **parametrization**: $\int_{\omega\in V_p} P(\omega \mid D)=p$

- **differentia equations**
    > time evolution is described as a recursion from the past data
    - **time dependence**: $f:\mathbb R\to W$ where $W\sim \mathbb R^N$ (value) are vector spaces
    - **assumptions**
        - deterministic evolution
        - Markov process
        - assume there exists a function $F_{\Delta t}$ for all $\Delta t$ (time step) that $$f(t+\Delta t) = f(t) + \Delta t F_{\Delta t}(f(t))$$
    - **initial conditions**
        - to determine full time evolution, we need to fix $N$ values
        - also called order of the recursion or degrees of freedom
        - can be $f(t_0)\;\to$ initial conditions
        - or it can be $f_a(t_i)$ for eventually different $t_i$ times (e.g. boundary conditions)
        - in extreme case $f_0(t)$ for $t\in\{t_1,\dots,t_N\}$ (or similarly for other components)
    - **time embedding**
        - give $f_0(t+n\Delta t)$ for $n=0,1,\dots N-1$ for fixed $a$
        - determines full time evolution (c.f. __delay embedding__ and __Takens' theorem__)
        - leads to a recursion equivalent to the original time series $$f_0(t) = \mathcal G(f_0(t-\Delta t),\dots f_0(t-N\Delta t))$$

- **differential equations**
    > limit of the differentia equations in the $\Delta t\to0$ limit
    - **continuum limit**
        - $\Delta t\to 0$
        - time derivative $$\partial _t f = \dot f= \lim_{\Delta t\to0}\dfrac{f(t+\Delta t)-f(t)}{\Delta t}$$
        - evolution equation becomes a differential equation $$\partial_t f = F_0(f)$$
    - **advantages**
        - simpler form (we not need to give an account for terms vanishing in the continuum limit)
        - time translation symmetry leads to __conserved quantity__ (Noether theorem, energy)
    - **disadvantages**
        - in reality we do not know the time in arbitrary resolution

- **conserved quantity**
    > a function of features that do not change under time evolution
    - **examples**
        - with $v(t)=\dfrac{f(t+\Delta t)-f(t)}{\Delta t}$ we have $E = v- F_{\Delta t}(f) \equiv 0$ (equation of motion)
        - energy of a harmonic oscillator $$\left\{\begin{cases}& \dot x= y\\ &\dot y = -\omega^2 x\\ \end{cases}\right\}\Rightarrow E = \omega^2 x^2 +y^2$$
    - **Noether theorem**
        - a continuous symmetry leads to a conserved quantity

- **partial differential equations**
    > describes evolution in multiply continuous space (typically spacetime)
    - **spatial-temporal configurations**
        $f(t,x)$, where $x\in V\sim \mathbb R^d$ $d$ dimensional space
        - formally: multicomponent function $f_x(t)=f(t,x)$, space is an index
    - **assumption**
        - local evolution
        - neighborhood of $x$ is $V_x\subset V$
        - time update comes only from a local neighborhood $$f(t+\Delta t,x) = f(t,x) + \Delta t F_{\Delta t}(\{f(t,y)\mid y\in V_x\})$$
        - less degrees of freedom than expected, but still a lot
    - **initial conditions**
        - theoretically: full configuration in the complete space $\to$ usually not available
        - sampling space in a grid $\to$ not enough data for a complete time evolution
        - earlier time data $\to$ fewer information, diffusion, information loss

- **RNN**
    > try to represent reality as a hidden layer in a neural network
    - **alternative name**: recurrent neural network
    - **purpose**
        - model sequential / time-dependent data
        $$
        x_1, x_2, \dots, x_T \;\mapsto\; y_1, y_2, \dots, y_T
        $$
    - **internal (hidden) state**
        - goal is to represent the past
        - updated in each timestep
        $$
        h_t = f(h_{t-1}, x_t)
        $$
    - **recurrent structure**
        - output (or hidden state) is fed back as input at the next time step
        - same parameters are reused across time (weight sharing)

    - **unfolding in time**:
        - RNN can be unfolded into a deep feed-forward network of depth $T$
        - each layer corresponds to one time step
        - training performed via *backpropagation through time* (BPTT)
        - ![unfolding of recurrent neural networks](../Images/unfolding-recurrent-networks.png)

    - **theoretical properties**:
        - expressive enough to approximate sequence-to-sequence mappings
        - in principle can capture long-range dependencies

    - **problems**:
        - __vanishing gradient__ or __exploding gradient__ is severe problem (number of layers is infinite due to unfolding)
        - limited effective memory in practice

- **delay embedding**
    > past data are taken into account as present degrees degrees of freedom
    - **construction**
        - time series: $x(t_1), x(t_2), \dots, x(t_T)$
        - delay vectors: $$
      \mathbf y_t =
      \big(
      x(t),\ x(t-\tau),\ \dots,\ x(t-(m-1)\tau)
      \big)
      \in \mathbb R^m
      $$
    - **parameters**
        - $m$: embedding dimension
        - $\tau$: delay time
    - **theoretical result**: __Takens' theorem__

- **Takens' theorem**
    > with delayed embedding the important features of any time series can be captured
    - for a generic observation function and sufficiently large $m$,
      the delay embedding is a **diffeomorphic image** of the true state space
    - topological and geometric properties of the original system are preserved
    - implies that a single measured quantity can encode the full dynamics

- **LSTM**
    > solution for the unstable gradient problem of RNNs
    - **alternative name**: Long Short-Term Memory
    - **motivation**
        - address vanishing gradient problem of plain __RNN__s
        - enable learning of long-term dependencies

    - **core idea**
        - introduce an explicit **memory cell** with controlled information flow
        - separate *storage* from *exposure* of information

    - **components**:
        - **cell state** $c_t$: long-term memory
        - **hidden state** $h_t$: exposed representation
        - **input gate** $i_t$: controls how much new information is written
        - **forget gate** $f_t$: controls how much old memory is retained
        - **output gate** $o_t$: controls what part of memory is revealed

    - **gate dynamics**:
        $$
        f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f)
        $$
        $$
        i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i)
        $$
        $$
        c_t = f_t \odot c_{t-1} + i_t \odot \tilde c_t
        $$
        $$
        h_t = o_t \odot \tanh(c_t)
        $$
        - gates use sigmoid activations $\in [0,1]$
        - memory update is *additive*, improving gradient flow

    - **advantages**:
        - much more stable training than vanilla RNNs
        - effective for medium-range temporal dependencies
        - historically strong performance in speech, language, and time series

    - **limitations**:
        - complex architecture → many parameters
        - still sequential (poor parallelization)
        - struggles with very long sequences
        - training remains slow compared to modern architectures

    - **historical note**:
        - LSTMs were dominant from ~1997 to mid-2010s
        - today largely replaced by transformers in NLP and many sequence tasks
        - still used in resource-constrained or strictly causal settings

- **time series representation via embedding and prediction**
    > represent the time evolution (recursion) kernel by neural networks
    - **goal**
        - reconstruct the hidden state of a dynamical system
        - learn its temporal evolution for prediction or analysis
    - **construction**
        - use __delay embedding__ $(x(t),\ x(t-\tau),\ \dots,\ x(t-(m-1)\tau)\to y_t$
        - the expected evolution $$\mathbf y_{t+1} = F(\mathbf y_t)$$
        - represent $F$ by __DNNs__ (universal approximation theorem)

    - **advantages**
        - no explicit physical model required
        - flexible and expressive
        - can handle noisy and partially observed systems

    - **limitations**:
        - assumes homogeneous regime (same time evolution)
        - assumes fixed $m$ is enough to represent future $\to$ if not c.f. __transformers__


- **PINNs**
    > PINNs unify representation learning and physical modeling by embedding the governing equations directly into the learning process
    - **alternative name**: Physics-Informed Neural Networks
    - **core idea**
        - learn a function that represents the solution of a dynamical system
        - enforce known physical laws directly in the loss function
        - combine data-driven learning with first-principles constraints

    - **problem setting**
        - given a physical system described by differential equations:
        $$
        \mathcal F\big(u(x,t), \partial_t u, \nabla u, \nabla^2 u, \dots\big) = 0
        $$
        - where $u(x,t)$ is the unknown state (field, trajectory, solution)

    - **neural representation**
        - approximate the state by a neural network:
        $$
        u(x,t) \approx u_\theta(x,t)
        $$
        - network input: space, time, parameters, boundary conditions
        - network output: physical state variables

    - **physics-informed loss**:
        - total loss is a sum of terms: $$
        \mathcal L =
        \mathcal L_{\text{data}}
        + \lambda_{\text{phys}}\,\mathcal L_{\text{PDE}}
        + \lambda_{\text{bc}}\,\mathcal L_{\text{BC/IC}}
        $$
        - physics residual:
        $$
        \mathcal L_{\text{PDE}}
        =
        \mathbb E\left[
        \big\|
        \mathcal F(u_\theta)
        \big\|^2
        \right]
        $$
        - derivatives are computed via **automatic differentiation**

    - **advantages**
        - strong inductive bias from physics
        - requires less data than purely data-driven models
        - produces physically consistent predictions
        - can interpolate and extrapolate in space and time

    - **limitations**
        - optimization can be difficult (stiff PDEs, competing loss terms)
        - sensitive to loss weighting
        - struggles with chaotic or highly multiscale systems
        - computationally expensive for high-dimensional problems

    - **interpretation**:
        - PINNs replace numerical solvers with function approximation
        - learning becomes constrained by conservation laws, symmetries, and dynamics

- **TCNs**
    > TCNs model time by stacking causal, dilated convolutions, turning sequence learning into a parallel, stable convolutional problem
    - **goal**
        - model sequential / time-series data
        - predict future values from past observations
        - without recurrent connections

    - **core idea**:
        - use 1D convolutions along the time axis
        - enforce *causality*: output at time $t$ depends only on inputs at times $\le t$
        - represent temporal dependencies via convolutional receptive fields

    - **causal convolution**:
        - standard convolution modified so no “future leakage” occurs
        - for input sequence $x_t$:
        $$
        y_t = \sum_{k=0}^{K-1} w_k\, x_{t-k}
        $$
        - ensures suitability for forecasting and online prediction

    - **dilated convolutions**:
        - introduce gaps between convolution taps:
        $$
        y_t = \sum_{k=0}^{K-1} w_k\, x_{t-k\cdot d}
        $$
        - dilation factor $d$ grows exponentially with depth
        - allows very large temporal receptive fields with few layers

    - **effective memory**:
        - receptive field size:
        $$
        R = 1 + (K-1)\sum_{l=0}^{L-1} d_l
        $$
        - can cover long-range dependencies efficiently
        - memory length is explicit and controllable
