class QuestionHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.default_questions = [
            "What is the name of your website?",
            "What is the main purpose of your website?",
            "What pages do you want in your website?",
            "What color scheme would you prefer?",
            "Do you have any specific design preferences?"
        ]

    def get_questions(self):
        """Return the list of questions to ask the user"""
        return self.default_questions

    def collect_answers(self, questions):
        """Collect answers from the user for each question"""
        answers = {}
        print("\nPlease answer the following questions about your website:")
        for question in questions:
            answer = input(f"\n{question}\n> ")
            answers[question] = answer
        return answers

    def extract_site_config(self, answers):
        """Convert user answers into a site configuration dictionary"""
        site_name = answers.get("What is the name of your website?", "My Website")
        site_dir = site_name.lower().replace(" ", "_")

        # Create basic site configuration
        site_config = {
            'site_name': site_name,
            'site_dir': site_dir,
            'pages': ['index'],  # Always include index page
            'color_scheme': {},
            'design_preferences': []
        }

        # Extract pages from answers
        if "What pages do you want in your website?" in answers:
            pages = answers["What pages do you want in your website?"].lower().split(",")
            pages = [page.strip() for page in pages]
            if 'index' not in pages:
                pages.insert(0, 'index')
            site_config['pages'] = pages

        # Extract color scheme
        if "What color scheme would you prefer?" in answers:
            color_scheme = answers["What color scheme would you prefer?"]
            # Here you could add logic to parse color schemes
            site_config['color_scheme'] = {'primary': color_scheme}

        # Extract design preferences
        if "Do you have any specific design preferences?" in answers:
            preferences = answers["Do you have any specific design preferences?"].split(",")
            site_config['design_preferences'] = [pref.strip() for pref in preferences]

        # Add purpose to configuration
        if "What is the main purpose of your website?" in answers:
            site_config['purpose'] = answers["What is the main purpose of your website?"]

        return site_config

    def _create_prompt(self, answers):
        """Create a prompt for AI based on user answers"""
        prompt = "Create a website with the following specifications:\n"
        for question, answer in answers.items():
            prompt += f"- {question}: {answer}\n"
        return prompt 