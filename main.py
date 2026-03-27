import os
import argparse

from prompts import system_prompt
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from generate_content import get_key, generate_content

def main():
	api_key = get_key()

	client = genai.Client(api_key=api_key)

	parser = argparse.ArgumentParser(description="Chatbot")
	parser.add_argument("user_prompt", type=str, help="User prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()

	# Initialize messages
	messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

	for _ in range(20):
		# Generate content
		response = generate_content(client, args, messages, available_functions)
		if response.usage_metadata == None:
			raise RuntimeError("Failed API request")

		# Count tokens
		ptk = response.usage_metadata.prompt_token_count
		rtk = response.usage_metadata.candidates_token_count

		if ptk == None or rtk == None:
			raise RuntimeError("Failed API request")

		fresps = []

		# Print response
		if response.function_calls is None:
			print(response.text)
			exit(0)
		else:
			for function_call in response.function_calls:
				print(f"Calling function: {function_call.name}({function_call.args})")
				resp = call_function(function_call, args.verbose)

				if resp.parts[0].function_response.response == None:
					raise Exception("no response from function")
				if args.verbose:
					print(f"-> {resp.parts[0].function_response.response}")
				fresps.extend(resp.parts)

		for candidate in response.candidates:
			messages.append(candidate.content)

		messages.append(types.Content(role="user", parts=fresps))

		if args.verbose:
			print(f"User prompt: {args.user_prompt}")
			print(f"Prompt tokens: {ptk}")
			print(f"Response tokens: {rtk}")

	raise Exception("bro what are you doing that needs 20 iterations from a bot to get right")

if __name__ == "__main__":
    main()
