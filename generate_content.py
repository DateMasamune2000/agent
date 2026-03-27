import os
from dotenv import load_dotenv
from google.genai import types
from prompts import system_prompt

def get_key():
	load_dotenv()
	k = os.environ.get("GEMINI_API_KEY")
	if k == None:
		raise RuntimeError("Could not get API key from environment");
	return k

def generate_content(client, args, messages, available_functions):
	return client.models.generate_content(
		model='gemini-2.5-flash',
		contents=messages,
		config = types.GenerateContentConfig(
			tools=[available_functions],
			system_instruction=system_prompt
		),
	)
