import os
import types
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # construct target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # target in working directory?
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # check existence
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # Iterate and gather data
        files_list = os.listdir(target_dir)
        output_lines = []

        for item in sorted(files_list):
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            output_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: {str(e)}"
    
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
