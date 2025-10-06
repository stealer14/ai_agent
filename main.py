import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_files import schema_write_files
from functions.run_python_file import schema_run_python_file


def main():
    #Reading .env file (if present) and load the variables in the environment
    load_dotenv()

    #Reference API key for google to get from .env file
    api_key = os.environ.get("GEMINI_API_KEY")

    #Setting name of client and model number
    client = genai.Client(api_key = api_key)
    model_no = 'gemini-2.0-flash-001'

    system_prompt = system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read the content of a file
        - Write to a file (create or update)
        - Run a Python file with optional arguments

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

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

        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_files,
                schema_run_python_file,
            ]
        )
        
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )       

        response = client.models.generate_content(
            model=model_no, 
            contents=messages,
            config = config,
        )

        
        # Check for function calls or text in response
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call_part = part.function_call
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                elif hasattr(part, 'text') and part.text:
                    if verbose_mode:
                        print("******** Reporting.... ***********")
                        print(f"User prompt: {prompt}")
                        print(part.text)
                        print("\n********* Prompt Statistics *****************")
                        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
                    else:
                        print(part.text)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
