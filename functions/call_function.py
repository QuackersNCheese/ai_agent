from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ],
)
# Mapping the string names from the LLM to our actual Python functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    # 1. Check if the function exists in our map
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

    # 2. Prepare the arguments
    # We use dict() to create a shallow copy so we don't mutate the original object
    args = dict(function_call.args) if function_call.args else {}
    
    # 3. Security: Inject the working directory "behind the scenes"
    args["working_directory"] = "./calculator"

    # 4. Execute the function using dictionary unpacking (**)
    try:
        # This calls the actual function (e.g., write_file) with the args
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = f"Error: Internal execution failed: {str(e)}"

    # 5. Return the result in the format Gemini requires
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )