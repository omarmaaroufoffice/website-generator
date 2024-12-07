from openai import OpenAI
import os
from dotenv import load_dotenv

class OpenAIClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Debug print (remove in production)
        print(f"API key loaded: {api_key[:10]}...")
            
        self.client = OpenAI(api_key=api_key)
    
    def generate_completion(self, prompt, model="gpt-4", temperature=0.7):
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in generate_completion: {str(e)}")
            raise 