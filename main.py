import sys
import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from functions.call_function import call_function, available_functions

from pathlib import Path


def main():
    print("Starting main function...")
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    
    client = genai.Client(api_key=api_key)

    model_name="gemini-2.0-flash-001"

    parser = argparse.ArgumentParser(description="AI Coding Agent CLI")
    parser.add_argument("prompt", help="The prompt to send to the AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    prompt = args.prompt
    verbose = args.verbose

    """
	Initialize conversation with the user's initial prompt,
	formatted as a types.Content object
	"""
    conversation = [
    	types.Content(role='user', parts=[types.Part(text=prompt)])
    ]

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
	)

    try:
    	for _ in range(20):

    		response = client.models.generate_content(
    			model=model_name,
    			contents=conversation,
    			config=config
    		)

    		candidate = response.candidates[0]

			# Handle function calls and add model & tool outputs together conversation (if not broken) (model calls first to avoid model invocation issues [user>model>tool])
    		if response.function_calls:
    			tool_parts = []
    			for called_function in response.function_calls:
    				function_call_result = call_function(called_function)
    				if not function_call_result.parts[0].function_response.response:
    					raise Exception("Function call result missing expected response structure") 
    				if function_call_result.parts[0].function_response.response and verbose:
    					print(f"-> {function_call_result.parts[0].function_response.response}")
    				tool_parts.append(function_call_result.parts[0])
    			conversation.append(candidate.content)
    			conversation.append(types.Content(role="tool", parts=tool_parts))

    		else:
    			conversation.append(candidate.content)
    			if response.text:
    				print(f"Final response:\n{response.text}")
    				break

    	else:
    		print("Agent stopped after 20 iterations to prevent an infinite loop.")
    		print("The agent might still be thinking, or it may have reached a conclusion.")

    except Exception as e:
    	print(f'Error: An unexpected error occured: {e}')

'''
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

        # Access the candidates
    candidates = response.candidates

    # Access the content from the candidates
    if candidates:
        # A candidate's content is composed of "parts"
        for candidate in candidates:
            for part in candidate.content.parts:
                if part:
                    messages.append(part.text)
                    #print(f"\n{part.text}\n")

    else:
        print("No candidates were returned.")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_responses[0].text))
        #print(f"\n\n{function_responses[0].text}\n\n")
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    #print(f"*\n*\n*{function_responses[0]}")
    #print(f"&\n&\n{messages}")
'''

if __name__ == "__main__":
    main()
