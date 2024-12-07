import os
import shutil
from components.html_handler import HTMLHandler
from components.css_handler import CSSHandler
from components.js_handler import JSHandler
from components.media_handler import MediaHandler

class SiteGenerator:
    def __init__(self, openai_client):
        self.html_handler = HTMLHandler(openai_client)
        self.css_handler = CSSHandler(openai_client)
        self.js_handler = JSHandler(openai_client)
        self.media_handler = MediaHandler(openai_client)

    def generate_site(self, site_config):
        """Generate the complete website with proper structure"""
        # Sanitize site directory name
        site_config['site_dir'] = self._sanitize_name(site_config['site_dir'])
        
        # Create main site directory
        site_dir = os.path.join(os.getcwd(), site_config['site_dir'])
        os.makedirs(site_dir, exist_ok=True)
        
        # Create necessary subdirectories
        self._create_directory_structure(site_dir)
        
        # Update site_config with proper paths
        site_config['css_path'] = 'assets/css'
        site_config['js_path'] = 'assets/js'
        site_config['images_path'] = 'assets/images'
        site_config['media_path'] = 'assets/media'
        
        # Sanitize page names
        if 'pages' in site_config:
            site_config['pages'] = [self._sanitize_name(page) for page in site_config['pages']]
        
        # Generate all components in correct order
        self.css_handler.generate_styles(site_dir, site_config)
        self.js_handler.generate_scripts(site_dir, site_config)
        self.media_handler.handle_media(site_dir, site_config)
        self.html_handler.generate_pages(site_dir, site_config)

        # Clean up and organize files
        self._organize_files(site_dir)
        
        # Verify file structure
        self._verify_structure(site_dir)

    def _create_directory_structure(self, site_dir):
        """Create a proper directory structure for the website"""
        directories = [
            'assets/css',
            'assets/js',
            'assets/images',
            'assets/media',
            'assets/fonts'
        ]
        for directory in directories:
            os.makedirs(os.path.join(site_dir, directory), exist_ok=True)

    def _organize_files(self, site_dir):
        """Organize files into their correct directories"""
        # File type mappings
        file_types = {
            '.css': 'assets/css',
            '.js': 'assets/js',
            '.jpg': 'assets/images',
            '.jpeg': 'assets/images',
            '.png': 'assets/images',
            '.gif': 'assets/images',
            '.mp4': 'assets/media',
            '.mp3': 'assets/media',
            '.woff': 'assets/fonts',
            '.woff2': 'assets/fonts',
            '.ttf': 'assets/fonts'
        }

        # Walk through all files in the site directory
        for root, dirs, files in os.walk(site_dir):
            # Skip the assets directory itself
            if 'assets' in root.split(os.path.sep):
                continue

            for file in files:
                # Skip HTML files in root directory
                if file.endswith('.html') and root == site_dir:
                    continue

                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                # If we know where this type of file should go
                if ext in file_types:
                    target_dir = os.path.join(site_dir, file_types[ext])
                    target_path = os.path.join(target_dir, file)

                    # Move file to correct directory
                    if os.path.exists(target_path):
                        os.remove(file_path)  # Remove duplicate
                    else:
                        shutil.move(file_path, target_path)

        # Remove empty directories
        self._remove_empty_dirs(site_dir)

    def _remove_empty_dirs(self, path):
        """Remove empty directories"""
        for root, dirs, files in os.walk(path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path) and 'assets' not in dir_path:
                    os.rmdir(dir_path)

    def _verify_structure(self, site_dir):
        """Verify the site structure is correct"""
        expected_dirs = [
            'assets/css',
            'assets/js',
            'assets/images',
            'assets/media',
            'assets/fonts'
        ]

        # Check all expected directories exist
        for dir_path in expected_dirs:
            full_path = os.path.join(site_dir, dir_path)
            if not os.path.exists(full_path):
                print(f"Warning: Expected directory missing: {dir_path}")

        # Check for files in wrong locations
        for root, dirs, files in os.walk(site_dir):
            if 'assets' not in root.split(os.path.sep):
                for file in files:
                    if not file.endswith('.html'):
                        print(f"Warning: Non-HTML file found outside assets: {os.path.join(root, file)}")

    def _sanitize_name(self, name):
        """Convert a string into a valid directory/file name"""
        # Replace spaces and special characters with underscores
        sanitized = name.lower().strip()
        sanitized = ''.join(c if c.isalnum() else '_' for c in sanitized)
        sanitized = '_'.join(filter(None, sanitized.split('_')))  # Remove empty parts
        return sanitized