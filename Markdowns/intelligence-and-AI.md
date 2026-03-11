
- **intelligence and AI**
    - **why do we need intelligence?**
        - goal of a living being
        - why intelligence, not science?
    - **goal of a living being**
        - survival in a complex environment
        - has to react to the environmental issues: $\text{issue}\to\text{action}$
        - changing environment $\to$ adaptation (learning)
    - **definitions**
        - __Turing’s intelligence definition__
        - __Legg–Hutter intelligence definition__
        - __classification-based intelligence definition__
        - __representation-based intelligence definition__


- **Turing’s intelligence definition**
    - **historical context**
      - proposed in 1950, at a time when the internal mechanisms of thinking machines were unknown and difficult to formalize
    - **methodological principle**
      - intelligence should be defined operationally, by behavior, rather than by internal structure or subjective notions such as consciousness 
      - __Turing test__
    - **formulation**
      - a machine is considered intelligent if, in unrestricted textual conversation, a human interrogator cannot reliably distinguish it from a human


- **Turing test**
    - **setup**
        - a human interrogator communicates via text with two hidden participants
        - one participant is human, the other is a machine
        - the interrogator may ask arbitrary questions
    - **criterion**: the machine passes the test if the interrogator cannot reliably distinguish it from the human
    - **criticism**
        - allows superficial pattern imitation to succeed: the Turing test evaluates indistinguishability of behavior, not the presence of internal understanding or goals
        - lead to tricky machines instead of real intelligence (__ELIZA__, __Eugene Goostman__)
    - **impact**
        - became the most influential and widely discussed benchmark for machine intelligence, shaping both AI research and public perception
    - **programs**
        - __ELIZA__
        - __PARRY__
        - __Eugene Goostman__

- **ELIZA**:
    - written by Joseph Weizenbaum (1966)
    - simple pattern matching, mimicking a Rogerian psychotherapist
    - Why it mattered: Some users felt understood and attributed intelligence to it
    - **Reality check**
        - No deception of expert interrogators
        - No unrestricted dialogue
    - **Status**: Psychological effect, not a Turing Test pass

- **PARRY**
    - Creator: Kenneth Colby
    - What it did: simulated a paranoid patient
    - Notable experiment: psychiatrists judged transcripts of PARRY vs humans
    - Results: accuracy was only slightly better than chance
    - **Reality check**
        - Limited deception
        - Narrow persona
    - **Status**: Closest early approximation, but still not a true pass

- **Eugene Goostman** :
    - written by: Vladimir Veselov, Eugene Demchenko, Sergey Ulasen (2000-2014)
    - Claim: passed the Turing Test at the Royal Society
    - Trick: posed as a 13-year-old non-native English speaker
    - **Reality check**
        - Short conversations
        - Non-standard test setup
        - Exploited lowered expectations
    - **Status**: Widely criticized claim, not accepted by experts

- **Legg–Hutter intelligence definition**
    - **historical context**: proposed in the mid-2000s in the context of formal, universal definitions of intelligence
    - **core idea**: define intelligence measure based on how an agent achieves its goals in a wide range of environments
    - **formulation** 
        - weighted average of performances over environments $$ \text{intelligence}(\text{agent}) = \!\!\!\sum\limits_{E\in\text{environments}} 2^{-K(E)}\, \mathbb E (\text{reward from }E)$$
        - weight: $K(E)$ Kolmogorov complexity
        - simple environments are more probable than complex ones
    - **advantages**
        - provides a precise, mathematical definition of intelligence
        - applies uniformly to humans, animals, and machines
        - explicitly captures generality across environments
        - avoids reliance on language or human imitation
    - **disadvantages**
        - relies on uncomputable quantities (Kolmogorov complexity)
        - assumes a fixed reward-based notion of goals
        - offers little guidance for practical system design
        - abstracts away representation and internal structure
    - **impact**: established a rigorous theoretical benchmark for general intelligence and influenced research on universal agents (e.g. AIXI)
    > Legg–Hutter intelligence is a normative, idealized definition rather than an operational or experimentally testable criterion

- **classification-based intelligence definition**
    > this definition evaluates intelligence by output equivalence, not by the quality or structure of internal representations
    - **historical context**: emerged implicitly with the success of supervised learning and __DNNs__ in perception tasks
    - **core idea**: a machine is considered intelligent if it classifies inputs in the same way a human does
    - **formal formulation**
        - let $X$ be an input space (e.g. images, sounds, texts)
        - let $\mathcal C_{\text{human}}$ be a context (partition of $X$) induced by human labeling
        - let $\mathcal C_{\text{machine}}$ be a context induced by a trained model
        - the machine is intelligent on $X$ if
          $\mathcal C_{\text{machine}} \approx \mathcal C_{\text{human}}$
          on a representative test set
        - measured by benchmarks
    - **typical applications**
        - image classification
        - speech recognition
        - text categorization
        - medical image diagnosis
    - **advantages**
        - simple, operational, and experimentally testable
        - enables large-scale benchmarking and rapid technological progress
        - effective for narrow, well-defined tasks
    - **corresponds to System 1–style intelligence**
        - intelligence is reduced to a single fixed context
        - no notion of goals, planning, or agency
        - no representation of uncertainty or error control
        - does not require understanding, grounding, or adaptability
        - focuses on direct pattern discrimination rather than structured representation


- **representation-based intelligence definition**
    - **core ideas**
        - environment is too complicated that an agent could react to each situations one-by-one  
        - intelligence is the ability of an agent to construct, refine, and use internal representations (model) of reality in order to act successfully within it
        - representation-based intelligence treats intelligence as a structural property of an agent’s internal world model, not merely as a pattern of outputs
    - **representation**
        - different tasks represent different contexts
        - select relevant features in the context, and ignore irrelevant details
        - representations may be refined hierarchically (__learning__)
    - **advantages**
        - explains generalization and transfer across tasks
        - naturally incorporates uncertainty and abstraction
        - applies to humans, animals, and machines
        - unifies perception, reasoning, and action under a single framework
    - **limitations**
        - more difficult to operationalize than behavior-only definitions
        - requires explicit modeling of representation structures
        - success depends on defining appropriate relevance and goals

- **learning**
    - **core idea**: a process that improves future performance by modifying internal structure or behavior based on experience
    - **unifying view**: learning refines representations, parameters, or selections under constraints
    > evolution is learning at the population level

- **changes in problem solving**
    - **historic times problem solving**
        - observation made by: human
        - modelling done by: human
        - computation done by: human
        - action taken by: human
    - **machines and measurement instruments**
        - observation made by: machine
        - modelling done by: human
        - computation done by: human
        - action taken by: human
    - **XX. century and computers**
        - observation made by: machine
        - modelling done by: human
        - computation done by: machine
        - action taken by: human
    - **XXI. century and artificial intelligence**
        - observation made by: machine
        - modelling done by: machine
        - computation done by: machine
        - action taken by: human
    - **methods**
        - __traditional algorithms__
        - __artificial intelligence based problem solving__

- **traditional algorithms**
    - **workflow**
        - understand the problem
        - write a code
        - run the code
    - **characteristics**
        - machine does the same task humans would do, only faster
        - machine is not smarter, only faster

- **artificial intelligence based problem solving**
    - **workflow**
        - understand learning
        - write a learning algorithm
        - the algorithm learns and solves the problem
    - **characteristics**
        - solution is not explicitly known
        - machine can be smarter in specific domains!

- **representation of reality**
    - **aspects**
        - __general reality__
        - __actual reality__
    - **mainstream AI representation**: general reality is represented much more deeply than actual reality
    - **methods**
        - __gather information__
        - extracting relevant features

- **general reality**
    > laws and generic mechanisms describing how the world works
    - **examples**
        - maps of streets
        - internal structure of LLMs predicting token sequences
        - sports equipment and physical abilities
    - **improvement methods**
        - better tools
        - training
    - **in AI**: encoded in trained hardware and parameters (millions to ~100 billion parameters)

- **actual reality**
    > the currently active environment, objects, persons, and phenomena
    - **examples**
        - traffic conditions on a map
        - prompts defining tasks for LLMs
        - current physical state of an athlete
    - **in AI**:  represented by input data (up to millions of tokens)
    - **using initial conditions**
        - represent the current state
        - exact prediction possible only in ideal systems
        - real systems have limited validity ranges
        - hallucination radius in LLMs
    - **how can we maintain precision**
        - continual projection onto actual reality
        - control may be simple
        - example: lossless compression



- **gather information**
    - **characteristics**
        - factual
        - interpretation-agnostic
    - **in IT**
        - big data approaches
        - avoidance of information loss
        - very large datasets
    - **examples**
        - pixel colors
        - logs
        - wave amplitudes
    - **storage methods**
        - data lakes
        - relational databases
        - non-relational databases

