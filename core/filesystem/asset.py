from typing import Optional
from core.facade.config import Config
from core.facade.env import Env

class AssetManager:
    def __init__(self):
        self.asset_url = Config.get('app.asset_url', '/static')
        self.secure = Env.get('HTTPS', False)

    def url(self, path: str) -> str:
        """Get the URL for an asset."""
        # Clean the path
        path = path.lstrip('/')
        base = self.asset_url.rstrip('/')
        return f"{base}/{path}"

    def secure_url(self, path: str) -> str:
        """Get the secure URL for an asset."""
        url = self.url(path)
        if url.startswith('//'):
            return f"https:{url}"
        if url.startswith('http://'):
            return url.replace('http://', 'https://')
        return url

# Create a singleton instance
asset = AssetManager() 