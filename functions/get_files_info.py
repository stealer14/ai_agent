import os

def get_files_info(working_directory, directory = "."):
    try:
        # Compute absolute pahts safely
        abs_working_dir = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(os.path.join(abs_working_dir, directory))

        # Ensure directory stays within working directory
        if not abs_directory.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the resolved path is actually a directory
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'

        # Build formatted listing
        entries = []
        contents = os.listdir(abs_directory)
        for item in contents:
            item_path = os.path.join(abs_directory, item)
            try:
                is_dir = os.path.isdir(item_path)
                size = os.path.getsize(item_path)
                entries.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                entries.append(f"- {item}: Error: {str(e)}")

        return "\n".join(entries)
    
    except Exception as e:
        return f"Error: {str(e)}"
