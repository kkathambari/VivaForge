import os
import tempfile
import PyPDF2
import pdfplumber
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class RAGEngine:
    def __init__(self, persist_directory="./database/chroma_db"):
        self.persist_directory = persist_directory
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        # Using Gemini Embeddings to prevent Render Free Tier Memory Overload
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004", 
            google_api_key=os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY"))
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vectorstore = None

    def extract_text_from_pdf(self, file_path):
        text = ""
        # Use lightweight PyPDF2 to prevent Render memory crashes (OOM Killer)
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}")
        return text

    def extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def process_document(self, uploaded_file):
        """Processes the uploaded file and builds the vector DB."""
        # Create a temporary file since uploaded_file is a file-like object in Streamlit
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        ext = os.path.splitext(uploaded_file.name)[1].lower()
        text = ""
        if ext == ".pdf":
            text = self.extract_text_from_pdf(tmp_path)
        elif ext == ".docx":
            text = self.extract_text_from_docx(tmp_path)
        else:
            os.remove(tmp_path)
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
        
        os.remove(tmp_path)

        if not text.strip():
            raise ValueError("Could not extract text from the document.")

        # Chunk the text
        chunks = self.text_splitter.split_text(text)
        
        # Create and persist Vector DB
        self.vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return True

    def get_retriever(self):
        if self.vectorstore is None:
            # Try to load existing
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        return self.vectorstore.as_retriever(search_kwargs={"k": 5})

    def get_full_context(self):
        """Returns a concatenated string of some top chunks as general context for the LLM"""
        if self.vectorstore is None:
             self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        # Fetch a broad representation by doing a generic search, or simply returning all stored docs
        # Note: For large docs, we shouldn't return everything. We'll return top 10 chunks as context.
        docs = self.vectorstore.similarity_search("project architecture overview methodology results", k=10)
        return "\n\n".join([doc.page_content for doc in docs])
