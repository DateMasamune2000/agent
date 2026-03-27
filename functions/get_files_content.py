from google.genai import types

import os

MAX_CHARS = 10000

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets content of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get content from, relative to the working directory. Mandatory argument, no default values.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
	print(f'file_path: {file_path}')
	cwd = os.path.abspath(working_directory)
	target = os.path.normpath(os.path.join(cwd, file_path))

	if os.path.commonpath([cwd, target]) != cwd:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

	try:
		with open(target) as f:
			content = f.read(MAX_CHARS)
			if f.read(1):
				content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
			return content
	except (FileNotFoundError, IsADirectoryError) as e:
		return f'Error: File not found or is not a regular file: "{file_path}"'
	except Exception as e:
		return f'Error: {e}'


