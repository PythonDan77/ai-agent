import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, abs_file_path]) != working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not os.path.basename(abs_file_path).endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True, text=True, cwd=working_directory)
        final_result = []
        if result.stdout:
            final_result.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            final_result.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            final_result.append(f"Process exited with code {result.returncode}")
        return "\n".join(final_result) if final_result else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory. Captures stdout and stderr, with a timeout of 30 seconds.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute from the working directory."
            )
        },
        required=["file_path"]
    )
)

 

    

    