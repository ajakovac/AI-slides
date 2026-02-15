<a id="attention-mechanisms-and-transformers"></a>
## Attention mechanisms and transformers
- motivation
	- classical sequence models (e.g. RNNs) process text sequentially
	- long-range dependencies are difficult to capture
	- information from distant tokens tends to vanish or blur
- need for a mechanism that
	- accesses all tokens directly
	- adapts dynamically to the task
	- scales efficiently to long sequences
<a id="attention-mechanism"></a>
## attention mechanism
- core idea
	- each element of a sequence selectively focuses on other elements
	- relevance between tokens is learned, not predefined
	- context is computed as a weighted combination of all tokens
- steps
	- attention mechanism steps
- multi-head attention
	- use several $Q_i,K_i,V_i$ matrices $\text{head}_i=\text{attention}(Q_i,K_i,V_i)$, and $\text{head} = \text{Concat}(\text{head}_i,\dots,\text{head}_H)$
	- train a weight of these heads $W_O\in \mathbb R^{(Hd_k)\times d_{model} }$
	- mix information of the attention heads
	- map it into the embedding dimension of the model
	- formally: $$\text{Multihead}(Q,K,V) = \text{head} W_O$$
- each head specializes to different things
	- syntax
	- agreement
	- semantic roles
	- long-range coreference
	- together, they form a rich contextual representation.
- interpretation
	- attention builds a soft, learned dependency graph over tokens
	- each token dynamically decides which others matter
	- context is global and adaptive
- computational cost
	- $\mathcal O(T^2d_k)$
	- all token-token interaction
	- sequence length is limited (e.g. 512 in BERT, 8k-1M+ in modern LLMs )
	- long-context variants are actively researched
	- parallelizable (GPUs)