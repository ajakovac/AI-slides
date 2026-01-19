# Foundations

## Concepts and contexts

It is difficult to determine where to start the whole descritpion. In human thinking the roots go deep into the unconscious.

We want to give a description from the point of view of an actor, an intelligent being, that can be a living being, in particular a human, or an AI. The Universe, the ultimate reality we are living in, is observed by this actor. But the largest part of the Universe is not relevant for the description: partly because it can not observe it, it has not the computational capacity to count with all of the details, and finally, but most importantly, most details are irrelevent for the actor to fulfill its purpose. This purpose is usually the mainanance of itself in the living world, but it can be other, artificial goals in case of an AI.

This argumentation shows, the relevant concepts of the actor are not the individual states in the Universe, but a collection of lot of states. E.g. pen is a collection of states where I hold a pen in my hand. However the simple collection of states is not sufficient to represent the intimate relation of the concepts, that is induced by the time evolution of the Universe.

A more adeuqate description is that if we treat the concepts as things that are good for something. In more refined wording, concepts are purpose-laden, action-oriented, agent-relative abstractions whose meaning is grounded in use, risk, and affordance. This approch has a lot of support in philosphy and psychology (Pragmatism (philosophy), Instrumentalism, Affordance-based perception, Embodied / enactive cognition, Teleosemantics (evolutionary framing)). The logic is that we consider “Steep” = “requires braking, caution, balance”, “Sharp” = “can cut me”, “Edible” = “can nourish me”.

Adapting this approach for technical use, a concept is something that act on other concepts, and as a result is can lead to one or eventually several other concepts. This is the network of associations. The definition reads as:

- **concepts**: a set $\Omega$ with a product operation: $\omega\cdot\omega' = \{\omega_1, \omega_2,\dots\}.$
    - circular rule: $\omega'\in \omega_1\cdot\omega$ and $\omega\in \omega'\cdot \omega_1$

The product can be defined on a set of concepts as well as
$A\cdot B = \{a\cdot b \mid a\in A,b\in B\}$,

The meaning of a concept is given by the transformations it induces and the transformations it participates in.

### Example: a family

To give an example, consider a family, the parents are Alice and Bob, the children are Cecile and Daniel. The fact that Alice's children are Cecile and Daniel can be represented as the concept "children" acts on "Alice" and results in the concepts "Cecile" and "Daniel". It can be interpreted that from "Alice" we associate to "Cecile" and "Daniel", if the "children" concept (context) is given. Formally:
$$ \text{Alice}\cdot\text{children} = \{\text{Cecile}, \text{Daniel} \}.$$

But it also induces other associations. If we hear "Cecile", by the name "Alice" we associate to "children" (eventually even more). Or if we start with "children", then "Cecile" makes us remember "Alice" and "Bob".
$$ \text{Cecile}\cdot\text{Alice} = \{\text{children},\dots\},$$
$$ \text{children}\cdot\text{Cecile} = \{\text{Alice}, \text{Bob}\}.$$

So each concept can serve as an object, or as a context of other objects, or the value of the association.

### Example: classification of an image

Classification of images, in principle, is very simple in this framework. If we take an actual image, then any concept we know may or may not result a new concept. For example an image depicting cats we will have
$$
\begin{aligned}
 & \text{cat image}\cdot\text{cat} = \{\text{cat1-in-the-image}, \text{cat2-in-the-image},\dots \}\\
 & \text{dog image}\cdot\text{cat} = \emptyset.\\
\end{aligned}
$$

Alternatively, if we only want to tell apart cat and dog images, then we can set up a "cat-and-dog-classifier" concept, which works as we think it will work:
$$ 
\begin{aligned}
 & \text{cat image}\cdot\text{cat-and-dog-classifier} = \{\text{cat}\}\\
 & \text{dog image}\cdot\text{cat-and-dog-classifier} = \{\text{dog}\}\\
 & \text{cat and dog image}\cdot\text{cat-and-dog-classifier} = \{\text{cat}, \text{dog}\}\\
\end{aligned}
$$

It is, of course, a more difficult question, how to realize these operation, we will discuss it later.

## New concepts, general and actual reality

The collection of concepts is not closed, we create and forget concepts all the time.

First of all, when we find a new object in our surroundings, then we immediately assign a concept to it, with a unique identifyer. We also automatically insert this new concept to the net of concepts. For example if a take a pen, the actual pen will have an ID, for example "pen-1768645481", referring to the creation time, but othe ID is possible. We assign a "is-a" concept to it like
$$ \text{pen-1768645481}\cdot\text{is-a} = \{\text{pen}\}.$$
Now we can assign all the properties of the general "pen" for the actual one, for example
$$ \text{pen-1768645481}\cdot\text{color} = \{\text{blue}\}.$$
Occasionally we can update the "color" concept and have
$$ \text{color}.\text{blue} = \{\text{pen-1768645481},\dots\},$$
which means that we will associate from the blue object to the actual pen.

The object in our surrounding make up the "actual reality", while the general object classes form the "general reality". All the properties of the general reality appear in the actual object, with the actual values. But the actual object may have specific properties, too. For example an actual pen can have an engraving, or a dot painted on it.

## Concepts with several arguments

A lot of properties are not connecting one concept to another, but their meaning can depend on other factors, too. For example the "where-is" concept can have different meaning: in an image the "where is the cat" question may have the answer "in the middle of the image", or "laying on a coach". The former refers to the position in the image, the latter the position in the real world. The action (meaning) of the "where-is" concept is context dependent.

Mathematically, if we connected three elements, then we can connect any number of them, by pulling apart the components. In the case of the example we may speak about "position-in-the-image" or "position-in-the-house", or even more. These are created as
$$ 
\begin{aligned}
 & \text{where-is}\cdot\text{image} = \{\text{position-in-the-image}\}\\
 & \text{where-is}\cdot\text{house} = \{\text{position-in-the-house}\}.\\
\end{aligned}
$$
Then we have the following connections
$$ 
\begin{aligned}
 & \text{actual image}\cdot\text{cat} = \{\text{cat-in-the-image}\}\\
 & \text{cat-in-the-image}\cdot\text{position-in-the-image} = \{\text{center}\}\\
 & \text{cat-in-the-image}\cdot\text{position-in-the-house} = \{\text{on-the-coach}\}.\\
\end{aligned}
$$

## Representation and robustness

The net of concepts is pretty much unique, as we can represent the reality in a lot of ways. There is not an ideal way to do it, different representations result in different properties, first of all as the efficiency and robustness is concerned.

### System-1

We can have concept created specially to perform a given task. We have seen in the image classification example that the "cat-and-dog-classifier" concept very nicely can tell apart cats and dogs. If this task is very important, it is worth to maintain a separate concept exclusively for this.

Usually this System-1 concepts result an immediate action, in abstract notation
$$ \text{sensory input}\cdot\text{System-1-concept} = \{\text{action},\dots\}.$$

#### Advantages

- **natural**: this is the most natural approach for a living being, an issue in the environment directly leads to reaction.
- **prompt**: this decision making is fast, and can be very accurate if it is adequate
- **small effort**: it requires a single, albeit complicated concept, thus the useage of this concept is cheap, requires not too lot of resources. This is why different System-1 applications can run parallel in the same time (e.g. walking and chewing gum).

#### Disadvantages

- **error conctrol**: the action is done without any double check if the concept is activated. But there can be tricky or complicated situations where a superficial decision is not correct.
- **unawareness**: System-1 concepts do not know, if they make a mistake. They do not know, what they know, or what they don't know. They do an instinctive reaction, the concept of "thinking" is not sensible in this approach.
- **analyticity**: in numerical implementation all concepts are results of analytic calculation. This requires that the probability of performing a possible action is approximately the same (balanced classes). For example, this approach is not useful for tell apart cat images and non-cat images, because non cat images form a vastly larger set. In such a space, distinguishing one element from all others by direct enumeration is combinatorially prohibitive.
- **specific**: these concepts are very special, and so the the generalizability is very tedious. For example the concept that separates dog and cat images can not be used for other purposes. For a different task a different specific concept has to be created (catastrophic forgetting). For the same reason, System-1 concepts are hard to train, we need a lot of sepcific examples to do that.
- **fragile**: if we forget the concept, there is no way to recreate is from other knowledge. We have to restart the creation of it, and we can just hope that we arrive to the same good result. Professional athletes can have the experience that suddenly they "forget" how to do the given sport effectively.

For all this reasons the applicability of System-1 concepts is limited. If there is a task that appear frequently, requires fast and accurate performance, then it is justified to set up such concepts.

In human thinking, System-1 appears in different levels. The ancient, elementary functions of our body works in this way, like the immune system, the reflexes, the elementary feelings and actions (like walking, reaching for an object, etc.). It also appears when we often have to do some action, then the nervous system slowly creates a unique concept relevant for that given task: this is riding a bycicle or driving a car. This mechanism can be used to force the mind to create System-1 concepts, for example when we practice something very frequently, and in a focused way. Doing competitive sports or martial arts require such concepts, otherwise the reactions are to slow and inaccurate.

### System-2

In the other approach to decide to make an action, we apply several concepts. We try to understand the meaning of the sensory inputs, make an maintain a model of the surrounding world. A new issue is analyzed from a lot of points of view, and we also try out different action scenarios before we decide to perform the given action. All of these tasks require the application of a lot of concepts. Even when some of them are independent, and so they are parallelizable, alltogether they require so large effort that we usually can run just a single System-2 process.

#### Coordination

A version of the implementation of System-2 is to fix those concepts that we want to apply to the input. Then they all have to be sensible for any input we can get, but in exchange they can be performed parallel at the same time. The applied concepts, on the other hand, can be simple, and result to a large set of possible outputs. The resulting action comes as the intersection of the results of the elementary concepts.

Formally we can introduce the coordiantion as follows:

- **coordination**: a set of $\{c_1, c_2,\dots,c_n\}$ concepts is called coordination. It acts on the input
$$ \text{input}\cdot c_i = r_i,$$
where $r_i$ are the results of the elementary concepts. The final result comes from
$$ \text{final result} = \bigcap_{i=1}^n r_i.$$
So all elementary concepts shrink the resulting set.

#### Concept hierarchy

Usually the concepts are not sensible for any inputs. For example the "display size" is not sensible for foods, and "fat content" is not sensible for electronic devices.

To accomodate to this fact, we can speak about a hierarchy of concepts. At each level of the reality representation, there is an adequate coordination. The final result of the given level introduced above forms the next level of the concept hierarchy.

- **concept hierarchy**: at level $\ell$ we have a set of concepts $C_\ell$, having a coordination $\mathcal C_\ell$. The next level we obtain as
$$ C_{\ell+1} = \text{final result}_{\mathcal C_{\ell}}(C_\ell)$$
while $C_0 = \{\text{inputs}\}$. The recursion stops after a given number of steps, or when the available concepts can not refine the result any more.

In this process each level updates the result, introduces a new, finer representation of reality.

A typical example is taxonomy where a givel species is given by the more and more refined concepts. Here the concept hierarchy is a tree, and each leaf has a unique path to it (the **prefix code** of that leaf). The optimal concept tree contains the shortest average path length: if we know the probabilities of the leaves, it can be done by **Huffman coding**.

## Other definitions

There are other notions that are used in general when the theory of representation is discussed. For completeness, we recall these concepts and define in the present approach.

- **feature**: concept $f$ is a feature of concept $c$, if $c\cdot f\neq\emptyset$
    - alternative name: **relevant concept**
    - **irrelevant concept**:  a concept that is not a feature

- **context**: the context of a concept $c$ is the collection of its features:
$$\mathcal C : c \mapsto \{f \mid c\cdot f\neq\emptyset\}$$



The features of a context are also features of a finer context:

- **extension** (of a feature):  $(\mathcal C \to B) \to (\mathcal C'\to B)$ if $\mathcal C \preceq \mathcal C'$, $f(c')= f(c)$ for $c'\in c$
    - constant over several classes of the finer context

This does not work the other way around. Some of the features of a given context are contexts of another one, some are not.

- **relevant** (feature): $(\mathcal C, f) \mapsto f\in \mathcal F_\mathcal C =$ true iff the induced context of $f$ is subcontext of $\mathcal C$
    - alternative name: selective feature

- **irrelevant concept** (feature): not relevant
    - alternative name: descriptive function

