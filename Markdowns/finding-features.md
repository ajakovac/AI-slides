# Feature finding

- **feature finding problem**
    - sample data are given as $S=\{(x_a,y_a)\}$
    - sample context $\mathcal C_{sample}= \{ c_1, c_2,\dots\}$, where $c_i$ are subsets of data belonging to the same class
    - task: find relevant features of the context, i.e. a function constant on sample classes
    - formally: find $f:x\mapsto y$ that $f(x)=f(x')$ if $x,x'\in c \in\mathcal C_{sample}$

- **relevance measure**
    - function $f:x\to y$ not fully consistent with a context
    - how useful is this function for classification? $\to$ "overlap" or relevance measures
        - feature importance (decision tree, random forest)
        - permutation importance, feature masking
        - relevance based on mutual information
        - neural networks Gradient-weighted Class Activation Mapping (Grad-CAM)

- **permutation importance**
    - model dependent
    - measures sensitivity for permuting values of a feature
    - method:
        - assume a model uses a feature for classification, assign a score $\text{Score}_{model}$
        - permute the feature values in the data
        - retrain the model, and determine the score $\text{Score}_{permuted}(f)$
        - importance: $$\text{Importance}(f)=\text{Score}_{model} - \text{Score}_{permuted}(f)$$

- **feature masking**
    - model dependent
    - measures sensitivity for setting arbitrary value for a feature
        - constant
        - random
    - method is the same as in permutation importance

- **relevance based on mutual information**
    - model independent
    - use mutual information between the feature values and the actual class from the context sample
    - technically:
        - calculate joint probability $$p(f, c) = \frac1{N_{sample}} \sum_{x\in \text{data}} \mathbb I(f(x)=f, c(x)=c)$$
        - mutual information $$I(f,\mathcal C_{sample}) = \sum_{f, c} p(f,c) \ln\dfrac{p(f)p(c)}{p(f,c)}$$

- **LLT**, **Linear Law Transformation**
    - goal: find a function that is constant in classes of a context
    - practically for small number of classes: multiple features, each is constant in one class
    - idea:
        - find linear laws for subsets of the classes: find $w$ unit vectors that satisfy $$w\cdot x=0\; \forall x\in b\subset c\in\mathcal C$$
        - cover all subsets with linear laws $\Rightarrow c\mapsto W_c=\{w_{c1}, w_{c2},\dots\}$, i.e.
        $$\forall x\in c\;\exists w\in W_c:\; w\cdot x=0$$
        - for a new element $x$ check which class'es laws are applicable
    - practical points:
        - collect a lot of laws, so for each class element a bunch of laws is true
        - check the number of applicable laws
        - choose the class, where the most laws are applicable
        - ideal case is when in the correct class one law is applicable, in other classes there is no appropriate law.

- **find linear law**
    - problem: for a set $c$ find $w$ unit vector satisfying $w\cdot x=0$ for all $x\in c$
    - in reality exactly zero can not be achieved; instead $w\cdot x=\xi_x$, and $\sum_{x\in c}\xi^2$ is minimal
    - in matrix notation $X_{ni}=(x_n)_i$ with LAgrange multiplicator $$ \sum_x \xi_x^2-\lambda w^Tw = w^T X^T X w -\lambda w^T w=\text{minimal}$$
    - solution $X^T X w =\lambda w$
    - write back: $$ \mathbb E[\xi] = \frac 1{|c|}\sum_{x\in c} \xi^2_x = \frac{\lambda}{|c|}$$
    - for smallest noise we need smallest eigenvalues

