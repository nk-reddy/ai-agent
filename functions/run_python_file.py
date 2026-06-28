import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
    
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", os.path.abspath(target_dir)]
        if args:
            command.extend(args)
        
        process = subprocess.run(
            command, 
            cwd=working_dir_abs, 
            capture_output=True, 
            text=True, 
            timeout=30
        )

        output = ""
        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}\n"
        if not process.stdout and not process.stderr:
            output += "No output produced\n"
        else:
            if process.stdout:
                output += f"STDOUT: {process.stdout}\n"
            if process.stderr:
                output += f"STDERR: {process.stderr}"
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the process",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument",
                ),
            ),
        },
        required=["file_path"],
    ),
)