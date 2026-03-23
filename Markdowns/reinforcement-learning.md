
- **reinforcement learning**
    > how to learn in environments where the reward arrives later?
    - **action-focused approach**: learning a policy that selects actions to optimize long-term cumulative reward
    - **application areas**
        - __board games and computer games__
        - __robotics__
        - self-driving cars  
          → typically a combination of algorithmic methods, supervised learning, and RL
        - portfolio optimization
        - recommendation systems (e.g. Youtube, Netflix, TikTok, Amazon, Spotify, etc.)
        - industrial control systems (e.g. energy network optimization)
        - healthcare and personal health management
        - language models, for fine-tuning learning using human preferences (RLHF)
    - **core components**
        - <b>agent</b>: the decision-making entity (e.g. player, driver, robot, language model)
        - <b>environment</b>: the external system the agent interacts with  
        (e.g. a chessboard and the opposing player, a road network, a simulated world)
        - <b>state</b>: a representation of the current situation of the environment,  
        on which the agent bases its decisions
        - <b>action</b>: an element of the action space available to the agent;  
        actions influence the future state of the environment
        - <b>reward</b>: a scalar feedback signal measuring immediate success or failure  
        (e.g. win: +1, draw: 0, loss: −1)

    - **policy (decision mechanism)**
        - __policy__
        - __what does an RL system learn?__
        - __Markov Decision Process (MDP)__
        - __Dynamic Programming__
        - __Two-Player Zero-Sum  Games__


    - **reward hypothesis**  
        - any goal-directed behavior can be formulated as the maximization of
          the <b>expected cumulative (long-term) reward</b>
        - the objective is typically <b>non-local in time</b>
          future rewards are taken into account via discounting
    - **challenges**:
        - <b>exploration issues</b>: the agent may exploit loopholes or glitches
        - <b>degenerate optima</b>: e.g. preferring safe draws over risky wins
        - <b>sparse or rare rewards</b>: important events may occur infrequently,
          making learning slow or unstable

- **What does an RL system learn?**
    - **policy**: learning policy is the main goal $\to$ deterministic or stochastic
    - **value functions**
        - for more detail: __value functions__
        - state-value and action-value functions are often learned **explicitly**
        - they provide an additional, strategy-independent source of information
        - crucial for balancing exploration vs. exploitation
    - **environment**
        - some RL systems also learn the **environment dynamics**
        (the transition model $P$), rather than assuming it is given
        - this leads to **model-based reinforcement learning**
    - **example: MuZero**
        - a general-purpose reinforcement learning algorithm
        - learns: the policy, the __value functions__, an internal model of the environment
        - all knowledge is learned directly from interaction with the environment,
          without access to explicit rules

- **Markov Decision Process (MDP)**
    > a system where the decision depends only on the current state (Markov property)
    - **formal definition**:  $$
      M = (S, A, P, r, \gamma)
      $$
        - $S$: set of states
        - $A$: set of possible actions
        - $P$: state transition probabilities  
          $$
          P(s_{t+1} \mid s_t, a_t)
          $$
        - $r$: reward function  
          $$
          r(s_t, a_t, s_{t+1}) \quad \text{or} \quad r(s_t, a_t)
          $$
        - $\gamma \in [0,1)$: discount factor for future rewards

- **policy**
    - a mapping from states (or observations) to actions
    - learned to <b>maximize the expected cumulative (long-term) reward</b>
    - implicitly balances reward maximization against loss avoidance
    - $ \pi(a \mid s) $: probability of choosing action $ a $ in state $ s $
    - defines the agent’s behavior

    - **exploration vs. exploitation**
        - <b>exploitation</b>: choose the action with the highest estimated value
        - <b>exploration</b>: try alternative actions to acquire new information
        - effective policies balance these two objectives
        - __common exploration strategies__

- **common exploration strategies**
    - **greedy policy**
        $$
        \pi(a \mid s) =
        \begin{cases}
        1, & a = \arg\max_{a'} Q(s,a') \\
        0, & \text{otherwise}
        \end{cases}
        $$
        - purely exploitative, no exploration

    - **$\varepsilon$-greedy policy**
        $$
        \pi(a \mid s) =
        \begin{cases}
        1-\varepsilon + \dfrac{\varepsilon}{|A|}, & a = \arg\max_{a'} Q(s,a') \\
        \dfrac{\varepsilon}{|A|}, & \text{otherwise}
        \end{cases}
        $$
        - explores with probability $ \varepsilon $
        - simple and widely used

    - **Boltzmann (softmax) exploration**
        $$
        \pi(a \mid s)
        = \frac{\exp\!\left(Q(s,a)/\tau\right)}
                {\sum_{a'} \exp\!\left(Q(s,a')/\tau\right)}
        $$
        - $ \tau $ (temperature) controls exploration
        - high $ \tau $: more random actions  
        - low $ \tau $: near-greedy behavior

    - **Upper Confidence Bound (UCB)**
        $$
        a_t
        = \arg\max_a
            \left(
            Q(s,a)
            + c \sqrt{\frac{\ln t}{N(s,a)}}
            \right)
        $$
        - favors actions with high uncertainty
        - $ N(s,a) $: number of times action $ a $ was selected in state $ s $
        - $ c $: exploration strength parameter
        - this is the classical (bandit) form, one can use $\ln t\to\ln N(s)$ (the number the state $s$ shows up)


- **value functions** 
    - **state-value function**
        - assume the agent follows policy $ \pi $
        - formula: $$
      V^\pi(s)
      = \mathbb{E}_\pi \left[
          \sum_{t=0}^{\infty} \gamma^t r(s_t, a_t)
          \,\bigg|\, s_0 = s
        \right]
      $$
      measures how good it is to be in state $ s $

    - **action-value function**
        - formula: $$
      Q^\pi(s, a)
      = \mathbb{E}_\pi \left[
          \sum_{t=0}^{\infty} \gamma^t r(s_t, a_t)
          \,\bigg|\, s_0 = s,\, a_0 = a
        \right]
      $$
      measures how beneficial it is to take action $ a $ in state $ s $

    - **relation between the two**: $$
      V^\pi(s) = \sum_{a \in A} \pi(a \mid s)\, Q^\pi(s, a)
      $$


- **Dynamic Programming**
    - **assumptions**
        - we known the environment dynamics $P(s'\mid s,a)$
        - the reward function $R(s,a, s')$
        - we have full information about environment
        - the state space is explorable
    - **goal**: learn the state-value function and the policy
    - **algorithm**
        - for a given policy obtain the the state-value function (__Bellman equation__)
        - for an optimal state-value function get the optimal policy (__Optimal Policy from the Bellman equation__)
        - alternative algorthms: __Q-learning__, __SARSA__
    - **remark**: game theory gives a similar approach
        - __Bellman equation__ $\to$ Nash equilibrium (in ideal cases)
    - **critics**
        - not full information game
        - not fully known reward function
        - the state and action space is too large
        - solution: __Monte Carlo control__, __MCTS__, __PUCT__

- **Bellman Equation**
    - **idea**
        - the value of a state equals the **immediate reward**
        plus the **expected discounted value of successor states**
        - expresses the principle of **optimal substructure**
    - **Bellman expectation equation (for a fixed policy $\pi$)**
    $$ V^\pi(s)  = \sum_{a} \pi(a \mid s)\sum_{s'}P(s' \mid s, a)\bigl[ r(s,a,s') + \gamma V^\pi(s')\bigr]$$
    - **explanation**
        - we choose an action with probability $\pi(a\mid s)$
        - the system goes into $s'$ with probability $P(s' \mid s, a)$
        - we obtain a rewards **and** a discounted reward from the future
    - **Bellman optimality equation**: simplified form when we choose only the best strategy
    $$ V^*(s)=\max_{a}\sum_{s'} P(s' \mid s, a)\bigl[r(s,a,s') + \gamma V^*(s')\bigr]$$
        - for two-player game: (c.f. __Two-Player Zero-Sum  Games__) $$V(s) = \max_{a}\min_{a'}[r(s,a,a') + \gamm V(s)]
        - __optimal Policy from the Bellman Equation__

- **Optimal Policy from the Bellman Equation**
    - **strategy**
        - assume the **optimal state-value function** $V^*(s)$ is known
        - the **optimal policy** is obtained by a one-step lookahead:
    $$\pi^*(s)=\arg\max_{a}\sum_{s'}P(s' \mid s,a)\bigl[r(s,a,s') + \gamma V^*(s')\bigr]$$
    - **interpretation**
        - evaluate all possible actions in the current state
        - choose the action that maximizes <b>immediate reward + discounted future value</b>
        - no further planning is required

- **Q-learning**
    > model-free reinforcement learning
    - **goal**
        - learn the **optimal action-value function** $Q^*(s,a)$
        - does **not** require an explicit model of the environment
      (no transition probabilities $P$)
    - **key idea**
        - replace the expectation in the Bellman optimality equation
          with **sampled transitions** from experience
        - learn directly from interaction with the environment
    - **update rule**: $$Q(s,a)\leftarrow Q(s,a)+\alpha\Bigl(r + \gamma \max_{a'} Q(s',a') - Q(s,a)\Bigr)$$
      where $s'$ is the state we arrive from $s$ and $a$
    - **properties**
        - off-policy: learns the optimal policy while following another
          (e.g. \(\varepsilon\)-greedy) policy
        - converges to $Q^*$ under sufficient exploration
        - scales well to unknown or complex environments

- **SARSA**
    > a model-free, on-policy reinforcement learning algorithm: learn the value of what you actually do.
    - **alternative name**: State–Action–Reward–State–Action
    - learns the action-value function $Q^\pi(s,a)$
      for the **policy actually being followed**
    - **update rule**: $$ Q(s,a)\leftarrow Q(s,a)+\alpha\Bigl(r + \gamma Q(s',a') - Q(s,a)\Bigr)$$
      where where $s'$ is the state we arrive from $s$ and $a$ and $a' \sim \pi(\cdot \mid s')$

    - **properties**
        - exploration **directly affects learning**
        - more conservative than Q-learning
        - often safer in stochastic or risky environments

- **Two-Player Zero-Sum  Games**
    - **setting**
        - two players: agent (maximizer) and opponent (minimizer)
        - rewards are opposite: $r_{\text{agent}} = - r_{\text{opponent}}$
        - typical examples: chess, Go, checkers
    - **state-value function**
        - value is defined from the agent’s perspective
        - positive value → winning position
        - negative value → losing position

    - **Bellman optimality equation (minimax form)**
        $$V^*(s)=\begin{cases}
            \displaystyle \max_{a}\sum_{s'}P(s' \mid s,a)\bigl[r(s,a,s') + \gamma V^*(s')\bigr], & \text{agent’s turn}\\
            \displaystyle \min_{a}\sum_{s'}P(s' \mid s,a)\bigl[r(s,a,s') + \gamma V^*(s')\bigr], & \text{opponent’s turn}
        \end{cases}$$

    - **interpretation**
        - the agent assumes the opponent plays **optimally**
        - replaces expectation over actions by **max–min**
        - this is the Bellman version of the **minimax principle**


- **board games and computer games**
    - **challenge**: evaluation of a strategy is typically available only at the end of the game (e.g. win / loss)
    - **successful AI agents**
        - chess engines: __Leela__, __Stockfish__
          Elo rating ≈ 3500 (best human ≈ 2800)
        - Go: __AlphaGo__
        - Dota 2: __OpenAI Five__ → world-champion level
        - StarCraft II: __AlphaStar__ → world-champion level
    - **preformance**: in closed-information games, AI systems can outperform human players

- **robotics**
    - **challenge**: success of a sequence of actions is often observed only at the end  
      (e.g. moving a robotic arm, grasping or catching an object)
    - training is frequently performed in simulation for efficiency and safety
    - **real-world examples**
        - [Boston Dynamics](https://www.youtube.com/@BostonDynamics)
        - [Moley Robots](https://www.youtube.com/watch?v=mKCVol2iWcc)
    - **specialized subfields**
        - drone control and training
        - multi-robot coordination

- **Leela**
    >  Chess Zero's chessbot
    -  **Paper**: Silver, D. et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. Nature, 362, 1140–1144. (Leela Chess Zero is an open-source reimplementation of AlphaZero-style learning.)
    - **Project page**: [https://lczero.org](https://lczero.org)
    - **Code**: [https://github.com/LeelaChessZero/lc0](https://github.com/LeelaChessZero/lc0)

- **Stockfish**
    - **Description / reference**: Romstad, T., Costalba, M., Kiiski, J., & Österlund, G. Stockfish: a strong open-source chess engine.
    - **Official website**: [https://stockfishchess.org](https://stockfishchess.org)
    - **Code**: [https://github.com/official-stockfish/Stockfish](https://github.com/official-stockfish/Stockfish)
    - **Remark**: Stockfish is primarily a classical search + evaluation engine, but modern versions integrate neural-network-based evaluation (NNUE).

- **AlphaGo**
    - **Paper**: Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. Nature, 529, 484–489.
    - **Follow-up**: Silver, D. et al. (2017). Mastering the game of Go without human knowledge. Nature, 550, 354–359.

- **OpenAI Five**
    > Dota 2 game engine
    - **Paper**: Berner, C. et al. (2019). Dota 2 with Large Scale Deep Reinforcement Learning. arXiv:1912.06680
    - **Blog / overview**: [https://openai.com/research/openai-five](https://openai.com/research/openai-five)
    - **Key point**: Demonstrates large-scale multi-agent RL with partial observability and delayed rewards.

- **AlphaStar**
    - **Paper**: Vinyals, O. et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning. Nature, 575, 350–354.
    - **Blog**: [https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/](https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/)


- **Monte Carlo control**
    - **motivation**
        - __Dynamic Programming__ requires: full knowledge of transition probabilities $P$ and complete sweeps over the state space
        - often infeasible in large or unknown environments
    - **alternates between**
        - policy evaluation (MC estimation of values)
        - policy improvement (making the policy better)

    - **policy evaluation**
        - fix a policy $\pi$
        - generate episodes using $\pi$: starting from $s_0$ and $a_0$ generate $$(s_0,r_0,a_0; s_1,r_1,a_1;\dots;s_N,r_N,a_N)$$
        - cumulative discounted reward from time $t$:
        $$ G_t = \sum_{k=0}^{T-t-1} \gamma^k r_{t+k+1}$$
        - estimate action values:
        $$ Q^\pi(s,a) \approx \mathbb{E}_\pi[G_t \mid s_t=s, a_t=a]$$

    - **policy improvement**
        - update the policy to prefer actions with higher $Q$-values
        - greedy improvement:
        $$ \pi(s) \leftarrow \arg\max_a Q(s,a)$$

    - **maintaining exploration**
        - use an $\varepsilon$-greedy policy:
        - with probability $1-\varepsilon$: choose the best action
        - with probability $\varepsilon$: explore randomly
        - ensures continued state–action coverage

    - **policy iteration loop**
        - evaluate policy → improve policy → repeat
        - converges to an optimal policy under sufficient exploration


- **MCTS**
    - **full name**: Monte Carlo Tree Search
    - **idea**
        - planning algorithm based on random sampling
        - builds a partial search tree guided by simulation outcomes
        - balances exploration and exploitation
    - **algorithm**: __MCTS algorithm__

    - Output of MCTS
        - after many simulations, select at the root: the action with the **highest visit count**, or the action with the **highest mean value**
    - Key properties
        - combines: search (MCTS) and learning (policy and value networks)
        - focuses exploration using learned priors
        - foundation of modern game-playing AI
        (e.g. :contentReference[oaicite:0]{index=0}, MuZero)

- **MCTS algorithm**

    - **Selection**
        - start from the root node
        - recursively select child nodes using a tree policy
        - continue until a node is reached that: is not fully expanded, or is terminal

    - **UCT upper confidence bound (classical selection rule)**: $$ a^*=\arg\max_a\left(\frac{W(s,a)}{N(s,a)}+c \sqrt{\frac{\ln N(s)}{N(s,a)}}\right)$$
        where:  
        - $N(s)$: number of visits to state $s$
        - $N(s,a)$: number of times action $a$ was selected in $s$
        - $W(s,a)$: cumulative reward after selecting $a$ in $s$
        - $c$: exploration constant

    - **Expansion**: if the selected node is non-terminal and not fully expanded:
        - choose one untried action
        - add a new child node corresponding to this action
    - **Simulation (Rollout)**
        - from the newly expanded node:
        - simulate a trajectory until a terminal state or depth limit
        - use a default (often random or heuristic) policy
        - obtain a return $z$ (e.g. win/loss or cumulative reward)

    - **Backpropagation**
        - propagate the simulation result $z$ back along the selected path
        - update statistics for each visited node (or edge): visit counts or cumulative rewards
        - in two-player zero-sum games: alternate the sign of $z$ when moving up the tree
    - **recursion**: repeat this loop from many simulations


- **PUCT**
    - **full name**:  Policy-guided MCTS (AlphaZero-style)
    - **motivation**
        - pure UCT explores uniformly at the start
        - neural networks can provide strong **prior knowledge**
        - PUCT incorporates a learned **policy prior** into selection

    - **neural network outputs**
        - $P(s,a)$: prior probability of action $a$ in state $s$
        - $V(s)$: value estimate of state $s$

    - **PUCT selection rule**
        - formula: $$ a^*=\arg\max_a\left(Q(s,a)+c_{\text{puct}} \,P(s,a)\frac{\sqrt{N(s)}}{1 + N(s,a)}\right)$$

        where:
        - $Q(s,a) = \frac{W(s,a)}{N(s,a)}$: mean action value
        - $P(s,a)$: policy prior from the neural network
        - $N(s)$: visit count of state $s$
        - $N(s,a)$: visit count of action $a$
        - $c_{\text{puct}}$: exploration strength

    - **leaf evaluation**
        - instead of a rollout use the value network $V(s)$
        - this value is backpropagated through the tree

