# Reasoning in LLMs (e.g., GPT)

## What does “reasoning” mean here?
- **Reasoning**: producing an answer that is **coherent**, **consistent with the prompt**, and often **step-by-step justified**.
- A practical question in evaluation is: **How do we decide whether a text is coherent and logically acceptable?**
  - internal consistency (no contradictions)
  - correct use of facts (when required)
  - valid intermediate steps (for math/logic)
  - alignment with the task (answering *the asked question*)

---

## Memory and “what the model knows”
- In a strict sense, the model has **no long-term memory** inside a single forward pass.
- What it *does* have:
  - **patterns learned during training** (statistical regularities in language and reasoning-like structures)
  - a **working context window** during inference (the prompt + generated tokens)
- This means:
  - It can appear “knowledgeable” because it learned many patterns.
  - It can appear “forgetful” because it cannot recall things not present in the context and does not store new memories by default.

---

## Inferring context from the prompt
- LLMs **infer the situation** from the user’s question:
  - topic domain (math, programming, medicine, etc.)
  - expected style (short answer, explanation, formal tone)
  - hidden assumptions (what is likely meant)
- This “context inference” is often the main driver of whether the response feels intelligent.

---

## Chain-of-Thought (CoT) prompting
- **Chain-of-Thought prompting** encourages the model to solve a problem by:
  - breaking it into smaller subproblems
  - producing intermediate steps
  - then giving the final answer
- Example (mental arithmetic):
  - $12 \times 14 = 12 \times (10 + 4) = 12 \times 10 + 12 \times 4 = 120 + 48 = 168$
- Why CoT helps:
  - intermediate steps reduce the chance of “jumping” to a wrong conclusion
  - it makes the process more inspectable for humans
- Caution:
  - CoT can produce **plausible but incorrect** steps (“confident nonsense”)
  - the steps are not guaranteed to reflect a true internal logical proof

---

## Self-consistency
- **Self-consistency**: run multiple reasoning attempts (often via sampling) and check whether:
  - the answers converge to the same result
  - the most frequent answer is selected
- Intuition:
  - if independent reasoning paths agree, the result is more reliable
- Limitation:
  - if the model is biased toward a common mistake, self-consistency may reinforce the wrong answer.

---

## Web search and tool use
- LLMs may use **web search** or external tools to incorporate:
  - up-to-date facts (news, prices, laws, leadership changes)
  - verifiable sources
- This shifts the system from “pattern-only” to **retrieval + reasoning**, improving factuality.
- Important distinction:
  - the model can still misinterpret sources; tools reduce but do not eliminate errors.

---

## “Not real logic” and understanding
- LLMs do not “understand” in the human sense:
  - they generate text by predicting likely next tokens given context
  - they can simulate logical structure without having grounded meaning
- Consequences:
  - they can **hallucinate**: produce statements that sound coherent but are false
  - they may fail on tasks requiring strict symbolic guarantees



---

## Practical checklist for evaluating “reasoning quality”
- Does the output stay consistent with the question and given context?
- Are intermediate steps valid (for math/logic/code)?
- Does it contradict itself?
- Are factual claims supported (especially when web search is used)?
- If we re-run the reasoning (self-consistency), does the answer remain stable?
