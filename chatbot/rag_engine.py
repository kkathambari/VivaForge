import os
import tempfile
import PyPDF2
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

class RAGEngine:
    def __init__(self, persist_directory="./database/chroma_db"):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.retriever = None
        self.docs = []

    def extract_text_from_pdf(self, file_path):
        text = ""
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
        """Processes the uploaded file and builds the BM25 Retriever."""
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
        
        # Create BM25 Retriever (Zero API calls, Zero memory bloat)
        self.docs = [Document(page_content=chunk) for chunk in chunks]
        self.retriever = BM25Retriever.from_documents(self.docs)
        self.retriever.k = 5
        return True

    def get_retriever(self):
        if self.retriever is None:
            raise ValueError("Document not processed yet.")
        return self.retriever

    def get_full_context(self):
        """Returns a concatenated string of some top chunks as general context for the LLM"""
        if not self.docs:
            return ""
        # Return top 10 chunks as context
        return "\n\n".join([doc.page_content for doc in self.docs[:10]])
