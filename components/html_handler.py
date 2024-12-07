import os
import re

class HTMLHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_pages(self, site_dir, site_config):
        """Generate all HTML pages for the website"""
        pages = site_config.get('pages', ['index'])
        
        for page in pages:
            self._generate_page(page, site_dir, site_config)

    def _generate_page(self, page_name, site_dir, site_config):
        """Generate a single HTML page"""
        prompt = self._create_html_prompt(page_name, site_config)
        html_content = self.openai_client.generate_completion(prompt)
        
        # Post-process the content
        cleaned_content = self._clean_generated_content(html_content)
        
        file_path = os.path.join(site_dir, f"{page_name}.html")
        with open(file_path, 'w') as f:
            f.write(cleaned_content)

    def _clean_generated_content(self, content):
        """Clean up AI-generated content by removing markdown code blocks and language indicators"""
        # Find content between first set of ``` markers
        pattern = r'```(?:html\n|\n)?(.+?)```'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = match.group(1)
        
        # Remove any "Here's the HTML:" or similar prefixes
        content = re.sub(r'^.*?<!DOCTYPE', '<!DOCTYPE', content, flags=re.DOTALL)
        
        return content.strip()

    def _create_html_prompt(self, page_name, site_config):
        """Create prompt for HTML generation with proper paths"""
        return f"""Generate HTML for {page_name} page with these requirements: {site_config}
        Use these paths in your HTML:
        - CSS files should be referenced as: {site_config['css_path']}/main.css
        - JavaScript files should be referenced as: {site_config['js_path']}/main.js
        - Images should be referenced from: {site_config['images_path']}/
        """