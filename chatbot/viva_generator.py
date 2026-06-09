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
        
        # Load the prompt template
        prompt_path = os.path.join("prompts", "viva_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def generate_question(self, role, difficulty, context, history):
        """Generates the next viva question based on context and history."""
        prompt = PromptTemplate(
            input_variables=["role", "difficulty", "context", "history"],
            template=self.prompt_template
        )
        
        formatted_prompt = prompt.format(
            role=role,
            difficulty=difficulty,
            context=context,
            history=history
        )
        
        response = self.llm.invoke(formatted_prompt)
        return response.content
