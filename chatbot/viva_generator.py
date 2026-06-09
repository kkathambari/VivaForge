import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class VivaGenerator:
    def __init__(self):
        # Using Gemini 2.5 Flash as requested
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
            
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Load the prompt templates
        viva_prompt_path = os.path.join("prompts", "viva_prompt.txt")
        with open(viva_prompt_path, "r", encoding="utf-8") as f:
            self.viva_prompt_template = f.read()

        qa_prompt_path = os.path.join("prompts", "qa_prompt.txt")
        with open(qa_prompt_path, "r", encoding="utf-8") as f:
            self.qa_prompt_template = f.read()

    def generate_question(self, role, difficulty, context, history):
        """Generates the next viva question based on context and history."""
        prompt = PromptTemplate(
            input_variables=["role", "difficulty", "context", "history"],
            template=self.viva_prompt_template
        )
        
        formatted_prompt = prompt.format(
            role=role,
            difficulty=difficulty,
            context=context,
            history=history
        )
        
        response = self.llm.invoke(formatted_prompt)
        return response.content

    def answer_student_question(self, context, history, question):
        """Answers a student's question based ONLY on the document context."""
        prompt = PromptTemplate(
            input_variables=["context", "history", "question"],
            template=self.qa_prompt_template
        )
        
        formatted_prompt = prompt.format(
            context=context,
            history=history,
            question=question
        )
        
        response = self.llm.invoke(formatted_prompt)
        return response.content
