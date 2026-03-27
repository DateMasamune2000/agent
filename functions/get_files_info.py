from google.genai import types

import os

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

def get_files_info(working_directory, directory="."):
	cwd = os.path.abspath(working_directory)
	target_dir = os.path.normpath(os.path.join(cwd, directory))

	if os.path.commonpath([cwd, target_dir]) != cwd:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

	try:
		return '\n'.join(map(lambda f: f"- {f[0]}: file_size={os.stat(f[1]).st_size} bytes, is_dir={os.path.isdir(f[1])}", map(lambda x: (x, f"{target_dir}/{x}"), os.listdir(target_dir))))
	except NotADirectoryError as e:
		return f'Error: "{directory}" is not a directory'
	except Exception as e:
		return f"Error: {e}"
