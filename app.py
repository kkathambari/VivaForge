import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from chatbot.rag_engine import RAGEngine
from chatbot.viva_generator import VivaGenerator
from chatbot.evaluator import Evaluator

# --- Page Config ---
st.set_page_config(page_title="ProjectViva", page_icon="🎓", layout="wide")
st.title("🎓 ProjectViva: AI Mock Viva Examiner")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False
if "context" not in st.session_state:
    st.session_state.context = ""
if "viva_started" not in st.session_state:
    st.session_state.viva_started = False

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Input (Fallback if not in .env)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input("Gemini API Key", type="password")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            
    st.subheader("1. Upload Project Report")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    
    if uploaded_file and not st.session_state.document_processed:
        if st.button("Process Document"):
            with st.spinner("Processing document & building knowledge base..."):
                try:
                    rag_engine = RAGEngine()
                    rag_engine.process_document(uploaded_file)
                    st.session_state.context = rag_engine.get_full_context()
                    st.session_state.document_processed = True
                    st.success("Knowledge Base Built Successfully!")
                except Exception as e:
                    st.error(f"Error processing document: {e}")

    st.subheader("2. Viva Settings")
    role = st.selectbox("Role", ["Teacher", "External Examiner", "Industry Interviewer", "Research Reviewer"])
    difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard", "Expert"], value="Medium")
    
    st.subheader("3. Session Controls")
    if st.button("Start / Restart Viva"):
        if not st.session_state.document_processed:
            st.warning("Please upload and process a document first.")
        elif not os.getenv("GEMINI_API_KEY"):
             st.warning("Please provide a Gemini API Key.")
        else:
            st.session_state.chat_history = []
            st.session_state.viva_started = True
            
            # Generate the first question
            with st.spinner("Generating first question..."):
                try:
                    generator = VivaGenerator()
                    first_q = generator.generate_question(
                        role=role, 
                        difficulty=difficulty, 
                        context=st.session_state.context, 
                        history="[Viva Started. Ask the first basic question.]"
                    )
                    st.session_state.chat_history.append({"role": "examiner", "content": first_q})
                except Exception as e:
                    st.error(f"Error generating question: {e}")
                    
    if st.button("End Viva & Evaluate"):
        if len(st.session_state.chat_history) < 2:
            st.warning("Not enough interaction to evaluate.")
        else:
            with st.spinner("Generating Readiness Report..."):
                try:
                    evaluator = Evaluator()
                    # Format history for evaluator
                    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
                    report = evaluator.evaluate_session(st.session_state.context, history_text)
                    st.session_state.chat_history.append({"role": "evaluator", "content": report})
                    st.session_state.viva_started = False
                except Exception as e:
                    st.error(f"Error generating report: {e}")

# --- Main Chat Interface ---
if not st.session_state.document_processed:
    st.info("👈 Please upload your project report from the sidebar to begin.")
elif not st.session_state.viva_started and len(st.session_state.chat_history) == 0:
    st.info("👈 Document processed! Click 'Start / Restart Viva' in the sidebar.")
else:
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "examiner":
            with st.chat_message("assistant", avatar="🧑‍🏫"):
                st.write(msg["content"])
        elif msg["role"] == "student":
            with st.chat_message("user", avatar="🎓"):
                st.write(msg["content"])
        elif msg["role"] == "evaluator":
            st.markdown("---")
            st.markdown("## 📊 Final Readiness Report")
            st.markdown(msg["content"])

    # User input
    if st.session_state.viva_started:
        student_input = st.chat_input("Type your answer here...")
        if student_input:
            # 1. Display student message
            st.session_state.chat_history.append({"role": "student", "content": student_input})
            with st.chat_message("user", avatar="🎓"):
                st.write(student_input)
                
            # 2. Generate examiner response/next question
            with st.chat_message("assistant", avatar="🧑‍🏫"):
                with st.spinner("Thinking..."):
                    try:
                        # Build history string
                        history_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history])
                        
                        generator = VivaGenerator()
                        next_q = generator.generate_question(
                            role=role,
                            difficulty=difficulty,
                            context=st.session_state.context,
                            history=history_text
                        )
                        st.write(next_q)
                        st.session_state.chat_history.append({"role": "examiner", "content": next_q})
                    except Exception as e:
                        st.error(f"Error: {e}")
