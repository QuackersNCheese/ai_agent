import os

def write_file(working_directory, file_path, content):
    try:
        # Security and path validation
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Block writing to directories
        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Ensure parent directories exist
        parent_dir = os.path.dirname(target_file_abs)
        os.makedirs(parent_dir, exist_ok=True)

        # Write the file
        with open(target_file_abs, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"