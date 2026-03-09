import os
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Directory created", directory)
        os.mkdir(directory)

create_project_dir("mysite")

def create_data_files(project_name, base_url):
    queque=os.path.join(project_name, "queue.txt")
    crawled=os.path.join(project_name, "crawled.txt")
    if not os.path.isfile(queque):
        write_data(queque, base_url)
    if not os.path.isfile(crawled):
        write_data(crawled, '')

def write_data(path, data):
    with open(path, 'w') as f:
        f.write(data)

def append_to_file(path, data):
    with open(path, 'a') as f:
        f.write(data + "\n")

def delete_file_contents(path):
    open(path,'w').close()
def file_to_set(file_path):
    results=set()
    with open(file_path, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(links, file_name):
    with open(file_name, 'w') as f:
        for l in links:
            f.write(l+'\n')






