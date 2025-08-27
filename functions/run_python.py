import os
import subprocess

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
