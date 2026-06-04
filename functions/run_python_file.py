from google.genai import types

import subprocess
import os


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str | None:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args is not None:
            command.extend(args)

        completed = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = ""

        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode} "
        if completed.stdout is not None:
            output += f"STDOUT: {completed.stdout}"
        if completed.stderr != "":
            output += f"STDERR: {completed.stderr}"
        if output == "":
            output += "No output produced"

        return output

    except Exception as e:
        print(f"Error: executing Python file: {e}")


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to working_directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING, description="Argument passed to function"
                ),
            ),
        },
    ),
)
