# Intelligence

This note is about the concept intelligence 

---
<a id="intelligence"></a>
- **intelligence**
    - goal of a living being
        - survival in a complex environment
        - has to react to the environmental issues: $\text{issue}\to\text{action}$
        - changing environment $\to$ adaptation (learning)
    - definitions:
        - Turing intelligence definition
        - Legg–Hutter intelligence definition
        - DNN-based definition
        - representation-based intelligence definition

---
<a id="turing-intelligence"></a>
- **Turing’s intelligence definition**
    - historical context:
      proposed in 1950, at a time when the internal mechanisms of thinking machines were unknown and difficult to formalize
    - methodological principle:
      intelligence should be defined operationally, by behavior, rather than by internal structure or subjective notions such as consciousness - Turing test
    - formulation:
      a machine is considered intelligent if, in unrestricted textual conversation, a human interrogator cannot reliably distinguish it from a human

---
<a id="turing-test"></a>
- **Turing test**
    - setup:
        - a human interrogator communicates via text with two hidden participants
        - one participant is human, the other is a machine
        - the interrogator may ask arbitrary questions
    - criterion:
      the machine passes the test if the interrogator cannot reliably distinguish it from the human
    - criticism: 
        - allows superficial pattern imitation to succeed: the Turing test evaluates indistinguishability of behavior, not the presence of internal understanding or goals
        - lead to tricky machines instead of real intelligence (ELIZA, Eugeen )
    - impact:
      became the most influential and widely discussed benchmark for machine intelligence, shaping both AI research and public perception
    - programs:
        - ELIZA
        - PARRY
        - Eugeen Goostman

- **ELIZA**:
    - written by Joseph Weizenbaum (1966)
    - simple pattern matching, mimicking a Rogerian psychotherapist
    - Why it mattered: Some users felt understood and attributed intelligence to it
    - Reality check:
        - No deception of expert interrogators
        - No unrestricted dialogue
    - Status: Psychological effect, not a Turing Test pass

- **PARRY**
    - Creator: Kenneth Colby
    - What it did: simulated a paranoid patient
    - Notable experiment: psychiatrists judged transcripts of PARRY vs humans
    - Results: accuracy was only slightly better than chance
    - Reality check:
        - Limited deception
        - Narrow persona
    - Status: Closest early approximation, but still not a true pass

- **Eugene Goostman** :
    - written by: Vladimir Veselov, Eugene Demchenko, Sergey Ulasen (2000-2014)
    - Claim: passed the Turing Test at the Royal Society
    - Trick: posed as a 13-year-old non-native English speaker
    - Reality check:
        - Short conversations
        - Non-standard test setup
        - Exploited lowered expectations
    - Status: Widely criticized claim, not accepted by experts

---
<a id="legg-hutter-intelligence"></a>
- **Legg–Hutter intelligence definition**
    - historical context:
      proposed in the mid-2000s in the context of formal, universal definitions of intelligence
    - core idea: define intelligence measure based on how an agent achieves its goals in a wide range of environments
    - formulation: 
        - weighted average of performances over environments $$ \text{intelligence}(\text{agent}) = \!\!\!\sum\limits_{E\in\text{environments}} 2^{-K(E)}\, \mathbb E (\text{reward from }E)$$
        - weight: $K(E)$ Kolmogorov complexity
        - simple environments are more probable than complex ones
    - advantages:
        - provides a precise, mathematical definition of intelligence
        - applies uniformly to humans, animals, and machines
        - explicitly captures generality across environments
        - avoids reliance on language or human imitation
    - disadvantages:
        - relies on uncomputable quantities (Kolmogorov complexity)
        - assumes a fixed reward-based notion of goals
        - offers little guidance for practical system design
        - abstracts away representation and internal structure
    - impact:
      established a rigorous theoretical benchmark for general intelligence and influenced research on universal agents (e.g. AIXI)
    - note:
      Legg–Hutter intelligence is a normative, idealized definition rather than an operational or experimentally testable criterion

---
<a id="classification-based-intelligence"></a>
- **classification-based intelligence definition**
    - historical context:
      emerged implicitly with the success of supervised learning and deep neural networks in perception tasks
    - core idea:
      a machine is considered intelligent if it classifies inputs in the same way a human does
    - formal formulation:
        - let $X$ be an input space (e.g. images, sounds, texts)
        - let $\mathcal C_{\text{human}}$ be a context (partition of $X$) induced by human labeling
        - let $\mathcal C_{\text{machine}}$ be a context induced by a trained model
        - the machine is intelligent on $X$ if
          $\mathcal C_{\text{machine}} \approx \mathcal C_{\text{human}}$
          on a representative test set
        - measured by benchmarks
    - typical applications:
        - image classification
        - speech recognition
        - text categorization
        - medical image diagnosis
    - advantages:
        - simple, operational, and experimentally testable
        - enables large-scale benchmarking and rapid technological progress
        - effective for narrow, well-defined tasks
    - corresponds to System 1–style intelligence
        - intelligence is reduced to a single fixed context
        - no notion of goals, planning, or agency
        - no representation of uncertainty or error control
        - does not require understanding, grounding, or adaptability
        - focuses on direct pattern discrimination rather than structured representation
    - note:
      this definition evaluates intelligence by output equivalence, not by the quality or structure of internal representations

---
<a id="representation-based-intelligence"></a>
- **representation-based intelligence definition**
    - core ideas:
        - environment is too complicated that an agent could react to each situations one-by-one  
        - intelligence is the ability of an agent to construct, refine, and use internal representations (model) of reality in order to act successfully within it
        - representation-based intelligence treats intelligence as a structural property of an agent’s internal world model, not merely as a pattern of outputs
    - representation:
        - different tasks represent different contexts
        - select relevant features in the context, and ignore irrelevant details
        - representations may be refined hierarchically (learning)
    - advantages:
        - explains generalization and transfer across tasks
        - naturally incorporates uncertainty and abstraction
        - applies to humans, animals, and machines
        - unifies perception, reasoning, and action under a single framework
    - limitations:
        - more difficult to operationalize than behavior-only definitions
        - requires explicit modeling of representation structures
        - success depends on defining appropriate relevance and goals

---
<a id="learning"></a>
- **learning**
    - core idea:
      a process that improves future performance by modifying internal structure or behavior based on experience
    - unifying view:
      learning refines representations, parameters, or selections under constraints
    - note:
      evolution is learning at the population level

---
<a id="learning-by-selection"></a>
- **learning by selection**
    - principle:
      generate variants and retain those with higher success
    - mechanisms:
        - biological evolution
        - cultural evolution
        - genetic algorithms
        - model and feature selection
    - characteristic:
      population-level learning across generations

---
<a id="learning-by-optimization"></a>
- **learning by optimization**
    - principle:
      improve parameters to minimize or maximize an objective function
    - mechanisms:
        - gradient descent
        - maximum likelihood estimation
        - backpropagation
        - convex optimization
    - characteristic:
      assumes a parameterized representation and a loss function

---
<a id="learning-by-association"></a>
- **learning by association**
    - principle:
      strengthen connections between co-occurring events
    - mechanisms:
        - Hebbian learning
        - correlation-based learning
        - self-organizing maps
        - contrastive learning
    - characteristic:
      local, often unsupervised representation formation

---
<a id="learning-by-reinforcement"></a>
- **learning by reinforcement**
    - principle:
      learn actions through reward and punishment
    - mechanisms:
        - reinforcement learning
        - operant conditioning
        - trial-and-error learning
    - characteristic:
      delayed feedback and exploration–exploitation tradeoff

---
<a id="learning-by-abstraction"></a>
- **learning by abstraction**
    - principle:
      discover relevant distinctions and invariants
    - mechanisms:
        - representation learning
        - feature learning
        - context formation
        - refinement trees
    - characteristic:
      changes how the world is represented

---
<a id="learning-by-compression"></a>
- **learning by compression**
    - principle:
      remove redundancy while preserving relevant information
    - mechanisms:
        - minimum description length
        - information bottleneck
        - PCA and dimensionality reduction
        - lossy compression
    - characteristic:
      compact representations enable generalization

---
<a id="learning-by-imitation"></a>
- **learning by imitation**
    - principle:
      acquire behavior by copying others
    - mechanisms:
        - imitation learning
        - behavior cloning
        - social learning
    - characteristic:
      transfers knowledge without explicit optimization

---
<a id="learning-by-reasoning"></a>
- **learning by reasoning**
    - principle:
      derive new knowledge through inference and symbol manipulation
    - mechanisms:
        - logical deduction
        - theorem proving
        - planning
        - program synthesis
    - characteristic:
      discrete, compositional, System-2–style learning

---
<a id="learning-by-interaction"></a>
- **learning by interaction**
    - principle:
      learn by actively querying and experimenting with the environment
    - mechanisms:
        - active learning
        - exploration
        - curiosity-driven learning
    - characteristic:
      agent controls data acquisition

---
<a id="learning-by-coordination"></a>
- **learning by coordination**
    - principle:
      integrate multiple partial or coarse representations into a coherent whole
    - mechanisms:
        - multi-view learning
        - sensor fusion
        - multimodal learning
        - common refinement of contexts
    - characteristic:
      intelligence emerges from combining representations

---
<a id="unifying-perspective"></a>
- **unifying perspective of learning methods**
    - insight:
      all learning methods differ mainly in *what they modify*
    - table:
        - selection → populations
        - optimization → parameters
        - association → connections
        - reinforcement → policies
        - abstraction → representations
        - coordination → contexts
    - note:
      representation quality ultimately determines learning success


---
<a id="problem-solving"></a>
- **problem solving**
    - approaches:
        - historic times problem solving
        - problem solving with machines
        - problem solving with computers
        - problem solving with artificial intelligence
    - methods:
        - traditional algorithms
        - AI-based problem solving

---
<a id="historic-problem-solving"></a>
- **historic times problem solving**
    - observation made by: human
    - modelling done by: human
    - computation done by: human
    - action taken by: human

---
<a id="machine-problem-solving"></a>
- **problem solving with machines**
    - observation made by: machine
    - modelling done by: human
    - computation done by: human
    - action taken by: human

---
<a id="computer-problem-solving"></a>
- **problem solving with computers**
    - observation made by: machine
    - modelling done by: human
    - computation done by: machine
    - action taken by: human

---
<a id="ai-problem-solving"></a>
- **problem solving with artificial intelligence**
    - observation made by: machine
    - modelling done by: machine
    - computation done by: machine
    - action taken by: human

---
<a id="traditional-algorithms"></a>
- **traditional algorithms**
    - workflow:
        - understand the problem
        - write a code
        - run the code
    - characteristics:
        - machine does the same task humans would do, only faster
        - machine is not smarter, only faster

---
<a id="ai-based-problem-solving"></a>
- **artificial intelligence based problem solving**
    - workflow:
        - understand learning
        - write a learning algorithm
        - the algorithm learns and solves the problem
    - characteristics:
        - solution is not explicitly known
        - machine can be smarter in specific domains!

---
<a id="representation-of-reality"></a>
- **representation of reality**
    - aspects:
        - general reality
        - actual reality
    - mainstream AI representation:
      general reality is represented much more deeply than actual reality
    - methods:
        - gathering information
        - extracting relevant features

---
<a id="general-reality"></a>
- **general reality**
    - description:
      laws and generic mechanisms describing how the world works
    - examples:
        - maps of streets
        - internal structure of LLMs predicting token sequences
        - sports equipment and physical abilities
    - improvement methods:
        - better tools
        - training
    - in AI:
      encoded in trained hardware and parameters (millions to ~100 billion parameters)

---
<a id="actual-reality"></a>
- **actual reality**
    - description:
      the currently active environment, objects, persons, and phenomena
    - examples:
        - traffic conditions on a map
        - prompts defining tasks for LLMs
        - current physical state of an athlete
    - in AI:
      represented by input data (up to millions of tokens)
    - initial conditions:
        - represent the current state
        - exact prediction possible only in ideal systems
        - real systems have limited validity ranges
        - hallucination radius in LLMs
    - maintaining precision:
        - continual projection onto actual reality
        - control may be simple
        - example: lossless compression

---
<a id="worldview"></a>
- **worldview**
    - approaches:
        - scientific worldview
        - intelligence-based worldview

---
<a id="gather-information"></a>
- **gather information**
    - characteristics:
        - factual
        - interpretation-agnostic
    - in IT:
        - big data approaches
        - avoidance of information loss
        - very large datasets
    - examples:
        - pixel colors
        - logs
        - wave amplitudes
    - storage methods:
        - data lakes
        - relational databases
        - non-relational databases


---
<a id="ai"></a>
- **artificial intelligence (AI)**
    - successes:
        - classification
        - text generation
        - image generation
        - autonomous cars
    - business value:
        - billion-USD-scale industry (2023: ~200 bUSD)
    - challenges:
        - needs balanced datasets
        - catastrophic forgetting
        - no error control
        - no intrinsic goals or planning

---
<a id="no-error-control"></a>
- **no error control**
    - issues:
        - adversarial attacks
        - hallucinations

---
<a id="balanced-datasets"></a>
- **AI needs balanced datasets**
    - requirements:
        - representative samples for all categories
        - sufficient number of samples for all categories
    - technologies:
        - data augmentation
        - synthetic data generation

---
<a id="ai-classification"></a>
- **AI classification**
    - examples:
        - dog breeds
        - faces
        - birdsong
        - flowers

---
<a id="text-generation"></a>
- **text generation**
    - examples:
        - ChatGPT
        - Bing
        - DeepSeek

---
<a id="image-generation"></a>
- **image generation**
    - examples:
        - Midjourney
        - DALL·E
        - DreamStudio

---
<a id="autonomous-cars"></a>
- **autonomous cars**
    - examples:
        - AI driving assistants

