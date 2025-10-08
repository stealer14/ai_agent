import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_files import schema_write_files
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

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

    # Initialize conversation
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_files,
            schema_run_python_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    max_iters = 20
    for i in range(max_iters):
        try:
            # Model call with full history
            response = client.models.generate_content(
                model=model_no,
                contents=messages,
                config=config,
            )

            # Add model outputs to the conversation
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Check model’s reply parts
            if not response.candidates:
                print("No response candidates found.")
                break

            parts = response.candidates[0].content.parts
            if not parts:
                print("No content parts returned.")
                break

            done = False
            for part in parts:
                # Function call
                if hasattr(part, "function_call") and part.function_call:
                    function_call_part = part.function_call

                    if verbose_mode:
                        print(f"- Calling function: {function_call_part.name}")

                    function_call_result = call_function(function_call_part, verbose=verbose_mode)

                    if (
                        not function_call_result.parts
                        or not hasattr(function_call_result.parts[0], "function_response")
                    ):
                        raise Exception("Function call did not return a valid response")

                    result_data = function_call_result.parts[0].function_response.response
                    output = result_data.get("result", "") if isinstance(result_data, dict) else str(result_data)
                    print(output)

                    # Feed result back into conversation
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part(text=f"Tool result:\n{output}")]
                        )
                    )

                # Final text response
                elif hasattr(part, "text") and part.text:
                    if verbose_mode:
                        print("******** Reporting.... ***********")
                        print(f"User prompt: {prompt}")
                        print(part.text)
                        print("\n********* Prompt Statistics *****************")
                        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
                    else:
                        print(part.text)
                    done = True
                    break

            if done:
                print("Final response:")
                break

        except Exception as e:
            print(f"Exception occurred: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()