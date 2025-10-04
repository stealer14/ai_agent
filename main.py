import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info

#Reading .env file (if present) and load the variables in the environment
load_dotenv()

#Reference API key for google to get from .env file
api_key = os.environ.get("GEMINI_API_KEY")

#Setting name of client and model number
client = genai.Client(api_key = api_key)
model_no = 'gemini-2.0-flash-001'

def main():
    #command line parsing 
    if len(sys.argv) < 2:
        print("Usage: uv run main.py \"<prompt\" [--verbose]")
        sys.exit(1)

    #First argument will always be the prompt
    prompt = sys.argv[1]

    #Second argument Check if --verbose flag exist anywhere after the prompt
    verbose_mode = "--verbose" in sys.argv[2:]

    #Program starts running here.
    print("Hello from Nestor ai-agent! project")

    # Previous state: direct prompt string used in generate_content
    # response = client.models.generate_content(model=model_no, contents=[prompt])

    # New state: using types.Content and types.Part for messages

    try:       
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
        response = client.models.generate_content(model=model_no, contents=messages)

        if response:
            #Always print the mode's answer 
            #print(response.text)

            if verbose_mode: #When the flag for verbose mode is provided in sys.argv[2]
                print("******** Reporting.... ***********")
                print(f"User prompt: {prompt}")
                print(response.text)

                print("\n********* Prompt Statistics *****************")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
                sys.exit(0)

            else: #normal mode, only return the basic response 
                print(response.text)
                sys.exit(0)

    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
