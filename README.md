# 🎓 ProjectViva: AI Mock Viva Examiner & Tutor

ProjectViva is an advanced, memory-optimized AI chatbot designed to help students prepare for their project viva examinations. By leveraging Retrieval-Augmented Generation (RAG) and the Gemini API, the chatbot mathematically analyzes uploaded project documents to conduct realistic technical viva sessions and act as an intelligent project tutor.

## 🚀 Key Features

* **Dual Modes of Operation:**
  * **📖 Learn Mode:** Functions as an intelligent tutor. Students can ask questions about their project, and the bot provides accurate answers strictly based on the uploaded documentation.
  * **🎯 Test Mode:** Simulates a real viva examination. The bot assumes a role (e.g., External Examiner), asks targeted questions, evaluates student responses, and dynamically generates follow-up questions based on the chat history.
* **Serverless RAG Engine:** To prevent Out-Of-Memory (OOM) crashes on free-tier cloud hosting (like Render), ProjectViva completely bypasses heavy vector databases (like ChromaDB). Instead, it uses a lightweight, in-memory **BM25 Keyword Retrieval Algorithm** combined with `PyPDF2`, ensuring lightning-fast processing with almost zero RAM footprint.
* **Dynamic Evaluation:** Analyzes the entire viva session to generate a comprehensive "Readiness Report," scoring the student based on relevance, technical depth, completeness, and confidence, while highlighting strong/weak areas.
* **Customizable Settings:** Allows users to select the Examiner Role (Teacher, External Examiner, Industry Interviewer) and adjust the Difficulty Level (Easy, Medium, Hard, Expert).

## 🏗️ System Architecture

1. **Document Upload:** User uploads a PDF or DOCX report via the Streamlit interface (capped at 10MB to protect server memory).
2. **Memory-Safe Extraction:** Content is parsed using lightweight libraries (`PyPDF2` or `python-docx`) to prevent cloud server crashes.
3. **BM25 Indexing:** Text is split into mathematical chunks using Langchain and indexed into an in-memory BM25 Retriever. This eliminates the need for expensive third-party embedding APIs and heavy SQL databases.
4. **Retrieval-Augmented Generation (RAG):** When interacting, the BM25 algorithm retrieves the most statistically relevant document chunks to provide context to the LLM.
5. **LLM Generation:** `Gemini 2.5 Flash` generates examiner questions, tutor answers, or evaluation reports based on the retrieved context and conversational history.

## 🛠️ Technology Stack

* **Frontend & Backend UI:** Streamlit (Python)
* **LLM / AI:** Google Gemini 2.5 Flash API
* **RAG Framework:** LangChain
* **Retrieval Algorithm:** BM25 (rank_bm25)
* **Document Parsers:** PyPDF2, python-docx
* **Hosting:** Render (Web Service)

## 📂 Folder Structure

```text
ProjectViva/
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API Key)
│
├── .streamlit/
│   └── config.toml            # Server limits (10MB upload max)
│
├── chatbot/
│   ├── rag_engine.py          # Handles document parsing and BM25 logic
│   ├── viva_generator.py      # LLM logic for generating questions & tutor answers
│   ├── evaluator.py           # LLM logic for generating readiness reports
│
└── prompts/
    ├── viva_prompt.txt        # Prompt template for Test Mode
    ├── qa_prompt.txt          # Prompt template for Learn Mode
    └── evaluator_prompt.txt   # Prompt template for Readiness Report
```

## ⚙️ Local Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/kkathambari/VivaForge.git
cd VivaForge
```

**2. Create a Virtual Environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up the API Key**
Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_api_key_here
```

**5. Run the Application**
```bash
streamlit run app.py
```

## ☁️ Cloud Deployment (Render)

ProjectViva is heavily optimized for Render's free tier.
1. Create a New Web Service on Render linked to your GitHub repo.
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `streamlit run app.py --server.port $PORT --server.enableCORS false --server.enableXsrfProtection false`
4. **Environment Variables:** Add `GEMINI_API_KEY` to your Render dashboard.
5. Deploy!

## 📝 Usage Guide

1. **Upload Document:** Open the app and upload your project report from the sidebar. Click "Process Document" to build the knowledge base.
2. **Select Mode:** Choose between *Learn Mode* and *Test Mode*.
3. **Learn Mode:** Type any question regarding your project to get an instant, context-aware answer.
4. **Test Mode:** Configure the examiner role and difficulty, then click "Start/Restart Viva". Answer the questions posed by the AI. When finished, click "End Viva & Evaluate" to receive your final Readiness Report.
