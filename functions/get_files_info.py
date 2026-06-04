from google.genai import types
import os


def get_files_info(working_directory: str, directory: str = ".") -> str | None:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is'
        if not os.path.isdir(target_dir):
            return f"{directory} is not a directory"
        dir_tree = os.listdir(target_dir)
        dir_dict = {}

        for item in dir_tree:
            dir_dict[item] = [
                str(os.path.getsize(target_dir + "/" + item)),
                str(os.path.isdir(target_dir + "/" + item)),
            ]
        result = ""
        result = "\n".join(
            list(
                map(
                    lambda x: (
                        f"{x}: "
                        + f"file_size={dir_dict[x][0]}, is_dir={dir_dict[x][1]}"
                    ),
                    dir_dict,
                )
            )
        )
        print(f'Success: "{directory}" is within the working directory')
        print(result)
        return result

    except Exception as e:
        print(f"Error: {e}")


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
