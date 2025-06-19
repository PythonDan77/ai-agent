from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if isinstance(function_call_part, list):
        call = function_call_part[0]
    else:
        call = function_call_part
    func_name = call.name
    func_args = {"working_directory":"./calculator", **call.args}

    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    functions_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    }

    if func_name in functions_map:
        try:
            func_result = functions_map[func_name](**func_args)

            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=func_name,
                        response={"result": func_result},
                    )
                ],
            )

        except Exception as e:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=func_name,
                            response={"error": str(e)},
                        )
                    ],
                )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unknown function: {func_name}"},
            )
        ],
    )