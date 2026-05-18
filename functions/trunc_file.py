from google.genai import types

import os

schema_trunc_file = types.FunctionDeclaration(
    name="trunc_file",
    description="Truncates file to a specified size equal to or below its current size",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to truncate, relative to the working directory. Mandatory argument",
            ),

            "size": types.Schema(
                type=types.Type.INTEGER,
                description="New size of the file. Mandatory argument.",
            ),
        },
    ),
)

def trunc_file(working_directory, file_path, size):
    cwd = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(cwd, file_path))

    if os.path.commonpath([cwd, target]) != cwd:
        return f'Error: Cannot write to "{target}" as it is outside the permitted working directory'

    if os.path.isdir(target):
        return f'Error: Cannot write to "{target}" as it is outside the permitted working directory'

    os.makedirs("/".join(target.split("/")[:-1]), exist_ok=True)

    try:
        with open(target, "a") as f:
            f.truncate(size)
        return f'Successfully truncated "{file_path}" to {size} bytes.'
    except Exception as e:
        return f'Error: {e}'
