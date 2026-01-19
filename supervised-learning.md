# Supervised learning

In this section we discuss the methods used in the practical approaches to describe a context change in System 1.

- **parameters**: $\text{par}\subset\mathbb R^N$
  - $N$ is the number of parameters

<a id="context-change"></a>
- **model** (of context change): $(\mathcal C,\text{par})\to \mathcal C'$, if $\mathcal C'\preceq \mathcal C$
    - examples:
        - [pattern recognition](#pattern-recognition)
        - [data compression](#data-compression)

- **target context**: (model, parameters) $\to$ context, the induced context of a model for a given parameter

- **distance** (of contexts): $(\mathcal C_1, \mathcal C_2) \to \mathbb R$, with the conditions
  - loss $\ge 0$
  - loss $=0$ iff $\mathcal C_1=\mathcal C_2$
  - for context changing distance is $\sum_{c\in\mathcal C} \ell(\Pi_{\mathcal C_1}(c), \Pi_{\mathcal C_2}(c))$, where $\ell$ is the loss function.

- **loss function**: $\mathcal C \times \mathcal C\to \mathbb R^+_0$
  - uses some numerical representation for the classes, then it can be defined as $\mathbb R^N\times\mathbb R^N\to\mathbb R^+_0$

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


<a id="input-output-pairs"></a>
- **labelled samples**: $\{(x,y) \mid x\in\mathcal C, y\in\}$
    - description: data pairs sampled from a context change
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


<a id="model-optimization"></a>
- **optimization** of a model: (context, model) $\mapsto$ model, resulting a better model of the context
    - definition:
      finding optimal parameter values for given labelled samples
    - general methods:
        - maximize parameter distribution
        - loss function minimization
        - $\frac{\partial \ell}{\partial \omega}=0$
    - failure modes:
        - underfitting
        - overfitting
        - bad convergence
        - label noise sensitivity
        - dataset shift
        - shortcut learning
    - optimization methods:
        - linear regression
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
