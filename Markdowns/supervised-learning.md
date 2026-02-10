# Supervised learning

- **supervised learning**: find the context $\mathcal C$ that smoothly represents the provided sample data.
    - examples:
        - [pattern recognition](#pattern-recognition)
        - [data compression](#data-compression)
    - unsupervised is not really meaningful
      - mathematically any partition is possible
      - depends on the "distance" $\to$ data representation
      - easy to manipulate (c.f. university ranking, economic data)
      - needs a clean definition of the context (e.g. temporal-spatial closeness)
      - examples: university ranking, economic or individual performance evaluation, IQ tests
      - see also intelligence in psychology

<a id="sample-data"></a>
- **sample data**: $\{(x_a,y_a) \mid x_a\in C, y\in \mathcal C: x_a\in y_a, a=1\dots N_{data}\}$, where $C=\text{underlying class}(\mathcal C)$
    - assumption:
        - independent measurements
    - failure modes:
        - [corrupted label](#corrupted-label)
        - [not enough information](#not-enough-information)
    - examples:
        - (cat-imege-1,cat), (cat-imege-2,cat), (dog-imege-1,dog), $\dots$ (cat-imege-N,cat), 
        - what is the word the speaker says?

- **sample context**: collect data belonging to the same class
  - formally $\mathcal C_{sample} =\{ \{x_a \mid c_a=c\} \mid c \in\mathcal C\}$

- **data model**: $\mathcal M :(C,Q)\to B$, where $Q$ are the parameters, $B$ is the target (label) set
  - names:
    - if $B$ is a finite set: **classification**
    - if $B$ is continuous: **regression**
  - modelling a context by the induced context $\mathcal M^{-1}(B,q)$
    - example $\mathcal M(\text{image}, q_{opt}) = \text{cat}$ will be true approximately for the cat images

- **classification models**
    - one dimensional classification
    - decision trees
    - ensemble models
      - bagging
      - random forest
      - boost (Adaboost)
      - other methods (extra trees, isolated forests, oblique trees)
    - KNN ($k$-nearest neighbor) method
    - classification via regression
    - distribution estimation methods
    - feature finding methods

- **optimization** of a model: (context, model) $\mapsto$ model, resulting a better model of the context
    - definition:
      finding optimal parameter values for given sample data
    - objective: minimize $L=\text{loss}(\mathcal M(C,q),\mathcal C \mid \text{samples})$
      - we need $\partial L/\partial q=0$
      - practically batch evaluation
    - failure modes:
        - gradient calculation in complete database is numerically inefficitent
        - underfitting
        - overfitting
        - bad convergence (divergence, stuck to local minimun)
        - label noise sensitivity
        - dataset shift
        - shortcut learning
    - optimization methods:
        - linear regression
        - gradient descent
        - conjugate gradient descent
        - random algorithms
        - second-order optimization (Newton-Raphson method)
    - improvements in high dimensions: high dimensional optimization

- **steps of optimization**
  - data acquisition, database of samples
  - split into training, validation and test set
    - training set (60-80\% of data) to optimize the parameters
    - validation set (10-20%) to optimize hyperparameters
    - test set (10-20%) to evaluate the results
  - cross validation: use different sets for validation and test set
  - evaluate results

- **classification via regression**
    - define a function $p_i(x, q)$
        - Bayesian interpretation: $p_i(x)$ is the probability that the input $x$ belongs to class $i$
        - $q$ are parameters to optimize
    - can be defined from an unconstrained $f_i(x,q)$, using softmax normalization
    - loss function: $L(q) = \sum_{x\in\mathcal S} \ell(p_i(x), I(x\in c_i))$, where $I$ is the indicator function
      - smallest if $p_i(x)=1$ for the correct class
      - $\ell$ preferrably cross-entropy loss
    - prediction: class $(x)= \argmax_i p_i(x,q_{opt})\;\Rightarrow\;$ induced context
    - classifies every element of the base class
    - technical implementation:
      - preceptron
      - support vector machine
      - extreme learning machine
      - deep neural networks, DNN

- **distribution estimation methods**
    - tries to model the data distribution of the different classes of the sample data
    - uses one or more Gaussian per class
    - techniques:
        - Naive Bayes models
        - Gaussian Mixture Models
        - PCA (principal component analysis)

- **feature finding methods**
    - try to find features of the context, i.e. functions that are constant on the classes of the context
    - binary coding: $0$ for one class, $1$ for other
    - techniques:
        - LLT
        - autoencoders


- **softmax normalization** $(x_1,\dots x_n)\mapsto (p(x_1),\dots, p(x_n))$ where $p(x) = \dfrac{e^{x}}{\sum_j e^{x_j}}$
    - satisfies $p(x_i)\in [0,1]$
    - sum rule: $\sum_i p(x_i)=1$
    - $p(x_i)$ can be interpreted as probabilities

- **loss**: $L:(\mathcal C_1, \mathcal C_2 \mid S) \to \mathbb R$, measures the distance of the two contexts over a sample space
  - $L = \sum_{c\in\mathcal S} \ell(\Pi_{\mathcal C_1}(c), \Pi_{\mathcal C_2}(c))$, where $\ell$ is the loss function
  - $\ell\ge 0$
  - $\ell(y_1,y_2)=0$ iff $y_1=y_2$

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
- **gradient calculation**
  - lot of data: can not use all of them to determine gradient
  - use batches (few number of samples) to a guess
  - results in not uniform convergence 

---

- **underfitting**
    - **definition:**
      poor approximation already on $X_{\text{sample}}$,
      therefore also on $X \setminus X_{\text{sample}}$
    - **symptom:**
      high training error and high validation / test error
    - **intuition:**
      the model is too simple to capture the underlying structure
      of the data
    - **problem:**
      - too few parameters
      - overly restrictive model assumptions
      - insufficient training or premature stopping
    - **bias–variance viewpoint:**
      - high bias (systematic error)
      - low variance
    - **example:**
      - fitting a linear model to strongly nonlinear data
      - low-degree polynomial fit for complex patterns
      - shallow neural networks with very few hidden units
    - **detection:**
      - training and validation losses are both high
      - increasing model capacity improves both errors
    - **solution:**
      - **model-related**
        - increase model complexity
        - add nonlinear features or interactions
        - deepen or widen the network
      - **training-related**
        - train longer
        - improve optimization (learning rate, optimizer choice)
      - **feature-related**
        - better feature engineering
        - richer representations


---

- **overfitting**
    - **definition:**
      good approximation on $X_{\text{sample}}$ but poor generalization on  
      $X \setminus X_{\text{sample}}$
    - **symptom:**
      low training error, high validation / test error
    - **intuition:**
      the model adapts to accidental patterns (noise) in the finite sample
      instead of the underlying structure
    - **problem:**
      - too many parameters relative to the amount of data
      - learning sampling noise instead of signal
      - excessive model flexibility
    - **bias–variance viewpoint:**
      - low bias
      - high variance (small changes in data → large changes in the model)
    - **example:**
      - high-order polynomial fit oscillating between data points
      - deep neural networks with a large number of parameters trained on small datasets
      - decision trees grown to full depth
    - **detection:**
      - training loss decreases while validation loss increases
      - unstable predictions under resampling (e.g. cross-validation)
    - **solution:**
      - **regularization**
        - $L_2$ (ridge, weight decay)
        - $L_1$ (lasso, sparsity)
      - **data-related**
        - more training data
        - data augmentation
      - **model-related**
        - reduce model complexity
        - early stopping
        - pruning (decision trees)
      - **validation techniques**
        - cross-validation
        - hold-out test set


---

<a id="bad-convergence"></a>
- **bad convergence**
    - symptom: algorithm does not find global minimum
    - reason:
      - lot of local minima in almost flat directions
      - enhanced in high dimensions
    - results:
      - divergence
      - stuck in local minima
    - solutions:
      - regularization, better conditioning
      - momentum in minimum finding (e.g. ADAM)
      - coordinate descend, simulated annealing, reheating

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
