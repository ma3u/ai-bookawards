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

response = requests.request("POST", url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Pretty print the entire response
    console.print("[bold blue]Full Response:[/bold blue]")
    console.print(data)
    
    # Format and print messages content
    console.print("\n[bold green]Formatted Messages:[/bold green]")
    if 'choices' in data:
        for choice in data['choices']:
            if 'message' in choice:
                console.print(f"[bold magenta]Role:[/bold magenta] {choice['message']['role']}")
                markdown = Markdown(choice['message']['content'])
                console.print(markdown)
            if 'delta' in choice and choice['delta']['content']:
                console.print(f"[bold magenta]Role:[/bold magenta] {choice['delta']['role']}")
                markdown = Markdown(choice['delta']['content'])
                console.print(markdown)
    else:
        console.print("[bold red]No 'choices' key found in the response.[/bold red]")
else:
    console.print(f"[bold red]Error with status code {response.status_code}[/bold red]")
    console.print("Response Data:")
    console.print(response.text)
