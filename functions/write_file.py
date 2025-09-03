import os
from google.genai import types

def write_file(working_directory, file_path, content):
    
    try:   
        wd = os.path.realpath(working_directory)
        target = os.path.realpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([wd, target]) != wd:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        os.makedirs(os.path.dirname(target), exist_ok=True)
        
        try:
            with open(target, "w", encoding="utf-8") as file:
                file.write(content)
            return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        except Exception as e:
            return f"Error: {e}"
        
    except Exception as e:
         return f"Error: {e}"



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)