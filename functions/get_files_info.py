import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = "."):
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_absolute, directory))

        valid_target_directory = os.path.commonpath([working_directory_absolute, target_directory]) == working_directory_absolute
        valid_directory = os.path.isdir(target_directory)
    
        if not valid_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not valid_directory:
            return f'Error: {directory} is not a directory'
        #return f'Success: "{directory}" is within the working directory'
        
        target_directory_names = os.listdir(target_directory)
        result = []
        for item_name in target_directory_names:
            path = f"{target_directory}/{item_name}"
            file_size = os.path.getsize(path)
            is_directory = os.path.isdir(path)
            result.append(f"- {item_name}: file_size={file_size} bytes, is_dir={is_directory}")
        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"