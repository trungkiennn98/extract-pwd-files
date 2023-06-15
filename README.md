# Xtracting - Multiple Extract Password-Protected Archive Files

Xtracting is a Python library for dealing with multiple password-contained archive files.

Practice: If you have many password-protected archived files with a list of passwords corresponding to the filename.

```json
{
    "A_name": "A_password",
    "B_name": "B_password",
    "C_name": "C_password"
}
```
The extract function is called when a corresponding password is found for compressed files.
```
|-- A_name_584ugf.rar -> A_password
|-- 564A_name_g2f.zip -> A_password
|-- A_name_9182yu.rar -> A_password
|-- 99C_name98ty.zip -> C_password
|-- B_name-19yb91.rar -> B_password
|-- 817B_namey41.rar -> B_password
|-- 115C_name124.zip -> C_password

```

Multithreading is applied to improve the extraction speed.

```
# Set the number of threads
num_threads = 3
```

Error messages are written to logs.txt.
```python
def write_to_log(error_message):
    with open("logs.txt", "a") as log_file:
        log_file.write(error_message + "\n")
```
## Installation

Use git clone to install.

```bash
git clone https://github.com/trungkiennn98/extract-pwd-files
```

## Usage

```python
# Set the path to the folder containing the compressed files
compressed_files_folder = r"path\to\compressed\folder"

# Set path for passwords.json file
passwords_file = r"path\to\passwords.json"

# Set the folder you want to extract the files
output_folder = r"path\to\extract\output\folder"
```

## Contributing

Pull requests are welcome. For significant changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
google-site-verification: googled2d3c95b08dc4e03.html
