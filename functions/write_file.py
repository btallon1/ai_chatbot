import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_absolute, file_path))

        valid_target_file_path = os.path.commonpath([working_directory_absolute, target_file_path]) == working_directory_absolute
        invalid_file_path = os.path.isdir(target_file_path)

        if not valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if invalid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_directory = os.path.dirname(target_file_path)
        os.makedirs(parent_directory, exist_ok=True)

        open_file = open(target_file_path, mode="w")
        open_file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"