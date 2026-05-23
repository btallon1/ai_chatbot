import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files in a specified directory relative to the working directory, returning the output of the python function (including errors and return codes other than 0)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Additional arguments to be passed onto the python function, provided as a list of strings",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument to be passed onto a python function",
                )
            )
        },
        required=["file_path"]
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_absolute = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_absolute, file_path))

        valid_target_file_path = os.path.commonpath([working_directory_absolute, target_file_path]) == working_directory_absolute
        valid_file_path = os.path.isfile(target_file_path)

        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not valid_file_path:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        child_process = subprocess.run(command, cwd=working_directory_absolute, capture_output=True, text=True, timeout=30)
        output = ""
        if child_process.returncode != 0:
            output += f"Process exited with code {child_process.returncode}"
        if not child_process.stdout and not child_process.stderr:
            output += f"No output produced"
        if child_process.stdout:
            output += f"STDOUT: {child_process.stdout}"
        if child_process.stderr:
            output += f"STDERR: {child_process.stderr}"
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"