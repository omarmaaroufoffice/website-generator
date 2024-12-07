"""
Website Generator

This program generates custom websites based on user requirements through an
interactive questionnaire system. It uses OpenAI's API for content generation
and creates a complete website structure.

Author: [Omar Maarouf]
Date: [2024-12-07]
"""

from components.site_generator import SiteGenerator
from components.question_handler import QuestionHandler
from utils.openai_client import OpenAIClient
import os
from dotenv import load_dotenv

def main():
    """
    Main function that orchestrates the website generation process.
    
    The function performs the following steps:
    1. Loads environment variables
    2. Initializes necessary components
    3. Collects user requirements through questions
    4. Generates the website based on collected configuration
    """
    # Debug: Print environment variables
    load_dotenv()
    print(f"Environment variables loaded: {os.environ.get('OPENAI_API_KEY', 'Not found')[:10]}...")

    # Initialize components
    openai_client = OpenAIClient()
    question_handler = QuestionHandler(openai_client)
    site_generator = SiteGenerator(openai_client)

    # Get website requirements and configuration
    questions = question_handler.get_questions()
    answers = question_handler.collect_answers(questions)
    site_config = question_handler.extract_site_config(answers)
    
    # Generate the complete website
    site_generator.generate_site(site_config)
    
    print(f"Website generated in directory: {site_config['site_dir']}\nOpen index.html in your browser to view the site.")

if __name__ == "__main__":
    main()
