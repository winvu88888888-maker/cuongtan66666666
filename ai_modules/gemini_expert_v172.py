import sys
import os

# Redirect to gemini_helper
try:
    # Try parent directory first (where gemini_helper usually lives)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
        
    from gemini_helper import GeminiQMDGHelper
except ImportError:
    # Fallback or stub if not found
    class GeminiQMDGHelper:
        def __init__(self, *args, **kwargs):
            pass
        def _call_ai(self, *args, **kwargs):
            return "🛑 AI Module missing."
