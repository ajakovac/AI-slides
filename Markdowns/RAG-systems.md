- **RAG**
    - **full name**: Retrieval-Augmented Generation
    - **motivation**
        - large language models store knowledge implicitly in parameters
    - **parameters are**
        - expensive to retrain
        - static (can become outdated)
        - limited in capacity and traceability
    - need a way to **access external, up-to-date information**

    - **core idea**
        - combine retrieval from an external knowledge source and generation using a language model
        - generation is conditioned on retrieved documents, not only on the prompt
        - __RAG architecture__


    - **knowledge source**
        - documents, PDFs, markdown files
        - databases, APIs, logs
        - domain-specific corpora
        - vector databases (embeddings)

    - **key advantages**
        - reduces hallucination
        - enables factual grounding
        - allows easy knowledge updates without retraining
        - improves transparency and controllability

    - **limitations**
        - quality depends on retrieval accuracy
        - context window limits how much can be injected
        - retrieval errors propagate to generation
        - system complexity higher than pure LLMs

    - **typical applications**
        - question answering over private documents
        - enterprise knowledge assistants
        - technical documentation search
        - scientific and legal assistants
        - code and API help systems

    - **conceptual view**
        - LLM = reasoning and language engine
        - retriever = external memory
        - RAG = **LLM + searchable knowledge**

- **RAG architecture**
    - **query encoding**
        - user query is converted into a vector representation
    - **retrieval**
        - relevant documents are fetched from a database
        - typically using vector similarity search
    - **augmentation**
        - retrieved texts are appended to the prompt
    - **generation**
        - language model generates an answer grounded in retrieved content
