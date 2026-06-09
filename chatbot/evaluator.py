import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class Evaluator:
    def __init__(self):
        # Using Gemini 2.5 Flash
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
            
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2 # Lower temperature for more objective evaluation
        )
        
        prompt_path = os.path.join("prompts", "evaluator_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def evaluate_session(self, context, history):
        """Evaluates the entire viva session and returns a readiness report."""
        prompt = PromptTemplate(
            input_variables=["context", "history"],
            template=self.prompt_template
        )
        
        formatted_prompt = prompt.format(
            context=context,
            history=history
        )
        
        response = self.llm.invoke(formatted_prompt)
        return response.content
