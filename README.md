# Book Award AI Scraper

1. Read a [JSON list](./bookawards.json) of 100 generated book awards with URLs (Perplexity Deep Research) 


# Setup

1. setup file `.env` with the API key:

`
PERPLEXITY_API_KEY=<KEY>
`

2. Create environment:  `python3 -m venv .venv`

3. activate the environment: `source .venv/bin/activate`
4.  Now install the packages (within the activated virtual environment: `pip install requests rich python-dotenv`
5. run perplexity call alone: `py perplexity.py`