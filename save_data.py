import os


# Each website you crawl is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.makedirs(directory)


# Create crawled files (if not created)
def insert_data_to_file(project_name, data):
    crawled = project_name + '/crawled-5.txt'

    if not os.path.isfile(crawled):
        write_file(crawled, data)
    else:
        append_to_file(crawled, data)


# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass
