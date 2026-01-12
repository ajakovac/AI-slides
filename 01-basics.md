# Conceptual foundations

These concepts define the basic structure used throughout the documentation.


---

## States and time

It is difficult to determine where to start the whole descritpion. In human thinking th roots go deep into the unconscious.

We choose a somewhat physical basis, the states of the world, and the time evolution. But, as it will turn out later, the description is self-consistent, so the starting point is not so relevant.

<a id="states"></a>
- **states**: $\Omega$ $\hookleftarrow$ [set](mathematics_basics.md#mathematical-set)
    - contains all information to be able to predict the future
    - can be the complete world's state in a hyper (Cauchy) surface
    - a theoretical construct assuming that the future is deterministic if we fully fix a state.

<a id="time"></a>
- **time**: $T$ $\hookleftarrow$ number
    - arrow of time: goes ahaed
    - in real world parameters of the Cauchy surfaces where the states are set
    - in general the index of time moments when we register the state
    - observer dependent
    - additive

<a id="time-difference"></a>
- **time difference**: $dT$ $\hookleftarrow$ positive number
    - distance of two surfaces, where states are registered
    
<a id="time-evolution"></a>
- **time evolution**: $TE: \Omega\times dT \to \Omega$
    - Markov process
    - does not depend on the absolute time, only the time difference
    - consistency: $TE(\omega, dt) = TE(TE(\omega,dt/2),dt/2))$

***

## Classes in the world

The world can not be described in every detail. We consider certain details irrelevent when we try to describe and predict the world. For example the position of the Mars is not important when we define a book, therefore the 'book' concept must contain the Mars in all positions. Therefore a concept or object we are interested in, means in fact a very huge collection of states of the world.

<a id="class"></a>
- **class** : $C \subset \Omega$
    - interpretation:
        - collects states differing only in irrelevant details
        - corresponds to a concept (e.g. pen, red color, living being)
    - examples:
        - images where a given pixel is red
        - all living beings in the animal kingdom
    - we can speak about **subclasses**, **nested classes**, etc. just like in case of sets

---

## Context

A class in itself is the simplest element of the description of the world, defining a single concept. But we also want to speak about finer details, like for example dog breeds in the large class of dogs.

As the example of dog breeds show, in a detailed description we also speak about classes, that are disjunct subclasses of the underlying larger class. Also all elements of the underlying class belongs to some of the subclasses. 

We can divide a class in different ways into subclasses, and it then denotes a different set of concepts in the thinking. For example the world of books are divided into different subclasses by a book shop, a book collector, a reader, or a mover. An actual division of a class is called context.

<a id="context"></a>
- **context**: ${\cal C} = {\cal P}(C)$ $\hookleftarrow$ [partition](mathematics_basics.md#partition-of-a-set)
    - partition of the underlying class
    - elements are called **classes of the context**
    - interpretation:
        - only part of the world is relevant
        - states differing in irrelevant details are bundled
    - examples:
        - dog breeds in the class of dogs
        - a bookshop owner, a reader, a book collector and a mover uses different contexts of the class of books.

### Contexts instead of states

The states of the world is an abstraction, an assumption that the time evolution can be ultimately completely casual. However, all systems we get in connection are just contexts, whose elements are sets of states.
no ultimate description of the world! but any refinement is possible

From now on we will forget about the states of the world, and we speak exclusively about contexts. There is usually a fine context that serves as a basis of different subcontexts. For example to the set of images we can define a fine partition where two images are in different class if at least one pixel is different.

### Properties of the contexts

We can define a bunch of functions operating on the context.

- **underlying class**: $\mathcal C\mapsto C$

- **class of the context** : $(\mathcal C, c\subseteq \Omega) \mapsto$ true, if $c\in \mathcal C$

- **projector onto a context**: $\Pi: \mathcal C\mapsto \omega \mapsto c\in{\cal C}$ where $\omega\in c$ or $\Pi_\mathcal{C}(\omega)=\emptyset$

- **time evolution in a context**: $\mathcal C \mapsto n \mapsto \Pi_\mathcal{C}(\omega_n)$

- **disjunct contexts**: $(\mathcal C, \mathcal C')\mapsto $ true, if $\mathrm{UnderlyingClass}(\mathcal C)\cap \mathrm{UnderlyingClass}(\mathcal C')=\emptyset$

- **sum**: if $\mathrm{DisjunctContexts}(\mathcal C, \mathcal C')$: $(\mathcal C, \mathcal C')\mapsto \mathcal C\cup\mathcal C'$

- **subcontext**: $\hookleftarrow$ [context](#context): $\mathcal C'\preceq \mathcal C$ if $\forall c\in\mathcal C \exists c'\in C': c\subset c'$
    - notes: 
        - partial ordering
        - the subcontext means a coarser resolution of the world
    - examples:
        - animal kingdom in the complete biological taxonomy

We can also go to the other direction, and know a segment of the context in finer details (see the example of dogs and dog breeds). The concept of refining a context can be defined in several ways. We use that defintition that we refine only a single element of a context:

- **local refinement**:
  $(\mathcal C, \mathcal C') \mapsto \text{true}$
  iff
  $\exists c \in \mathcal C:\;
  \mathcal C'$ is a partition of $c$
    - notes: 
        - a refining of an element of a context
    - examples:
        - dogs and dog breeds
        - basic colors and shades of blue

- **global refinement**: $\mathcal C^+ = (\mathcal C\setminus \{c\}) \cup \mathcal C'$
    - note: $\mathcal C \preceq \preceq C^+$

- **common refinement** $\hookleftarrow$ [context](#context): $\mathcal C_1\vee \mathcal C_2 = \{ c_1 \cap c_2 \mid c_1 \in \mathcal C_1,\; c_2 \in \mathcal C_2,\; c_1 \cap c_2 \neq \emptyset \}$
    - notes:
        - all classes of the domain contexts are union of the elements of the common refinement context
        - several coarse contexts can lead to a fine description of the world.

## Characterization of contexts

### System 1

The most elementary way to characterize a context is to treat the context itself as the representation: each element (class) is considered directly and independently.

While this approach is formally complete, it quickly becomes infeasible in practice when the context is large. For example, a black-and-white image with one million pixels has  
\(2^{1{,}000{,}000}\) possible elements. In such a space, distinguishing one element from all others by direct enumeration is combinatorially prohibitive.

A slight variation of this idea is to single out an element by a function that evaluates above a fixed threshold (e.g. larger than $\tfrac12$) for that element and below it for all others. Such a function is effectively an indicator of a single point. In high-dimensional spaces, this indicator is almost everywhere constant and exhibits no exploitable regularity.

If one restricts attention to continuous, smooth, or otherwise low-complexity function classes, approximating such a sharply localized indicator becomes extremely difficult. The function must remain nearly constant on the overwhelming majority of the domain while changing abruptly at a single element. This makes the construction numerically unstable and structurally ill-suited for computation or learning.

So, while representing the class with its own elements is a viable strategy, it is useful only for low dimensional, eventually structured contexts.

The advantage of this approach is its simplicity: we do not need to assume other structures than the one is given by the task itself.

### System 2 — Global coordinates

A fine context can be characterized indirectly by a collection of coarse contexts whose common refinement reproduces it. This provides a structured alternative to direct, element-wise representation.

We define coordination in an algebraic way:

- **coordination**: $(\mathcal C_1,\dots,\mathcal C_n) \blacktriangleright \mathcal C$, iff $\mathcal C_1\vee \dots \vee \mathcal C_n = \mathcal C$
    - note:
  the contexts $\mathcal C_i$ are coarse views whose joint distinctions fully characterize $\mathcal C$
    - examples:  
        - coordination of a vector space: $\mathcal C = V$, the $\mathcal C_i = \{ c^{(i)}_s \mid s \in \mathbb R\}$ where $c^{(i)}_s = \{ x\in \mathbb{R}^d \mid e_i\cdot x = s\}$ are collections of hyperplanes with fixed orientation
        - pixelize images: $\mathcal C=$ images, $\mathcal C_i = \{$ images with $i$-th pixel fixed $\}$
        - token embeddings in LLMs:
          $\mathcal C =$ partition of embedding space by semantic equivalence, $\mathcal C_i =$ partitions induced by coordinate projections (or low-dimensional feature functions), with similarity measured by cosine distance

### System 2 — Local coordinates

There is another way to characterize a context that goes beyond global coordination.  
Instead of decomposing a fine context directly into several coarse ones, we start with a simple coarsening of the context and then apply **local refinements** to the individual elements of this coarse context. Repeating this process yields a hierarchical structure, called a **refinement tree**, whose leaves are exactly the classes of the fine context.

A refinement tree thus represents a context by **successive, conditional partitions**.

The key conceptual shift is that coordinates are no longer global. Different regions of the context may admit different refinements, and the most appropriate local distinctions can be used where they make sense. For example, the concept of *display size* is meaningful for displays but not for vegetables, while *fat content* is meaningful for foods but not for electronic devices.

- **refinement tree**:
  a mapping
  $\mathcal C \mapsto \mathcal T$,
  where $\mathcal T$ is a rooted tree whose nodes are labeled by subsets of $\mathcal C$,
  satisfying the following conditions:
    - conditions
        - the root is labeled by the full context $\mathcal C$
        - for each internal node labeled by $C' \subseteq \mathcal C$, its children form a context (partition) of $C'$
        - the leaves (nodes with no children) are singleton sets $\{c\}$ with $c \in \mathcal C$

    - notes:
        - every refinement tree induces a unique fine context (its leaves)
        - different refinement trees may induce the same context
        - generic coordination is a special case, where all local refinements are identical at every node
        - System 1 corresponds to a refinement tree of depth 1
        - local coordinates correspond to paths from the root to a leaf

    - examples:
        - using *display size* to refine the class of displays and *fat content* to refine the class of foods, even though these refinements are not meaningful outside their respective domains

A refinement tree also defines a **prefix code** for each element of the context: each path from the root to a leaf uniquely identifies an element by a sequence of refinement choices. If the relevance (or probability of occurrence) of the elements is known, one can construct an optimal refinement tree that minimizes the expected path length, in direct analogy with **Huffman coding**.

## Features

So far we have spoken about contexts in an abstract, algebraic way. When we want to treat them in a calculation, we have evaluate them in some way, i.e. we have to assign a value to its classes.

In fact there is a one-to-one correspondence between a function and the subclasses. First, a function defined on a context is called feature:

- **feature**: $\mathcal C \to B$
    - function defined on the elements of  a context
    - range can be a finite set or real numbers
    - the result is called a fact, or data
    - alternative name: **measurement**, **observation**
    - domain the complete context
    - $F$ is measurable wrt. $(\Omega,\sigma({\cal C)})$
    - $F$ is a random variable in the context
    - examples:
        - measuring temperature with a thermometer
        - recording the color of a pixel with a camera

A feature defines a subcontext:

- **induced context**:
      $f\mapsto \mathcal \{ f^{-1}(\{y\}) \mid y \in \operatorname{Ran}(f) \}$

The features of a context are also features of a finer context:

- **extension** (of a feature):  $(\mathcal C \to B) \to (\mathcal C'\to B)$ if $\mathcal C \preceq \mathcal C'$, $f(c')= f(c)$ for $c'\in c$
    - constant over several classes of the finer context

This does not work the other way around. Some of the features of a given context are contexts of another one, some are not.

- **relevant** (feature): $(\mathcal C, f) \mapsto f\in \mathcal F_\mathcal C =$ true iff $f$ has a domain compatible with $\mathcal C$
    - alternative name: selective feature

- **irrelevant** (feature): not relevant
    - alternative name: descriptive function

### Functional approach to define contexts

- **ID**: $\mathcal C \mapsto$ unique string
    - all elements of all contexts should be named
    - all functions should be named
    - e.g. timestamp of its creation, or a sensible name
    - examples:
        - "apple", "alligator"
        - "ID36692855235"

- **triplet assignment**: $(n, f, v = f(n))$
    - corresponds to the name:property:value triplet
        - $n=$ name ID
        - $f=$ functions ID, the property as a function
        - $v$ is the value, the range of the function on $n$
        - in case of multiple values, it is equivalent to multiple triplets $(n,f,v_1), (n,f,v_2),\dots$
    - additional actions:
        - induces defining the partition generated by the function
        - induces circular definitions: $(v,n,f)$ and $(f,v,n)$
    - examples:
        - ("apple", "color", ["red", "green", "yellow"])
        - generates subclasses: "red color apple", "green color apple", etc.
        - induces definitions: ("red", "apple", "color"), ("color", "red", "apple")
