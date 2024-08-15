import os
import shutil
import subprocess
import math

def create_folder(path):
    """
    Create a folder at the specified path.
    """
    try:
        os.makedirs(path)
        print(f"Folder created at: {path}")
    except FileExistsError:
        print(f"Folder already exists at: {path}")

def delete_folder(path):
    """
    Delete the folder at the specified path.
    """
    try:
        shutil.rmtree(path)
        print(f"Folder deleted at: {path}")
    except FileNotFoundError:
        print(f"Folder not found at: {path}")
    except OSError as e:
        print(f"Error: {e.strerror}")

def delete_file(path):
    """
    Delete the file at the specified path.
    """
    try:
        os.remove(path)
        print(f"File deleted at: {path}")
    except FileNotFoundError:
        print(f"File not found at: {path}")
    except OSError as e:
        print(f"Error: {e.strerror}")



def oscmd(cmd):
    val = subprocess.run(cmd,capture_output=True,text=True,shell=True)
    return val.stdout


def data_stored(path):
# Example usage:
    directory_path = path
    # target_file_name = 'example.txt'  # Replace with the file name you are looking for
    print('dir /s "'+path+'"')
    a = subprocess.run('dir /s "'+path+'" | findstr /c:"bytes"  ',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    l = list(a.stdout.split("\n"))
    print(l)
    #print(l[-3].split())
    #print(type(a.stdout))
    return str((l[-3].split()[-2])).replace(",","")

# Example usage
# folder_path = 'example_folder'
# file_path = 'example_folder/example_file.txt'

# # Create a folder
# create_folder(folder_path)

# # Create a file in the folder for testing delete_file function
# with open(file_path, 'w') as f:
#     f.write("This is a test file.")

# # Delete the file
# delete_file(file_path)

# # Delete the folder
# delete_folder(folder_path)
def check_file_stirage(path):
    total_stored = int(data_stored(path))
    toatal_storage_to_gb = total_stored/math.pow(1024,3)
    if(toatal_storage_to_gb > 2):
        return True
    return False