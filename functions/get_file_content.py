import os
from config import MAX_CHARS



def get_file_content(working_directory, file_path):
    # Check If the file_path is outside the working_directory, return a string with an error
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    #Check if file is outside of working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    #Check fi file path does not exist
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    file_content_string = ""
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (f'[...File "{file_path}" truncated at 10000 characters]')
        return file_content_string
    except Exception as e:
        return f"Exception reading file: {e}"