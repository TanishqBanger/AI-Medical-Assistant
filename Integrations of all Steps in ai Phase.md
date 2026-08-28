# **Integrations of all Steps in Phase 3(AI Phase)**



#### **Step 1: LLM Integration is successfully completed. ✅**

User

&#x20; ↓

Railway

&#x20; ↓

FastAPI

&#x20; ↓

backend/ai/llm.py

&#x20; ↓

OpenAI API

&#x20; ↓

GPT-5.6 Luna

&#x20; ↓

AI response







### **step 2: prompts**

### 

###### **Architecture -----**



User Request

&#x20;    │

&#x20;    ▼

FastAPI (endpoint)

&#x20;    │

&#x20;    ▼

Orchestrator

&#x20;    │

&#x20;    ├───────────────► RAG

&#x20;    │                  │

&#x20;    │                  ▼

&#x20;    │             Hospital Context

&#x20;    │

&#x20;    ├───────────────► Memory

&#x20;    │                  │

&#x20;    │                  ▼

&#x20;    │             Conversation History

&#x20;    │

&#x20;    ▼

prompts.py

&#x20;    │

&#x20;    ├── System instructions

&#x20;    ├── User question

&#x20;    ├── Hospital context

&#x20;    ├── Conversation history

&#x20;    └── Task-specific instructions

&#x20;    │

&#x20;    ▼

Final Prompt

&#x20;    │

&#x20;    ▼

llm.py

&#x20;    │

&#x20;    ▼

OpenAI API

&#x20;    │

&#x20;    ▼

GPT-5.6

&#x20;    │

&#x20;    ▼

Response







### **use of prompts**



User:

"What are the hospital visiting hours?"

&#x20;       ↓

Orchestrator

&#x20;       ↓

RAG finds:

"Visiting hours are 4 PM – 7 PM."

&#x20;       ↓

prompts.py

&#x20;       ↓

Creates instructions:

"Answer using the hospital context.

Be concise.

Don't invent information."

&#x20;       ↓

llm.py

&#x20;       ↓

GPT

&#x20;       ↓

"Hospital visiting hours are 4 PM to 7 PM."





### **Step 3: rag**



&#x20;                        **USER**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                   **┌──────────────┐**

&#x20;                   **│   FastAPI    │**

&#x20;                   **│   app.py     │**

&#x20;                   **└──────┬───────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌──────────────────┐**

&#x20;                 **│  orchestrator.py │**

&#x20;                 **└────────┬─────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                    **┌───────────┐**

&#x20;                    **│   rag.py  │**

&#x20;                    **└─────┬─────┘**

&#x20;                          **│**

&#x20;                   **User Question**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌─────────────────┐**

&#x20;                 **│ Document Search │**

&#x20;                 **└────────┬────────┘**

&#x20;                          **│**

&#x20;             **┌────────────┴────────────┐**

&#x20;             **▼                         ▼**

&#x20;     **hospital\_faqs.csv       hospital\_policies.csv**

&#x20;             **│                         │**

&#x20;             **└────────────┬────────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                **Relevant Documents**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌────────────────┐**

&#x20;                 **│   prompts.py   │**

&#x20;                 **│ Build Context  │**

&#x20;                 **└───────┬────────┘**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                      **llm.py**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                   **OpenAI API**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                      **Luna**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                   **Final Answer**





### **retrieval pipeline**



**User Question**

&#x20;     **│**

&#x20;     **▼**

**TF-IDF Vectorization**

&#x20;     **│**

&#x20;     **▼**

**Cosine Similarity**

&#x20;     **│**

&#x20;     **▼**

**Rank Hospital Documents**

&#x20;     **│**

&#x20;     **▼**

**Top 5 Results**





##### **rag.py   → "What hospital information is relevant?"**

##### **prompts.py → "How should we present that information to Luna?"**

##### **llm.py   → "Send it to the LLM."**









### **After adding Vector Database**



&#x20;                        **USER**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                   **┌──────────────┐**

&#x20;                   **│   FastAPI    │**

&#x20;                   **│   app.py     │**

&#x20;                   **└──────┬───────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌──────────────────┐**

&#x20;                 **│  orchestrator.py │**

&#x20;                 **└────────┬─────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                    **┌───────────┐**

&#x20;                    **│   rag.py  │**

&#x20;                    **└─────┬─────┘**

&#x20;                          **│**

&#x20;                   **User Question**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                   **┌─────────────┐**

&#x20;                   **│   Embedding │**

&#x20;                   **└──────┬──────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                **┌────────────────────┐**

&#x20;                **│   Vector Database  │**

&#x20;                **│                    │**

&#x20;                **│ FAQ Embeddings     │**

&#x20;                **│ Policy Embeddings  │**

&#x20;                **└─────────┬──────────┘**

&#x20;                          **│**

&#x20;                   **Similarity Search**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **Relevant Documents**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌────────────────┐**

&#x20;                 **│   prompts.py   │**

&#x20;                 **│ Build Context  │**

&#x20;                 **└───────┬────────┘**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                      **llm.py**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                   **OpenAI API**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                      **Luna**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                   **Final Answer**





### **Chroma db flow creation**





**hospital\_faqs.csv**

&#x20;      **│**

&#x20;      **│**

**hospital\_policies.csv**

&#x20;      **│**

&#x20;      **▼**

&#x20;   **ingest.py**

&#x20;      **│**

&#x20;      **▼**

&#x20;**Read + Combine**

&#x20;**question + answer**

&#x20;      **│**

&#x20;      **▼**

&#x20; **embeddings.py**

&#x20;      **│**

&#x20;      **▼**

&#x20; **1536-dimensional**

&#x20;   **embedding**

&#x20;      **│**

&#x20;      **▼**

&#x20;   **ChromaDB**

&#x20;      **│**

&#x20;      **▼**

&#x20;**backend/vectorstore/chroma\_db/**

&#x20;      **│**

&#x20;      **▼**

&#x20;**ID + Document**

&#x20;**Embedding + Metadata**







# **New architecture after integrating chroma db**



&#x20;                        **USER**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                   **┌──────────────┐**

&#x20;                   **│   FastAPI    │**

&#x20;                   **│   app.py     │**

&#x20;                   **└──────┬───────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌──────────────────┐**

&#x20;                 **│  orchestrator.py │**

&#x20;                 **└────────┬─────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                    **┌───────────┐**

&#x20;                    **│   rag.py  │**

&#x20;                    **└─────┬─────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌─────────────────┐**

&#x20;                 **│ Query Embedding │**

&#x20;                 **└────────┬────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌─────────────────┐**

&#x20;                 **│    ChromaDB     │**

&#x20;                 **│                 │**

&#x20;                 **│ 75 Documents    │**

&#x20;                 **└────────┬────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌─────────────────┐**

&#x20;                 **│ Relevant Chunks │**

&#x20;                 **└────────┬────────┘**

&#x20;                          **│**

&#x20;                          **▼**

&#x20;                 **┌────────────────┐**

&#x20;                 **│   prompts.py   │**

&#x20;                 **└───────┬────────┘**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                      **llm.py**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                   **OpenAI API**

&#x20;                         **│**

&#x20;                         **▼**

&#x20;                      **Luna**

