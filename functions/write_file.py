from google.genai import types

import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))


        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(working_dir_abs, exist_ok=True)
        
        file = open(target_dir, mode='w')
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



    except Exception as e:
        print(f"Error: {e}")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Writes to a file at the specified file_path with the specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to working_directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file",
            ),
        },
    ),
)
