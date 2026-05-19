import os

def get_files_info(working_directory, directory="."):
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_absolute, directory))

        valid_target_directory = os.path.commonpath([working_directory_absolute, target_directory]) == working_directory_absolute
        valid_directory = os.path.isdir(directory)
    
        if not valid_target_directory:
            #raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not valid_directory:
            #raise Exception(f'Error: {directory} is not a directory')
            print(f'Error: {directory} is not a directory')
        if valid_directory and valid_target_directory:
            print(f'Success: "{directory}" is within the working directory')
    except Exception as e:
        return f"Error: {e}"

        