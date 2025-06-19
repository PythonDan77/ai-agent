import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    
    working_directory = os.path.abspath(working_directory)

    if directory:
        target_directory = os.path.join(working_directory, directory)
    else:
        target_directory = working_directory

    target_directory = os.path.abspath(target_directory)

    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    if os.path.commonpath([working_directory, target_directory]) != working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        file_list = sorted(os.listdir(target_directory))
        data_list = []
        for file in file_list:
            full_path = os.path.join(target_directory, file)
            data_list.append(f"- {file}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}")
        return "\n".join(data_list)
    except Exception as e:
        return f"Error listing files: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

    
    

