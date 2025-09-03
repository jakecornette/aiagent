import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:   
        
        if file_path[-2:] != 'py':
            return f'Error: "{file_path} is not a Python file.'
        
        if os.path.realpath(os.path.join(working_directory, file_path)):
            wd = os.path.realpath(working_directory)
            target = os.path.realpath(os.path.join(working_directory, file_path))
        else: 
            return f'Error: File "{file_path}" not found.'

        if os.path.commonpath([wd, target]) != wd:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(target) == False:
            return f'File "{file_path}" not found.'
        
        try:
            command = ["python3", target]
            result = subprocess.run(command, capture_output=True, timeout=30, check=True)
            if result == None:
                return "No output produced."
            return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'

        except subprocess.CalledProcessError as e:
            return f"Error: {e}\nProcess exited with code X"
        
    except Exception as e:
         return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)