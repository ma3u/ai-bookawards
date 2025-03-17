import requests
import os
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "temperature": 0.2,
    "top_p": 0.9,
    "search_domain_filter": [],
    "return_images": False,
    "return_related_questions": False,
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1,
    "model": "sonar",
    "messages": [
        {
            "role": "user",
            "content": "Describe step-by-step in detail how to use the MCP protocol in Perplexity via API?"
        }
    ]
}
headers = {
    "Authorization": f"Bearer {os.environ.get('PERPLEXITY_API_KEY')}",
    "Content-Type": "application/json"
}

# Rest of your code remains the same