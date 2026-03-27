from google.genai import types

import os
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file given a path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to Python file being run. Mandatory argument."
            ),
			"args": types.Schema(
				type=types.Type.ARRAY,
				items=types.Schema(type=types.Type.STRING),
				description="List of arguments. Leave empty for no args."
			),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
	cwd = os.path.abspath(working_directory)
	target = os.path.normpath(os.path.join(cwd, file_path))

	if os.path.commonpath([cwd, target]) != cwd:
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	if not os.path.isfile(target):
		return f'Error: "{file_path}" does not exist or is not a regular file'

	if not file_path.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file'

	try:
		command = ["python", target]
		command.extend(args)

		stderr = ""
		stdout = ""
		
		cproc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
		output = ""

		if cproc.returncode != 0:
			output += f"Process exited with code {cproc.returncode}\n"

		if len(cproc.stdout) == 0 and len(cproc.stderr) == 0:
			output += "No output produced\n"
		else:
			output += f"STDOUT: {cproc.stdout}\n"
			output += f"STDERR: {cproc.stderr}\n"
		return output
	except Exception as e:
		return f"Error: executing Python file: {e}"
