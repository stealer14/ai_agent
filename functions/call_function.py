from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_files import write_files
from functions.run_python_file import run_python_file
from google.genai import types
import os

working_directory = "calculator"

def call_function(function_call_part, verbose=False):
    """Handles calling the correct function based on the LLM's request."""

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Map of available functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_files": write_files,
        "run_python_file": run_python_file,
    }

    func = function_map.get(function_call_part.name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    try:
        # Call the function and capture its result
        result = func(working_directory, **function_call_part.args)
    except Exception as e:
        result = f"Error while executing {function_call_part.name}: {e}"

    # Always return a structured response
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},  # ✅ always wrapped in "result"
            )
        ],
    )