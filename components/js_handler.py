import os
import re

class JSHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_scripts(self, site_dir, site_config):
        """Generate JavaScript files for the website"""
        js_dir = os.path.join(site_dir, 'js')
        os.makedirs(js_dir, exist_ok=True)
        
        prompt = self._create_js_prompt(site_config)
        js_content = self.openai_client.generate_completion(prompt)
        
        # Post-process the content
        cleaned_content = self._clean_generated_content(js_content)
        
        file_path = os.path.join(js_dir, 'main.js')
        with open(file_path, 'w') as f:
            f.write(cleaned_content)

    def _clean_generated_content(self, content):
        """Clean up AI-generated content by removing markdown code blocks and language indicators"""
        # Find content between first set of ``` markers
        pattern = r'```(?:javascript\n|js\n|\n)?(.+?)```'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = match.group(1)
        
        # Remove any "Here's the JavaScript:" or similar prefixes
        content = re.sub(r'^.*?\/\/ ', '// ', content, flags=re.DOTALL)
        
        return content.strip()

    def _create_js_prompt(self, site_config):
        """Create prompt for JavaScript generation"""
        return f"Generate JavaScript code for website with these requirements: {site_config}"