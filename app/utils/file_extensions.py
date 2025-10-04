def get_file_extensions(file_name):
    file_split = file_name.split(".")

    return file_split[-1].lower()