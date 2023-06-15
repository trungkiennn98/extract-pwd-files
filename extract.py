import os
import subprocess
import concurrent.futures
import time
import zipfile
import json

#path to the WinRAR executable
winrar_path = r"winrar\path"

#path to the folder containing the compressed files
compressed_files_folder = r"path\to\compressed\folder"

#passwords.json file
passwords_file = r"path\to\passwords.json"

#folder want to extract the files
output_folder = r"path\to\extract\output\folder"

#Extract RAR files
def extract_rar(file_path, output_folder):
    #Get the file name -> convert it to lowercase
    file_name = os.path.splitext(os.path.basename(file_path))[0].lower()

    #Check key in the json is present in the file name (lowercase)
    password = None
    for key in passwords_dict:
        if key.lower() in file_name:
            password = passwords_dict[key]
            break

    if password is not None:
        # Extraction with password
        print(f"Extracting {file_path} with password: {password}")
        file_extracted = False

        # Try extracting the file with the password, enabling file renaming if already exist
        command = [
            winrar_path,
            "x",
            "-inul",
            "-ibck",  # Automatically answer "Yes" to all prompts
            "-or",    # Rename files if already exist
            "-p" + password,
            file_path,
            output_folder
        ]
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT)
            print(f"Extraction successful for {file_path} with password: {password}")
            file_extracted = True
        except subprocess.CalledProcessError as e:
            # Check if error message contains diagnostic information
            error_output = e.output.decode().strip()
            print(f"Error occurred for {file_path}: {error_output}")

        if not file_extracted:
            error_message = f"Unable to extract {file_path} with password: {password}"
            print(error_message)
            write_to_log(error_message)
    else:
        # No corresponding password found for the file
        print(f"No password found for {file_path}. Extracting without password.")
        extract_without_password(file_path, output_folder)
        
    print()

#Extract a RAR files
def extract_zip(file_path, output_folder):
    #Get the file name -> convert it to lowercase
    file_name = os.path.splitext(os.path.basename(file_path))[0].lower()

    #Check key in the json is present in the file name (lowercase)
    password = None
    for key in passwords_dict:
        if key.lower() in file_name:
            password = passwords_dict[key]
            break

    if password is not None:
        # Extraction with password
        print(f"Extracting {file_path} with password: {password}")
        file_extracted = False

        # Try extracting the file with the password, enabling file renaming if already exist
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                zip_file.extractall(path=output_folder, pwd=password.encode())
            print(f"Extraction successful for {file_path} with password: {password}")
            file_extracted = True
        except (zipfile.BadZipFile, RuntimeError) as e:
            error_message = f"Error occurred for {file_path}: {str(e)}"
            if "Bad password" in str(e):
                print(error_message)
            else:
                print(error_message)

        if not file_extracted:
            error_message = f"Unable to extract {file_path} with password: {password}"
            print(error_message)
            write_to_log(error_message)
    else:
        # No corresponding password found for the file
        print(f"No password found for {file_path}. Extracting without password.")
        extract_zip_without_password(file_path, output_folder)

    print()  # Print a newline for better readability

# Function to extract a file without a password
def extract_without_password(file_path, output_folder):
    try:
        subprocess.check_output([winrar_path, "x", "-inul", "-ibck", "-or", file_path, output_folder])
        print(f"Extraction successful for {file_path} without password")
    except subprocess.CalledProcessError as e:
        error_message = f"Error occurred for {file_path}: {e.output.decode().strip()}"
        print(error_message)
        write_to_log(error_message)

# Function to extract a file without a password for ZIP files
def extract_zip_without_password(file_path, output_folder):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            zip_file.extractall(path=output_folder)
        print(f"Extraction successful for {file_path} without password")
    except (zipfile.BadZipFile, RuntimeError) as e:
        error_message = f"Error occurred for {file_path}: {str(e)}"
        print(error_message)
        write_to_log(error_message)

# Function to write error messages to logs.txt file
def write_to_log(error_message):
    with open("logs.txt", "a") as log_file:
        log_file.write(error_message + "\n")

# Load passwords from the JSON file
with open(passwords_file, "r") as json_file:
    passwords_dict = json.load(json_file)

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the list of compressed files
compressed_files = [
    os.path.join(compressed_files_folder, file_name)
    for file_name in os.listdir(compressed_files_folder)
    if file_name.endswith(".rar") or file_name.endswith(".zip")
]

# Set the number of threads
num_threads = 7

# Start the timer
start_time = time.time()

# Create a thread pool and map the appropriate extract function based on the file extension
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    for file in compressed_files:
        if file.endswith(".rar"):
            executor.submit(extract_rar, file, output_folder)
        elif file.endswith(".zip"):
            executor.submit(extract_zip, file, output_folder)

# Calculate the elapsed time
elapsed_time = time.time() - start_time

print(f"All files extracted or extraction failed with all passwords. Elapsed time: {elapsed_time} seconds.")
