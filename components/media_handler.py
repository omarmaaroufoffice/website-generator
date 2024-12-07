import os
import requests

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL not available. Image processing will be limited.")

class MediaHandler:
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.has_pil = PIL_AVAILABLE

    def handle_media(self, site_dir, site_config):
        """Handle all media-related tasks"""
        if site_config.get('images'):
            self._process_images(site_dir, site_config['images'])
        
        if site_config.get('videos'):
            self._process_videos(site_dir, site_config['videos'])
        
        if site_config.get('fonts'):
            self._process_fonts(site_dir, site_config['fonts'])

    def _process_images(self, site_dir, images_config):
        """Process and optimize images"""
        images_dir = os.path.join(site_dir, 'images')
        for image in images_config:
            self._handle_image(images_dir, image)

    def _handle_image(self, images_dir, image_config):
        """Handle individual image processing"""
        if not self.has_pil:
            print(f"Warning: Skipping image processing for {image_config}. PIL not available.")
            return
        # Implementation for image processing when PIL is available
        pass 