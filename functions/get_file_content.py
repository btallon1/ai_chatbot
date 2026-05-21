import os

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_absolute, file_path))

        valid_target_file_path = os.path.commonpath([working_directory_absolute, target_file_path]) == working_directory_absolute
        valid_file_path = os.path.isfile(target_file_path)

        if not valid_target_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not valid_file_path:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        open_file = open(target_file_path)
        file_content = open_file.read(MAX_CHARS)
        if open_file.read(1):
            file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content

    except Exception as e:
        return f"Error: {e}"