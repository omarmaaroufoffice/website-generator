import os

class ContentHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_content(self, site_dir, site_config):
        """Generate website content"""
        if site_config.get('content_pages'):
            self._generate_content_pages(site_dir, site_config['content_pages'])
        
        if site_config.get('blog_posts'):
            self._generate_blog_posts(site_dir, site_config['blog_posts'])

    def _generate_content_pages(self, site_dir, content_pages):
        """Generate content for static pages"""
        content_dir = os.path.join(site_dir, 'content')
        for page in content_pages:
            self._generate_page_content(content_dir, page)

    def _generate_page_content(self, content_dir, page_config):
        """Generate content for a single page"""
        prompt = self._create_content_prompt(page_config)
        content = self.openai_client.generate_completion(prompt)
        
        file_path = os.path.join(content_dir, f"{page_config['name']}.html")
        with open(file_path, 'w') as f:
            f.write(content) 