import os

def create_file(filename):
    try:
        with open(filename, 'w') as file:
            print("File created successfully:", filename)
    except IOError:
        print("Error: Unable to create file")

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            print("File content of", filename, ":\n", file.read())
    except FileNotFoundError:
        print("Error: File not found")

def delete_file(filename):
    try:
        os.remove(filename)
        print("File deleted successfully:", filename)
    except FileNotFoundError:
        print("Error: File not found")

# Example usage
filename = "example.txt"

# Create file
create_file(filename)

# Read file
read_file(filename)

# Delete file
delete_file(filename)
