import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # Check If the file_path is outside the working_directory, return a string with an error
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could not create parent dirs: {parent_dir} = {e}"
    
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Failed to write to file: {file_path}, {e}"
    
schema_write_files = types.FunctionDeclaration(
    name="write_files",
    description="Overwrites, or writes to a new file or writes to a new file if it does not exist (and creates required parent dirs safely)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write.",
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a String.",
            )
        },
    ),
)