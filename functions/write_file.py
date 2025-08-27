import os

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



#os.path.realpath on both sides and compare with os.path.commonpath.