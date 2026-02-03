# Deep Neural Networks (DNNs)

- **deep neural network**, **DNN**
    - idea: classification via regression
    - data model: $\mathcal M :(C,W)\to B$ is a composite function $\mathcal M = f^{(L)}\circ\dots f^{(L-1)} \circ f^{(0)},$ 
    where $$f^{(a)}: \mathbb R^{d_a} \to \mathbb R^{d_{a+1}},\qquad f^{(a)}_i(x) = \sigma_a\left(\sum_{j=1}^{d_a} M^{(a)}_{ij} x_j +b^{(a)}_i\right)$$
    - layered architecture, $L$ is the number of hidden layers
    - parameters (weights): $W=(M,b)$ of the linear map
    - $\sigma_a$ are sigmoid (nonlinear) functions $\to$ activation functions
        - may depend on the layer
        - in the last layer softmax normalization
        - usual types: tanh, ReLU
    - examples:
        - image classification: $a=0$ layer is the image in pixel representation, $a=L+1$ layer is the layer of classes
        - bird song recognition: $a=0$ layer is the wav file, $a=L+1$ layer is the bird species
    - universal approximation theorem: any function can be realized in this way
    - implements a System I approach, with all of its advantages and disadvantages
    - training
        - usually high dimensional optimization
        - needs gradient, now of composite functions $\to$ backpropagation
    - problems with deep networks:
        - high dimensional optimization problems
        - vanishing and exploding gradient
        - overfitting
        - symmetries of the data
        - expensive training $\to$ pretrained models (transfer learning)
        - catastrophic forgetting

- **layer types**
    - in Pytorch: [layer types](https://docs.pytorch.org/docs/stable/nn.html)
    - fully connected (dense)
        - every neuron connects to all neurons of the previous layer
        - affine map + nonlinearity: $z=W x + b$, $x\mapsto \sigma(z)$
        - good for mixing global features, but large number of parameters
    - convolution
        - local receptive fields with shared weights (kernels/filters)
        - feature map: $(f\ast x)_i = \sum_j K_{i-j} x_j$ (discrete convolution)
        - translation equivariance, fewer parameters than dense layers
    - softmax
        - last layer for multi-class classification
        - maps logits to probabilities: $p_k = \dfrac{e^{z_k}}{\sum_j e^{z_j}}$
        - enables cross-entropy loss with probabilistic interpretation
    - dropout
        - during training randomly set activations to zero
        - prevents co-adaptation, reduces overfitting
        - at test time use the full network with scaled activations
    - batch normalization
        - normalize activations within a mini-batch: $\hat z=(z-\mu)/\sqrt{\sigma^2+\epsilon}$
        - learnable scale/shift: $y=\gamma \hat z+\beta$
        - stabilizes and speeds up training
    - gradient clipping
        - limit the gradient norm: $g\leftarrow g\cdot \min\left(1,\frac{\tau}{\|g\|}\right)$
        - prevents exploding gradients (useful in deep or recurrent nets)
    - pooling
        - down-sampling of feature maps, e.g. max/average pooling
        - reduces spatial size, adds local invariance
    - recurrent layers (RNN, LSTM, GRU)
        - process sequences by reusing the same weights over time steps
        - hidden state carries memory: $h_t = f(x_t, h_{t-1})$
        - good for time series, text, and signals
    - attention
        - compute weighted mixtures of inputs based on similarity
        - scores: $\alpha_{ij} \propto \exp(q_i\cdot k_j)$, output $y_i=\sum_j \alpha_{ij} v_j$
        - enables long-range dependencies without recurrence
    - residual (skip) connections
        - add identity shortcuts: $x \mapsto x + F(x)$
        - improves gradient flow, allows very deep networks
    - embedding
        - map discrete tokens to vectors: $x \in \{1,\dots,V\} \mapsto e_x \in \mathbb R^d$
        - used for words, categories, and IDs
    - transposed convolution
        - learnable up-sampling ("deconvolution")
        - used in decoders, generative models, and segmentation
    - normalization layers
        - layer norm, instance norm, group norm
        - stabilize training when batch statistics are unreliable
    - flatten / reshape
        - change tensor shape without changing data
        - bridge between convolutional and dense layers


- **backpropagation**
    - we want to have derivatives of the loss function with respect to the weights $$\dfrac{\partial \ell}{\partial W^{(a)}_{ij}}\quad \text{and}\quad \dfrac{\partial \ell}{\partial b^{(a)}_{i}}$$ 
    - loss function: $\ell(x) = \ell(\mathcal M(x;W,b))$ where $\mathcal M$ is a composite function
    - introduce intermediate results $x^{(0)}$ (input) $\to x^{(1)}\to \dots \to x^{(L)}\to x_{out}$ (output), here $x^{(a)}_j = f^{(a)}_j(x^{(a-1)})$
    - use chain rule $$\dfrac{\partial \ell}{\partial x^{(a-1)}_i} = \dfrac{\partial \ell}{\partial x^{(a)}_j}\dfrac{\partial x^{(a)}_j}{\partial x^{(a-1)}_i} = \dfrac{\partial \ell}{\partial x^{(a)}_j} \partial_i f^{(a)}_j(x^{(a-1)}) = \dfrac{\partial \ell}{\partial x^{(a)}_j} \partial_i f^{(a)}_j(f_a^{-1}(x^{(a)}))$$
    - implies a recursion: with notations $\ell^{(a)}_i = \dfrac{\partial \ell}{\partial x^{(a)}_i}$ and $U^{(a)}_{ij} = \partial_i f^{(a)}_j\circ f_a^{-1}$ we find in matrix notation $$\ell^{(a-1)}= U^{(a)} \ell^{(a)}.$$
    - known value: $$\ell^{(L+1)}_i = \dfrac{\partial\ell}{\partial x_{out,i}}$$
    - specifically if $x^{(a)}_j =f^{(a)}_j(x^{(a-1)}) = \sigma_a(\sum_i M^{(a)}_{ji} x^{(a-1)}_i + b^{(a)}_j)$ then $$ U^{(a)}_{ij} = M^{(a)}_{ji} u_a(x^{(a)}_j),\quad \text{where}\quad u_a = \sigma'_a\circ \sigma_a^{-1}$$
    - derivatives with respect to weights 
    $$\begin{align*}
    \dfrac{\partial \ell}{\partial M^{(a)}_{ij}} &= \dfrac{\partial \ell}{\partial x^{(a)}_i} \dfrac{\partial x^{(a)}_i}{\partial M^{(a)}_{ij}} = \ell^{(a)}_i u_a(x^{(a)}_i) x^{(a-1)}_j\\
    \dfrac{\partial \ell}{\partial b^{(a)}_i} &= \dfrac{\partial \ell}{\partial x^{(a)}_i} \dfrac{\partial x^{(a)}_i}{\partial b^{(a)}_i} = \ell^{(a)}_i u_a(x^{(a)}_i)\\
    \end{align*}
    $$
    - recursion (backpropagation):
        - forward cycle: from $x^{(0)}$ compute all $x^{(a)}$ layer values
        - backward cycle: compute $\ell^{(L+1)}$ and use recursion to evaluate all $\ell^{(a)}$
        - use the above formulae to compute the derivatives with respect to the weights

- **vanishing gradient**
    - symptom: gradients shrink exponentially with depth toward the input layer
    - formal cause:
        - backpropagation gradients $||U||<1$ (spectral norm is smaller than one)
        - in recursion gredient is multiplied at most by $U\;\Rightarrow \lambda_{max}<\gamma$
        - after $L$ recursion step gradient $\sim \gamma^L$
    - technical causes
        - sigmoid or tanh activations (saturation)
        - poor weight initialization
    - consequences:
        - early layers learn extremely slowly
        - network behaves as if it were shallow
        - long-range dependencies cannot be learned
    - mitigation techniques:
        - weight initialization
        - use better activation functions (ReLU and similar) to avoid saturation and to control gradient magnitude
        - use normalization techniques
        - use residual connections

- **exploding gradient**
    - symptom: gradients grows exponentially with depth toward the input layer
    - formal cause:
        - backpropagation gradients $||U||>1$ (spectral norm is smaller than one)
        - in recursion gredient is multiplied eventually by $U\;\Rightarrow \lambda_{max} > \gamma>1$
        - after $L$ recursion step gradient $\sim \gamma^L$
    - technical causes
        - large initial weights
        - unstable recurrent connections
        - unnormalized activations
    - consequences:
        - numerical overflow
        - unstable training,
        - wildly oscillating parameter updates
    - mitigation techniques:
        - weight initialization
        - use better activation functions (ReLU and similar) to avoid saturation and to control gradient magnitude
        - use normalization techniques
        - use residual connections
        - use gradient clipping


- **activation functions**
    - sigmoid functions breaking linearity
    - usual types:
        - sigmoid $\sigma(x)=\dfrac{1}{1+e^{-x}}$
            - outputs in $(0,1)$, saturates for large $|x|$
        - leaky ReLU $f(x)=\max(\alpha x, x)$
            - avoids "dead" neurons by allowing small negative slope
        - ELU $f(x)=x$ if $x>0$, else $\alpha(e^{x}-1)$
            - smooth negative part, mean activations closer to zero
        - GELU $f(x)=x\,\Phi(x)$ (Gaussian CDF)
            - smooth, used in Transformers
        - softplus $f(x)=\ln(1+e^{x})$
            - smooth ReLU, strictly positive

- **weight initialization**
    - goal: keep variance of activations and gradients approximately constant.
    - common schemes:
        - Xavier / Glorot initialization (tanh, sigmoid)
        - He initialization (ReLU-family)
    - effect:
    - balances forward and backward signal propagation.


- **normalization techniques**
    - batch normalization, layer normalization, and related methods.
    - effects:
        - stabilize activation distributions,
        - reduce internal covariate shift,
        - smooth the optimization landscape.
    - interpretation:
        - dynamically rescales representations to keep gradients well-conditioned
---

- **residual connections**
    - skip connections to carry information to lower layers
    - introduced in ResNets
    - benefits:
        - identity path guarantees gradient flow
        - prevents exponential decay or growth


- **gradient clipping**
    - used especially in recurrent neural networks:
    - allow maximal value for gradient $\|\nabla\| \leftarrow \min(\|\nabla\|, \tau)$
    - benefits:
        - prevents exploding gradients
        - stabilizes training

- **symmetries of the data**
    - **observation:**
      deep neural networks can represent symmetries,
      but they typically learn them slowly and inefficiently from data alone
    - **reason:**
      - symmetries correspond to exact constraints
      - gradient-based learning discovers them only approximately
      - learning the same pattern repeatedly at different locations / orientations
        wastes model capacity and data
    - **examples:**
        - translation symmetry (images, signals)
        - rotation symmetry (objects, physical systems)
        - reflection symmetry
        - scaling invariance
        - permutation invariance (sets, point clouds)
    - **consequence:**
      - increased sample complexity
      - slower convergence
      - higher risk of overfitting
    - **solution:**
      - encode symmetries directly into the model architecture
      - use representations that respect symmetry constraints
    - **architectural examples:**
      - convolutional layers $\to$ translation equivariance
      - pooling $\to$ approximate invariance
      - weight sharing $\to$ reduced degrees of freedom
      - equivariant networks (group convolutions)
      - permutation-invariant architectures for sets
    - **benefits:**
      - fewer effective parameters
      - faster learning
      - better generalization
      - improved robustness

- **pretrained models (transfer learning)**
    - **motivation:**
      training deep neural networks from scratch is computationally expensive
      and requires large labeled datasets
    - **idea:**
      reuse a model (or part of a model) trained on a large, generic dataset
      and adapt it to a new, related task
    - **assumption:**
      lower-level representations (features) are transferable across tasks
    - **typical workflow:**
      - load a pretrained model
      - reuse the feature extractor
      - fine-tune the last layers (or the full network)
    - **examples:**
      - image models pretrained on ImageNet
      - language models pretrained on large text corpora
      - audio models pretrained on speech datasets
    - **benefits:**
      - significantly reduced training time
      - lower computational cost
      - improved performance with limited data
      - faster convergence
    - **limitations:**
      - mismatch between source and target domain (negative transfer)
      - limited flexibility imposed by pretrained representations
    - **use cases:**
      - small or medium-sized datasets
      - rapid prototyping
      - resource-constrained environments

- **catastrophic forgetting**
    - **definition:**
      during sequential training on multiple tasks,
      a neural network rapidly loses performance on previously learned tasks
      when trained on new ones
    - **cause:**
      - shared parameters are overwritten by optimization for the new task
      - lack of explicit mechanisms to preserve earlier knowledge
    - **typical setting:**
      - continual / lifelong learning
      - non-stationary data distributions
      - task-by-task or stream-based training
    - **symptom:**
      - strong performance on the current task
      - near-random performance on earlier tasks
    - **intuition:**
      gradient updates for the new task interfere destructively
      with representations learned for previous tasks
    - **example:**
      - a classifier trained on task A, then on task B,
        forgetting task A almost completely
    - **consequence:**
      - inability to accumulate knowledge over time
      - poor long-term learning
    - **solution:**
      - **regularization-based**
        - penalize changes to important parameters (e.g. elastic weight consolidation)
      - **rehearsal-based**
        - replay old data or synthetic samples
      - **architectural**
        - task-specific subnetworks
        - expandable models
      - **representation-based**
        - learn task-invariant features

- **error-prone behavior and adversarial attacks**
    - **observation:**
      deep neural networks can be highly sensitive to small,
      carefully chosen perturbations of the input
    - **definition (adversarial example):**
      an input modified by an imperceptible perturbation
      that causes a confident but incorrect prediction
    - **cause:**
      - high-dimensional input spaces
      - locally linear behavior of DNNs
      - decision boundaries close to the data manifold
    - **intuition:**
      small input changes can accumulate along many dimensions
      and push the input across a decision boundary
    - **examples:**
      - image perturbations invisible to humans but misclassified by CNNs
      - adversarial noise in audio causing wrong transcription
      - small text changes leading to incorrect NLP outputs
    - **types of attacks:**
      - white-box attacks (full model access)
      - black-box attacks (query-based or transfer attacks)
      - targeted vs. untargeted attacks
    - **consequence:**
      - lack of robustness
      - safety and security risks
      - reduced trust in deployed systems
    - **solution:**
      - **adversarial training**
        - include adversarial examples during training
      - **regularization and smoothing**
        - gradient penalties
        - label smoothing
      - **input-level defenses**
        - noise injection
        - preprocessing / filtering
      - **model-level defenses**
        - robust architectures
        - certified robustness methods
