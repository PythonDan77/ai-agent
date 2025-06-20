from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file

WORKING_DIR = "./calculator"

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
# def call_function(function_call_part, verbose=False):
    
#     call = function_call_part
#     func_name = call.name
#     func_args = {"working_directory":"./calculator", **call.args}

#     if verbose:
#         print(f"Calling function: {func_name}({func_args})")
#     else:
#         print(f" - Calling function: {func_name}")

#     functions_map = {
#     "get_files_info": get_files_info,
#     "get_file_content": get_file_content,
#     "write_file": write_file,
#     "run_python_file": run_python_file,
#     }

#     if func_name in functions_map:
#         try:
#             func_result = functions_map[func_name](**func_args)

#             return types.Content(
#                 role="tool",
#                 parts=[
#                     types.Part.from_function_response(
#                         name=func_name,
#                         response={"result": func_result},
#                     )
#                 ],
#             )

#         except Exception as e:
#                 return types.Content(
#                     role="tool",
#                     parts=[
#                         types.Part.from_function_response(
#                             name=func_name,
#                             response={"error": str(e)},
#                         )
#                     ],
#                 )

#     return types.Content(
#         role="tool",
#         parts=[
#             types.Part.from_function_response(
#                 name=func_name,
#                 response={"error": f"Unknown function: {func_name}"},
#             )
#         ],
#     )