from langchain_openai import ChatOpenAI
from flask import current_app, g

def connect_ai():
	try:
		# Create a new client and connect to the server
		if 'llm' not in g:
			llm = ChatOpenAI(
				model="gpt-4o",
				temperature=0,
				max_tokens=None,
				timeout=100,
				max_retries=3,
				api_key=current_app.config['OPENAI_API_KEY'],
			)
			g.llm = llm
		return g.llm

	except Exception as e:
		print(e)