# File Sorter

A Python application for desktops that manages both files and folders/directories. Built using Python and Tkinter, this application currently provides a graphical user interface for inspecting files, searching by extension, moving files and identifying any potential duplicates

## Features

- **Directory inspection:** Scans files, folder and sub folders using recursion/ directory and sub directories
- **File statistics:** Counts files based on their extensions
- **Extension search:** Finds files which match a specific extension, including in subdirectories
- **File movement:** Moves a selected file to a specified destination
- **Duplicate detection:** Identifies files which share names, detects common copy naming patterns and any content duplicates
- **Graphical interface:** Interactively built for desktop with a graphical user interface in Tkinter
- **Confirmation prompts:** Request user confirmation before deleting any potential duplicate files

## Language and Libraries

| Technology | Purpose |

| Python | Core application logic |
| Tkinter | Graphical user interface |
| pathlib | Filesystem navigation |
| shutil | File movement |
| re | Pattern matching |
| collections | File grouping |

## Installation

### Requirements

- Python 3.10 or later
- Tkinter (usually included with standard Python installations)

No additional third-party packages are currently required!

### Running the application

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd file-sorter
```

Run the application:

```bash
python file_sorter.py
```

## Usage

1. Launch the application.
2. Select a working directory using the 'Browse' button or paste one in
3. Choose an operation:
   - List files by extension
   - List all files
   - Find files by extension
   - Move a file
   - Delete potential copies
4. Follow prompts displayed by the application.

**Note:** when deleting, a function delete by name will be used, this does not detect if the contents of the file are similar. Just the name
## Project Structure

The application currently contains:

- File operation functions for scanning, searching, moving and identifying potential duplicates
- A `FileSorterApp` class responsible for the Tkinter interface
- A `main()` entry point that initialises the application

## Future improvements

- Automated unit testing using pytest
- Improved separation of the GUI and file-management logic
- Additional file organisation options
