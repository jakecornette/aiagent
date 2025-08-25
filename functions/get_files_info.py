import os
try:
    def get_files_info(working_directory, directory="."):
    
        combined_directory = os.path.join(working_directory, directory)

        full_directory = os.path.abspath(combined_directory)

        combined_string = str(combined_directory)
        working_string = str(working_directory)

        if combined_string.startswith(working_string) == False:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if os.path.isdir(working_directory) == False:
            return (f'Error: "{directory}" is not a directory')

        file_list = os.listdir(working_directory)

        build_str = ""

        for file in file_list:
            file_name = str(file)
            file_size = str(os.path.getsize(working_directory))
            is_dir = os.path.isdir(f"{full_directory}/{file}")
            if is_dir == True:
                new_file_list = os.listdir(f"{full_directory}/{file}")
                for f in new_file_list:
                    filename = str(f)
                    filesize = str(os.path.getsize(working_directory))
                    isdir = os.path.isdir(f"{full_directory}/{f}")
                    build_str = build_str + f"{filename}: file_size={filesize} bytes, is_dir={isdir}\n"
            build_str = build_str + f"{file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return build_str


    get_files_info("calculator")



except:
    print("An unexpected error occurred!")