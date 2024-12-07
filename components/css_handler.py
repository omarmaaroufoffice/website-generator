import os
import re

class CSSHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_styles(self, site_dir, site_config):
        """Generate CSS files for the website"""
        css_dir = os.path.join(site_dir, 'css')
        os.makedirs(css_dir, exist_ok=True)
        
        prompt = self._create_css_prompt(site_config)
        css_content = self.openai_client.generate_completion(prompt)
        
        # Post-process the content
        cleaned_content = self._clean_generated_content(css_content)
        
        file_path = os.path.join(css_dir, 'main.css')
        with open(file_path, 'w') as f:
            f.write(cleaned_content)

    def _clean_generated_content(self, content):
        """Clean up AI-generated content by removing markdown code blocks and language indicators"""
        # Find content between first set of ``` markers
        pattern = r'```(?:css\n|\n)?(.+?)```'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = match.group(1)
        
        # Remove any "Here's the CSS:" or similar prefixes
        content = re.sub(r'^.*?/\*', '/*', content, flags=re.DOTALL)
        
        return content.strip()

    def _create_css_prompt(self, site_config):
        """Create prompt for CSS generation"""
        return f"Generate CSS styles for website with these requirements: {site_config}"