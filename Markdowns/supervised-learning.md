
- **AI learning paradigms**
    > different ways AI systems learn from data and experience
    - **goal of AI**: provide sensible context for an underlying set
    - **approaches**
        - __supervised learning__
        - __data driven approach__
        - __reinforcement learning__
        - __time series analysis__

- **supervised learning**
    > find the context $\mathcal C$ that smoothly represents the provided sample data.
    - **strategy**
        - collect __sample data__, implying __sample context__ $\to$ see __publicly available databases for classification__
        - assume __data model__
        - perform __model optimization__
        - __evaluation of results of a classification__
    - **unsupervised is not really meaningful**
      - mathematically any partition is possible
      - depends on the "distance" $\to$ data representation
      - easy to manipulate (c.f. university ranking, economic data)
      - needs a clean definition of the context (e.g. temporal-spatial closeness)
      - examples: university ranking, economic or individual performance evaluation, IQ tests
      - see also __Human Intelligence: A Psychological Perspective__
    - **examples**
        - __pattern recognition__
        - __data compression__

- **publicly available databases for classification**
    > databases can be used as benchmarks or for learning
    - **links**
        - https://davenport.libguides.com/data/public-data
        - https://github.com/awesomedata/awesome-public-datasets?tab=readme-ov-file
        - https://docs.pytorch.org/vision/main/datasets.html

- **sample data**:
    > for training, we need data - label (meaning) pairs
    - **definition**: $\{(x_a,y_a) \mid x_a\in C, y\in \mathcal C: x_a\in y_a, a=1\dots N_{data}\}$, where $C=\text{underlying class}(\mathcal C)$
    - **assumption**
        - independent measurements
    - **failure modes**
        - __corrupted label__
        - __not enough information__
    - **examples**
        - (cat-imege-1,cat), (cat-imege-2,cat), (dog-imege-1,dog), $\dots$ (cat-imege-N,cat), 
        - what is the word the speaker says?

- **sample context**
  > data belonging to the same class
  - formally $\mathcal C_{sample} =\{ \{x_a \mid c_a=c\} \mid c \in\mathcal C\}$

- **data model**
  > parametric map over a set
  - **definition**: $\mathcal M :(C,Q)\to B$, where $Q$ are the parameters, $B$ is the target (label) set
  - **names**
    - if $B$ is a finite set: **classification models**
    - if $B$ is continuous: **regression**
  - **representation**: corresponds to the __direct representation__ of the context
  - **modelling a context**
    - use the __induced context__ $\mathcal M^{-1}(B,q)$
    - example $\mathcal M(\text{image}, q_{opt}) = \text{cat}$ will be true approximately for the cat images

- **classification models**
  - **elementary methods**
      - __one dimensional classification__
      - __decision tree__
      - __KNN__ ($k$-nearest neighbor) method
  - **ensemble models**
      - __bagging__
      - __random forest__
      - __boost__ (Adaboost)
      - other methods (extra trees, isolated forests, oblique trees)
  - **classification via regression**
      - __classification via regression__
  - **distribution estimation methods**
      - __distribution estimation methods__
  - **feature finding methods**
      - __feature finding methods__

- **model optimization** 
    > find the optimal parameters that gives best results on a sample
    - **objective**
      - define a __sample loss__ $L=\text{loss}(\mathcal M(C,q),\mathcal C \mid \text{samples})$
      - minimize $L$
      - we need $\partial L/\partial q=0$
      - practically batch evaluation
      - optimization $\to$ __optimization methods__
    - **failure modes**
        - __gradient calculation in complete database__  is numerically inefficitent
        - __underfitting__
        - __overfitting__
        - __bad convergence__ (divergence, stuck to local minimun)
        - __label noise sensitivity__
        - __dataset shift__
        - __shortcut learning__

- **optimization methods**
    - **algorithms**
        - __linear regression__
        - __gradient descent__
        - __conjugate gradient descent__
        - __random algorithms__
        - second-order optimization (__Newton-Raphson method__)
    - **improvements in high dimensions**: __high dimensional optimization__

    - **steps of optimization**
      - data acquisition, database of samples
      - split into training, validation and test set
      - training set (60-80\% of data) to optimize the parameters
      - validation set (10-20%) to optimize hyperparameters
      - test set (10-20%) to evaluate the results
      - cross validation: use different sets for validation and test set
      - __evaluation of results of a classification__

- **classification via regression**
    > classes are defined by inequalities posed on a continuous function
    - **parametric function**
        - define a function $p_i(x, q)$
        - Bayesian interpretation: $p_i(x)$ is the probability that the input $x$ belongs to class $i$
        - $q$ are parameters to optimize
        - can be defined from an unconstrained $f_i(x,q)$, using __softmax normalization__
    - **optimization condition**
      - **loss function**: $L(q) = \sum_{x\in\mathcal S} \ell(p_i(x), I(x\in c_i))$, where $I$ is the indicator function
      - smallest if $p_i(x)=1$ for the correct class
      - $\ell$ preferrably cross-entropy loss
    - **prediction**
      - predicted class $(x)= \mathop{argmax}_i p_i(x,q_{opt})\;\Rightarrow\;$ induced context
      - classifies every element of the base class
    - **technical implementation**
      - __perceptron__
      - __support vector machine__
      - __extreme learning machine__
      - __DNNs__ (deep neural networks)

- **distribution estimation methods**
    > tries to model the data distribution of the sample data
    - uses one or more Gaussian per class
    - **techniques**
        - __Naive Bayes models__
        - __Gaussian Mixture Model__
        - __PCA__ (principal component analysis)

- **feature finding methods**
    > try to find features of the context, i.e. functions that are constant on the classes of the context
    - **binary coding**: $0$ for certain classes, $1$ for other
    - **techniques**
        - __LLT__
        - __autoencoders__

- **softmax normalization** 
    > normalizes output to be interpretable as probability distribution
    - **definition**: $(x_1,\dots x_n)\mapsto (p(x_1),\dots, p(x_n))$ where $$p(x) = \dfrac{e^{x}}{\sum_j e^{x_j}}$$
    - **properties**
      -satisfies $p(x_i)\in [0,1]$
      - sum rule: $\sum_i p(x_i)=1$
      - $p(x_i)$ can be interpreted as probabilities

- **sample loss**
  > measures the distance of the two contexts over a sample space
  - $L:(\mathcal C_1, \mathcal C_2 \mid S) \to \mathbb R$
  - with __loss function__ $\ell$: $L = \sum_{c\in\mathcal S} \ell(\Pi_{\mathcal C_1}(c), \Pi_{\mathcal C_2}(c))$


- **loss function**: 
  > distance of two context elements
  - **definition**
    - $\mathcal C \times \mathcal C\to \mathbb R^+_0$
    - using a numerical representation for the classes $\mathbb R^N\times\mathbb R^N\to\mathbb R^+_0$
  - **properties**
    - $\ell\ge 0$
    - $\ell(y_1,y_2)=0$ iff $y_1=y_2$
  - **link**: [Pytorch loss functions](https://docs.pytorch.org/docs/stable/nn.html#loss-functions)
  - **examples**
    - __Gaussian loss__
    - __MSE loss__
    - __p-norm loss__
    - __Kullback–Leibler loss__
    - __cross entropy loss__

- **Gaussian loss**
    - **covariance matrix**: $C_x$
    - **chi-squared function**: $$\chi^2(y,y') = (y-y')^T C_x^{-1} (y-y')$$
    - **loss function**: $\ell = \chi^2$

- **MSE loss**
    - **definition**: mean squared error loss
    - **loss function**: $\ell(y,y') = |y-y'|^2$

- **p-norm loss**
    - **definition**: loss based on $L_p$ distance
    - **power parameter**: $p \in \mathbb{R}$
    - **loss function**: $\ell(y,y') = (|y-y'|^p)^{1/p}$

- **Kullback–Leibler loss**
    - conditions:
        - $p,q$ are probability distributions
        - $\sum_i p_i = 1,\; p_i \in [0,1]$
        - $\sum_i q_i = 1,\; q_i \in [0,1]$
    - **loss function**: $\ell(p,q) = \sum_i p_i \log(p_i/q_i)$

- **cross entropy loss**
    - conditions:
        - $p_i \in \{0,1\}$
        - $q$ is a probability distribution
        - $\sum_i q_i = 1,\; q_i \in [0,1]$
    - **loss function**: $\ell(p,q) = -\sum_i p_i \log(q_i)$



- **not enough information**
    - **definition**: a given input leads to different labels
    - **formulation**: labels are not measurable with respect to the input context
    - **cause**: input contains insufficient information
    - **consequence**: probabilistic methods are required

- **corrupted label**
    - **definition**: label does not correspond to the class of the input
    - **causes**
        - human mistake
        - systematic error


- **gradient calculation in complete database**
  > numerically inefficient to collect all contributions of a dataset to the gradient
  - **solution**
    - use batches (few number of samples) to a guess
    - results in not uniform convergence 

- **underfitting**
    > the model is too simple to capture the underlying structure of the data
    - **definition**: poor approximation already on $X_{\text{sample}}$,
      therefore also on $X \setminus X_{\text{sample}}$
    - **symptom**: high training error and high validation / test error
    - **problem:**
      - too few parameters
      - overly restrictive model assumptions
      - insufficient training or premature stopping
    - **bias–variance viewpoint**
      - high bias (systematic error)
      - low variance
    - **example**
      - fitting a linear model to strongly nonlinear data
      - low-degree polynomial fit for complex patterns
      - shallow neural networks with very few hidden units
    - **detection**
      - training and validation losses are both high
      - increasing model capacity improves both errors
    - **solution**: __solutions for underfitting__

- **solutions for underfitting**
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

- **overfitting**
    > the model adapts to accidental patterns (noise) in the finite sample instead of the underlying structure
    - **definition**: good approximation on $X_{\text{sample}}$ but poor generalization on  
      $X \setminus X_{\text{sample}}$
    - **symptom**: low training error, high validation / test error
    - **problem**
      - too many parameters relative to the amount of data
      - learning sampling noise instead of signal
      - excessive model flexibility
    - **bias–variance viewpoint**
      - low bias
      - high variance (small changes in data → large changes in the model)
    - **example**
      - high-order polynomial fit oscillating between data points
      - __DNNs__ with a large number of parameters trained on small datasets
      - decision trees grown to full depth
    - **detection**
      - training loss decreases while validation loss increases
      - unstable predictions under resampling (e.g. cross-validation)
    - **solution**: __solution for overfitting__

- **solution for overfitting**
    - **regularization**
        - $L_2$ (ridge, weight decay)
        - $L_1$ (lasso, sparsity)
    - **data-related**
        - more training data
        - data augmentation
    - **model-related**
        - reduce model complexity
        - early stopping
        - pruning (__decision tree__)
    - **validation techniques**
        - cross-validation
        - hold-out test set

- **bad convergence**
    > algorithm does not find global minimum
    - **reason**
      - lot of local minima in almost flat directions
      - enhanced in high dimensions
    - **results**
      - divergence
      - stuck in local minima
    - **solutions**
      - regularization, better conditioning
      - momentum in minimum finding (e.g. ADAM)
      - coordinate descend, simulated annealing, reheating

- **dataset shift**
    > the training data are not representative of the data encountered in practice
    - **definition**: $P_{\text{sample}}(X) \neq P(X)$
    - **solution**: domain adaptation

- **label noise sensitivity**
    > small label noise causes large performance degradation
    - **mitigations**
        - data cleaning
        - robust losses
        - regularization
        - reweighting
        - noise-aware models

- **shortcut learning**
    > model learns spurious correlations instead of causal structure
    - **causes**
        - dataset bias
        - label leakage
        - insufficient context variability
    - **mitigations**
        - targeted augmentation
        - controlled data collection
        - adversarial training
    - **examples**
        - background-based image classification
        - channel-noise-based speech recognition

- **pattern recognition**
    > finding meaningful classes from raw data
    - **basic context**
        - pixels
        - audio samples
        - raw sensor data
        - $X \sim \mathbb{R}^N$
    - **target context**
        - object classes
        - $Y = \{c_1, \dots, c_K\}$
    - **examples**
        - image classification
        - speech recognition


- **data compression**
    > represent data with fewer bits by removing irrelevant features
    - **basic context**
        - pixels
        - audio samples
        - raw sensor data
        - $X \sim \mathbb{R}^N$
    - **target context**
        - compressed representation
        - $Y \sim \mathbb{R}^M,\; M < N$
    - **examples**
        - image compression
        - audio compression
