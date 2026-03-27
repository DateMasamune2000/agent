from google.genai import types

import os

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file given the path relative to the working directory. Overwrites content if file exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory. Mandatory argument",
            ),

            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file. Mandatory argument.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
	cwd = os.path.abspath(working_directory)
	target = os.path.normpath(os.path.join(cwd, file_path))

	if os.path.commonpath([cwd, target]) != cwd:
		return f'Error: Cannot write to "{file}" as it is outside the permitted working directory'

	if os.path.isdir(target):
		return f'Error: Cannot write to "{target}" as it is outside the permitted working directory'

	os.makedirs("/".join(target.split("/")[:-1]), exist_ok=True)

	try:
		with open(target, "w") as f:
			f.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f'Error: {e}'
