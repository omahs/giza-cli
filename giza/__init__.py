import os

__version__ = "0.4.0"
# Until DNS is fixed
API_HOST = os.environ.get("GIZA_API_HOST", "https://api.gizatech.xyz")
