import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types





def main():
    print("Hello from aiagent!")

    load_dotenv()
    api_key = os.environ.get("GEMENI_API_KEY")
    
    client = genai.Client(api_key=api_key)

    if len(sys.argv) == 1:
        print("No prompt provided.")
        sys.exit(1)
    elif len(sys.argv) > 1:
        content = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=content)]),]
        response = client.models.generate_content(
        model="gemini-2.0-flash-001",contents=messages)
        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

    prompt_t = response.usage_metadata.prompt_token_count
    response_t = response.usage_metadata.candidates_token_count

    print(response.text)

    #print(f"Prompt tokens: {prompt_t}\nResponse tokens: {response_t}")




if __name__ == "__main__":
    main()
