# 🎓 VivaForge: AI Mock Viva Examiner & Tutor

ProjectViva is an advanced, conversational AI chatbot designed to help students prepare for their project viva examinations. By leveraging Retrieval-Augmented Generation (RAG) and the Gemini API, the chatbot analyzes uploaded project documents (PDF/DOCX) to conduct realistic technical viva sessions and act as an intelligent project tutor.

## 🚀 Key Features

* **Dual Modes of Operation:**
  * **📖 Learn Mode:** Functions as an intelligent tutor. Students can ask questions about their project, and the bot will provide accurate answers strictly based on the uploaded documentation.
  * **🎯 Test Mode:** Simulates a real viva examination. The bot asks targeted questions, evaluates student responses, and dynamically generates follow-up questions based on the chat history.
* **Document Parsing & RAG Engine:** Automatically extracts text from PDF and DOCX files, chunks the content, and stores it in a local ChromaDB vector database using `all-MiniLM-L6-v2` embeddings.
* **Dynamic Evaluation:** Analyzes the entire viva session to generate a comprehensive "Readiness Report," scoring the student based on relevance, technical depth, completeness, and confidence, while highlighting strong/weak areas.
* **Customizable Settings:** Allows users to select the Examiner Role (Teacher, External Examiner, Industry Interviewer) and adjust the Difficulty Level (Easy, Medium, Hard, Expert).

## 🏗️ System Architecture

1. **Document Upload:** User uploads a PDF or DOCX report via the Streamlit interface.
2. **Text Extraction:** Content is parsed using `pdfplumber`/`PyPDF2` or `python-docx`.
3. **Knowledge Base Generation:** Text is split into overlapping chunks and embedded using `Sentence Transformers`. The embeddings are stored in `ChromaDB`.
4. **Retrieval-Augmented Generation (RAG):** When interacting, the system retrieves the most relevant document chunks to provide context to the LLM.
5. **LLM Generation:** `Gemini 2.5 Flash` (via LangChain) generates examiner questions, tutor answers, or evaluation reports based on the retrieved context and session history.

## 🛠️ Technology Stack

* **Frontend & Backend UI:** Streamlit (Python)
* **LLM / AI:** Google Gemini 2.5 Flash API
* **RAG Framework:** LangChain
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Sentence Transformers)
* **Vector Database:** ChromaDB (Local Open-Source)
* **Document Parsers:** PyPDF2, pdfplumber, python-docx

## 📂 Folder Structure

```text
ProjectViva/
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API Key)
│
├── chatbot/
│   ├── rag_engine.py          # Handles document parsing and ChromaDB logic
│   ├── viva_generator.py      # LLM logic for generating questions & tutor answers
│   ├── evaluator.py           # LLM logic for generating readiness reports
│
├── database/
│   └── chroma_db/             # Local vector database storage
│
├── uploads/                   # Temporary file storage (if needed)
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
python -m streamlit run app.py
```

## 📝 Usage Guide

1. **Upload Document:** Open the app and upload your project report from the sidebar. Click "Process Document" to build the knowledge base.
2. **Select Mode:** Choose between *Learn Mode* and *Test Mode*.
3. **Learn Mode:** Type any question regarding your project to get an instant, context-aware answer.
4. **Test Mode:** Configure the examiner role and difficulty, then click "Start Viva". Answer the questions posed by the AI. When finished, click "End Viva & Evaluate" to receive your final Readiness Report.
