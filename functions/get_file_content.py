import os
from functions import config


def truncate_string(s, max_length):
        if len(s) > max_length:
            return s[:max_length] + "..."
        else:
            return s

def get_file_content(working_directory, file_path):
    try:
        combined_directory = os.path.join(working_directory, file_path)

        full_directory = os.path.abspath(combined_directory)
        #print(full_directory)
        combined_string = str(combined_directory)
        working_string = str(working_directory)
        #print(working_string)

        if os.path.isfile(full_directory) == False:
            return (f'Error: File not found or is not a regular file: "{file_path}"')

        if combined_string.startswith(working_string) == False:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        
        MAX_CHARS = config.character_limit

        with open(full_directory, "r") as f: 
            file_content_string = f.read(MAX_CHARS)

        

        if len(file_content_string) > 10000:
            file_content_string = truncate_string(file_content_string, MAX_CHARS)
            return f'{file_content_string}[...File "{file_path}" truncated at 10000 characters].'

        return file_content_string


    except:
        
        print('Error: an unexpected error occurred in "get_file_content"!')