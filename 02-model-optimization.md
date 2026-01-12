# Model optimization

This section describes the conceptual and mathematical foundations of model optimization,
from data representation to probabilistic modeling and optimization methods.

---

<a id="context-change"></a>
- **context change** ↩ [function](mathematics_basics.md#function)
    - domain: [context](#context), $X$
    - range: [context](#context), coarsening of domain, $Y$
    - possible functions: ${\cal F}$
        - assume finite sets
        - ${\cal F} = \{ X \to Y \mid |X|=K,\; |Y|=L \}$
        - $|{\cal F}| = L^K$
        - very large function space
    - model space: parametrized subset of ${\cal F}$
    - parameters: $P \subset \mathbb{R}^M$
    - model: $F : X \times P \to Y$
    - optimization: model optimization
    - examples:
        - [pattern recognition](#pattern-recognition)
        - [data compression](#data-compression)
    - context definition in AI:
        - data-driven learning
        - input–output pairs

---

<a id="pattern-recognition"></a>
- **pattern recognition**
    - definition: finding meaningful classes from raw data
    - basic context:
        - pixels
        - audio samples
        - raw sensor data
        - $X \sim \mathbb{R}^N$
    - target context:
        - object classes
        - $Y = \{c_1, \dots, c_K\}$
    - examples:
        - image classification
        - speech recognition

---

<a id="data-compression"></a>
- **data compression**
    - definition: represent data with fewer bits by removing irrelevant features
    - basic context:
        - pixels
        - audio samples
        - raw sensor data
        - $X \sim \mathbb{R}^N$
    - target context:
        - compressed representation
        - $Y \sim \mathbb{R}^M,\; M < N$
    - examples:
        - image compression
        - audio compression

---

<a id="data-driven-approach"></a>
- **data driven approach**
    - definition: learning a model from raw data without explicit labels
    - context definition:
        - implicit patterns
        - temporal subsequences
        - symmetries
        - distances
    - goal: find features of the target context
    - data:
        - $X_{\text{sample}} \subset X$
    - examples:
        - image clustering
        - discovering physical laws
        - dimensionality reduction
    - methods:
        - autoencoders
        - generative models
        - principal component analysis
        - linear laws discovery
        - contrastive learning

---

<a id="input-output-pairs"></a>
- **input–output pairs** ↩ [countable set](mathematics_basics.md#countable-set)
    - description: input–output pairs sampled from a context change
    - input context: [context](#context)
    - output context: [context](#context), labels
    - sample space: subset of input context
    - sample values: subset of output context
    - data:
      $(x,y)$ pairs, where  
      $x \in$ sample space,  
      $y \in$ sample values
    - assumption:
        - independent measurements
    - failure modes:
        - [corrupted label](#corrupted-label)
        - [not enough information](#not-enough-information)
    - examples:
        - what is on an image?
        - what is the word the speaker says?

---

<a id="not-enough-information"></a>
- **not enough information**
    - definition: a given input leads to different labels
    - formulation:
      labels are not measurable with respect to the input context
    - cause: input contains insufficient information
    - consequence: probabilistic methods are required

---

<a id="corrupted-label"></a>
- **corrupted label**
    - definition: label does not correspond to the class of the input
    - causes:
        - human mistake
        - systematic error

---

<a id="probabilistic-data-model"></a>
- **probabilistic data model** ↩ [context change](01-basics.md#context-change)
    - dataset: [input–output pairs](#input-output-pairs), $D$
    - domain: input context of the dataset, $X$
    - range: output context of the dataset, $Y$
    - true conditional distribution: probability of measuring a value given the input
    - loss function: $\ell : Y \times Y \to \mathbb{R}$
    - probability: $P$
    - conditional distribution: $P(y \mid x,\omega) \sim e^{-\ell(y,F(x,\omega))}$

---

<a id="gaussian-loss"></a>
- **Gaussian loss**
    - covariance matrix: $C_x$
    - chi-squared function:
      $\chi^2(y,y') = (y-y')^T C_x^{-1} (y-y')$
    - loss function:
      $\ell = \chi^2$

---

<a id="mse-loss"></a>
- **MSE loss**
    - definition: mean squared error loss
    - loss function:
      $\ell(y,y') = |y-y'|^2$

---

<a id="l-p-loss"></a>
- **$L_p$ loss**
    - definition: loss based on $L_p$ distance
    - power parameter: $p \in \mathbb{R}$
    - loss function:
      $\ell(y,y') = (|y-y'|^p)^{1/p}$

---

<a id="kullback-leibler-loss"></a>
- **Kullback–Leibler loss**
    - conditions:
        - $p,q$ are probability distributions
        - $\sum_i p_i = 1,\; p_i \in [0,1]$
        - $\sum_i q_i = 1,\; q_i \in [0,1]$
    - loss function:
      $\ell(p,q) = \sum_i p_i \log(p_i/q_i)$

---

<a id="cross-entropy-loss"></a>
- **cross entropy loss**
    - conditions:
        - $p_i \in \{0,1\}$
        - $q$ is a probability distribution
        - $\sum_i q_i = 1,\; q_i \in [0,1]$
    - loss function:
      $\ell(p,q) = -\sum_i p_i \log(q_i)$

---

<a id="likelihood"></a>
- **likelihood** ↩ [probabilistic data model](#probabilistic-data-model)
    - description:
      probability of measuring the observed dataset given the model
    - formulation:
      $L : {\cal P} \to [0,1]$
    - definition:
      $L(\omega) = P(D \mid \omega)
      = \prod_{(x,y)\in D} P(x,y \mid \omega)$
    - total loss function:
      $\ell(\omega) = \sum_{(x,y)\in D} \ell(y,F(x,\omega))$

---

<a id="parameter-distribution"></a>
- **parameter distribution** ↩ [likelihood](#likelihood)
    - posterior:
      $P(\omega \mid D)$
    - parameter prior:
      $P(\omega)$
    - value prior:
      $P(D)$
    - Bayes relation:
      $P(\omega \mid D) = \frac{P(D \mid \omega) P(\omega)}{P(D)}$
    - assumptions:
        - flat priors
        - $P(\omega)=\text{const}$
        - $P(D)=\text{const}$
    - approximation:
      $P(\omega \mid D) \sim L(\omega)$
    - normalization:
      $\int_{\omega\in{\cal P}} P(\omega \mid D)=1$

---

<a id="confidence"></a>
- **confidence** ↩ [parameter distribution](#parameter-distribution)
    - confidence levels:
        - definition:
          $P(\omega \in S_p \mid D)=\text{const}$
        - $S_p$: hypersurface in ${\cal P}$
    - confidence regions:
        - volume $V_p \subset {\cal P}$
        - boundary $\partial V_p = S_p$
    - parametrization:
      $\int_{\omega\in V_p} P(\omega \mid D)=p$

---

<a id="model-optimization"></a>
- **model optimization** ↩ [parameter distribution](#parameter-distribution)
    - definition:
      finding optimal parameter values for given input–output pairs
    - general methods:
        - maximize parameter distribution
        - maximum likelihood estimation (MLE)
        - $\frac{\partial \ell}{\partial \omega}=0$
    - failure modes:
        - underfitting
        - overfitting
        - bad convergence
        - label noise sensitivity
        - dataset shift
        - shortcut learning
    - optimization methods:
        - function fitting in functional basis
        - gradient descent
        - conjugate gradient descent
        - random algorithms
        - second-order optimization

---

<a id="underfitting"></a>
- **underfitting**
    - definition:
      $F(x,\omega)$ cannot approximate $G(x)$ for any $\omega$
    - solution:
      increase model capacity

---

<a id="overfitting"></a>
- **overfitting**
    - definition:
      good approximation on $X_{\text{sample}}$ but not on $X\setminus X_{\text{sample}}$
    - solution:
      regularization

---

<a id="bad-convergence"></a>
- **bad convergence**
    - definition:
      flat directions near optimum
    - solution:
      regularization, better conditioning

---

<a id="dataset-shift"></a>
- **dataset shift**
    - definition:
      $P_{\text{sample}}(X) \neq P(X)$
    - solution:
      domain adaptation

---

<a id="label-noise-sensitivity"></a>
- **label noise sensitivity**
    - definition:
      small label noise causes large performance degradation
    - mitigations:
        - data cleaning
        - robust losses
        - regularization
        - reweighting
        - noise-aware models

---

<a id="shortcut-learning"></a>
- **shortcut learning**
    - definition:
      model learns spurious correlations instead of causal structure
    - causes:
        - dataset bias
        - label leakage
        - insufficient context variability
    - mitigations:
        - targeted augmentation
        - controlled data collection
        - adversarial training
    - examples:
        - background-based image classification
        - channel-noise-based speech recognition

---

<a id="function-fitting-functional-basis"></a>
- **function fitting in functional basis** ↩ Gaussian loss
    - data model:
      $F = \sum_{i=1}^N \omega_i g_i$
    - optimal parameters:
      $\omega_{\text{opt}} = (G^T C_x^{-1} G)^{-1} G^T C_x^{-1} y$
    - examples:
        - linear regression
        - role of covariance matrix

---

<a id="gradient-descent"></a>
- **gradient descent**
    - recursion:
      $x_{n+1} = x_n - r\nabla f$
    - advantages:
        - simple
        - robust
        - scalable
    - disadvantages:
        - slow convergence
        - local minima
        - ill-conditioning
    - improvements:
        - momentum
        - adaptive step size
        - second-order methods
