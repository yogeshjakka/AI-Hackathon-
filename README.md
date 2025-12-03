<div align="center">
  <h1>H-002 | Customer Experience Automation</h1>
 </div>
 
> Hyper-Personalized Customer Support Agent (Conversational AI + RAG).

1\. The Problem (Real World Scenario)
-------------------------------------

**Context:** During my exploration of Conversational AI systems used in retail and e-commerce, I noticed a big limitation: most chatbots fail when users speak vaguely or expect hyper-specific help. Real customers rarely type perfect queries; they say things like “I’m cold”, “Where’s my order?”, or “Something’s wrong with my item.”

**The Pain Point:** Traditional chatbots rely on static FAQ flows. They cannot understand real-time context such as user location, past orders, or store inventory. As a result:
*    Users receive generic responses
*    Conversion rates drop
*    Support becomes slow and frustrating

> **My Solution:** I built a Hyper-Personalized Customer Support Agent, a context-aware conversational AI system. It understands vague messages, reads internal documents via RAG, fetches real-time data from APIs, and returns personalized, actionable replies — all while masking PII to maintain privacy.

2\. Expected End Result
-----------------------

For the User:

 *   Input: incomplete message such as:
    “I’m cold.”
    or
    “Is this item available near me?”

*   Action: The AI automatically uses:
    *  Location context
    *  Order history
    *  Store inventory APIs
    *  Internal policy documents (via RAG)
 
*   Output: A hyper-specific, instant recommendation. For example:
    *  “There’s a Starbucks 50m from your location. Hot Cocoa is in stock, and you have a 10% coupon available.”

3\. Technical Approach
----------------------


I challenged myself to move beyond simple chatbots and create a production-grade, context-aware AI system with multiple moving components.

**System Architecture:**

1. **Event-Driven Context Collection:** The system dynamically collects user metadata such as location, recent purchases, and device type. Nothing is stored permanently — only session-based.
 
2. **RAG Pipeline (Retrieval-Augmented Generation):** I built a document ingestion flow that takes internal PDFs/policies, converts them into embeddings, and stores them in a vector database. During a query, only relevant chunks are retrieved to ground the AI’s answer.
  
3. **Reasoning Layer:** 
    *  RAG output
    *  User context
    *  Real-time API results

    
4. **Real-Time Decision Engine:**
    *  Inventory API → “Is this item in stock?”
    *  Store Locator → “Where’s the nearest place?”
    *  Coupon Engine → “Do I have an active offer?”
    *  Order API → “Where is my package now?”

5. **Privacy Guardrail:** Before anything is sent to the LLM, all PII (emails, phone numbers, addresses) is automatically masked using a redaction pipeline.


4\. Tech Stack
--------------


*  Language: Python 3.11
*  AI Engine: OpenAI / Gemini / Llama (model-agnostic architecture)

*  RAG Layer: FAISS / Pinecone vector store

*  Embedding Models: Sentence-Transformers

*  Backend: FastAPI

*  NER for PII Masking: spaCy

*  Database: Redis (for session context) + MongoDB/PostgreSQL (for user and order data)

*  Tool Layer:
   *  Store Inventory API
   *  Coupon Service
   *  Geolocation/Distance Calculator


5\. Challenges & Learnings
--------------------------


_This project wasn't easy. Here are two major hurdles I overcame:_

**Challenge 1: Interpreting Vague Human Inputs**

*   **Issue:** The model initially struggled with queries like “I’m cold” or “It’s too bright here.” It lacked context.
    
*   **Solution:** I built a Context Fusion Layer where metadata (location, history, store hours) is attached to every prompt before inference. This turned vague messages into actionable insights.
    

**Challenge 2: Real-Time API Reliability**

*   **Issue:** Inventory APIs sometimes lag.
    
*   **Solution:** Caching + fallback responses ensured smoother performance.
    

6\. Visual Proof
----------------


Architecture Diagram



7\. How to Run
--------------

**Clone Repo**
```bash
git clone https://github.com/yogeshjakka/AI-Hackathon-.git
cd AI-Hackathon-
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```


