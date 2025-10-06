import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    #Check if file is outside of working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    #Check fi file path does not exist
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    #Check if file ends with .py
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        final_args = ["python3", file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args, 
            cwd = abs_working_dir, 
            timeout = 30,
            capture_output = True
            )
        final_string = f""" 
STDOUT: {output.stdout}       
STDERR: {output.stderr}
"""
        if output.stdout == "" and output.stderr == "":
            final_string = "Not output produced.\n"
        if output.returncode != 0:
            final_string += f'Process exited with code {output.returncode}'
        return final_string
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts additional CLI args as an optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run relative to the current directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the Python",
                items=types.Schema(
                    type=types.Type.STRING,
                )
            )
        },
    ),
)