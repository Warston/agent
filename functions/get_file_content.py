from google.genai import types

import os
from config import MAX_CHARS
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))


        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file = open(target_dir)

        content = file.read(MAX_CHARS)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        print(f"Error: {e}")
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves contents of a file given a file path. It will only read up to the maximum {MAX_CHARS}",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to working_directory",
            ),
        },
    ),
)
