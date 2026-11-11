from pathlib import Path
from collections import defaultdict
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def movefiles(directory, file_name, new_directory):
    #moves a files from one folder to another
    old_file = Path(directory) / file_name
    destination = Path(new_directory)

    if not old_file.is_file():
        return False, f"Not a valid file: {old_file}"
    if not destination.is_dir():
        return False, f"Invalid destination directory: {destination}"

    try:
        shutil.move(str(old_file), str(destination / old_file.name))
    except OSError as error:
        return False, f"Error moving file: {error}"
    return True, f"Moved {old_file.name} successfully."


def extension(directory, extension_name):
    #returns all files with the requested extension
    normalized_extension = extension_name.strip().lstrip(".")
    if not normalized_extension:
        return []

    pattern = f"*.{normalized_extension}"
    try:
        return [file for file in Path(directory).rglob(pattern) if file.is_file()]
    except OSError:
        return []


def listFiles(directory):
    #returns a count of files by extension
    file_types = {}
    try:
        files = Path(directory).rglob("*")
        for file in files:
            if file.is_file():
                file_types[file.suffix or "[no extension]"] = (
                    file_types.get(file.suffix or "[no extension]", 0) + 1
                )
    except OSError:
        return {}
    return dict(sorted(file_types.items()))


def basicListFiles(directory):
    #return every file in the directory and its sub directories
    try:
        return sorted(
            (file for file in Path(directory).rglob("*") if file.is_file()),
            key=lambda file: str(file).lower(),
        )
    except OSError:
        return []


def deleteFilesByName(directory, confirm):
    #Asking to delete the files found by similar name keeping the first one found
    file_map = defaultdict(list)
    for file in basicListFiles(directory):
        file_map[file.name].append(file)

    deleted = 0
    for name, locations in sorted(file_map.items()):
        if len(locations) < 2:
            continue
        for duplicate in locations[1:]:
            if confirm(
                "Delete duplicate?",
                f"Delete duplicate named '{name}'?\n\n{duplicate}",
            ):
                try:
                    duplicate.unlink()
                    deleted += 1
                except OSError:
                    continue
    return deleted


def deleteFilesByPattern(directory, confirm):
    #looks for copy patterns e.g. (test (1).txt or test - copy.txt) and asks to delete them
    copy_pattern = re.compile(r"^(.*?)(?: \(\d+\)| - Copy)+(\.[^.]+)?$")
    deleted = 0
    for file in basicListFiles(directory):
        match = copy_pattern.match(file.stem + file.suffix)
        if not match:
            continue
        original_path = file.parent / (match.group(1) + (match.group(2) or ""))
        if not original_path.is_file():
            continue
        if confirm(
            "Delete copied file?",
            f"Delete this copy?\n\n{file}\n\nOriginal:\n{original_path}",
        ):
            try:
                file.unlink()
                deleted += 1
            except OSError:
                continue
    return deleted


# keeping old script name
deleteFilesByPatterns = deleteFilesByPattern


class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)

        self.directory = tk.StringVar()
        self.extension_name = tk.StringVar()
        self.file_name = tk.StringVar()
        self.destination = tk.StringVar()
        self.status = tk.StringVar(value="Choose a directory to get started.")

        self._build_interface()

    def _build_interface(self):
        directory_frame = ttk.LabelFrame(self.root, text="Working directory", padding=10)
        directory_frame.pack(fill="x", padx=10, pady=(10, 5))
        directory_frame.columnconfigure(0, weight=1)

        ttk.Entry(directory_frame, textvariable=self.directory).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(directory_frame, text="Browse...", command=self.choose_directory).grid(
            row=0, column=1
        )
        ttk.Button(directory_frame, text="Set directory", command=self.validate_directory).grid(
            row=0, column=2, padx=(6, 0)
        )

        actions = ttk.LabelFrame(self.root, text="File operations", padding=10)
        actions.pack(fill="x", padx=10, pady=5)

        ttk.Button(actions, text="List files by extension", command=self.show_file_counts).grid(
            row=0, column=0, padx=4, pady=4
        )
        ttk.Button(actions, text="List all files", command=self.show_all_files).grid(
            row=0, column=1, padx=4, pady=4
        )
        ttk.Button(actions, text="Find files by extension", command=self.find_by_extension).grid(
            row=0, column=2, padx=4, pady=4
        )
        ttk.Button(actions, text="Move a file", command=self.move_file).grid(
            row=0, column=3, padx=4, pady=4
        )
        ttk.Button(actions, text="Delete copies", command=self.delete_copies).grid(
            row=0, column=4, padx=4, pady=4
        )
        ttk.Button(actions, text="Clear output", command=self.clear_output).grid(
            row=0, column=5, padx=4, pady=4
        )

        ttk.Label(self.root, textvariable=self.status, anchor="w").pack(
            fill="x", padx=12, pady=(5, 0)
        )
        output_frame = ttk.LabelFrame(self.root, text="Results", padding=6)
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.output = tk.Text(output_frame, wrap="none", state="disabled")
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(output_frame, command=self.output.yview)
        scrollbar.pack(side="right", fill="y")
        self.output.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.root, text="Exit", command=self.root.destroy).pack(
            anchor="e", padx=10, pady=(0, 10)
        )

    def choose_directory(self):
        selected = filedialog.askdirectory(title="Choose a working directory")
        if selected:
            self.directory.set(selected)
            self.validate_directory()

    def get_directory(self):
        directory = Path(self.directory.get().strip())
        if not directory.is_dir():
            messagebox.showerror("Invalid directory", "Please enter or choose a valid directory.")
            return None
        return directory

    def validate_directory(self):
        directory = Path(self.directory.get().strip())
        if directory.is_dir():
            self.status.set(f"Working directory: {directory}")
            return True
        messagebox.showerror("Invalid directory", "Please enter or choose a valid directory.")
        return False

    def show_file_counts(self):
        directory = self.get_directory()
        if directory is None:
            return
        counts = listFiles(directory)
        self.clear_output()
        if not counts:
            self.write_output("No files found.")
        else:
            self.write_output("\n".join(f"{suffix}: {count}" for suffix, count in counts.items()))
        self.status.set(f"Found {sum(counts.values())} file(s).")

    def show_all_files(self):
        directory = self.get_directory()
        if directory is None:
            return
        files = basicListFiles(directory)
        self.clear_output()
        self.write_output("\n".join(str(file) for file in files) or "No files found.")
        self.status.set(f"Found {len(files)} file(s).")

    def find_by_extension(self):
        directory = self.get_directory()
        extension_name = self.extension_name.get().strip()
        if directory is None:
            return
        if not extension_name:
            extension_name = self.ask_for_extension()
        if not extension_name:
            return
        self.extension_name.set(extension_name)
        files = extension(directory, extension_name)
        self.clear_output()
        self.write_output("\n".join(str(file) for file in files) or "No matching files found.")
        self.status.set(f"Found {len(files)} .{extension_name.lstrip('.')} file(s).")

    def ask_for_extension(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Find by extension")
        dialog.transient(self.root)
        dialog.grab_set()
        value = tk.StringVar()
        result = []
        ttk.Label(dialog, text="Extension (for example: txt):").pack(padx=10, pady=(10, 3))
        entry = ttk.Entry(dialog, textvariable=value)
        entry.pack(padx=10, pady=3)
        entry.focus_set()

        def accept():
            result.append(value.get())
            dialog.destroy()

        ttk.Button(dialog, text="Search", command=accept).pack(pady=(3, 10))
        self.root.wait_window(dialog)
        return result[0] if result else ""

    def move_file(self):
        directory = self.get_directory()
        if directory is None:
            return
        file_name = self.file_name.get().strip()
        if not file_name:
            file_name = filedialog.askopenfilename(
                title="Choose a file to move", initialdir=str(directory)
            )
            if not file_name:
                return
            file_name = Path(file_name).name
        destination = self.destination.get().strip()
        if not destination:
            destination = filedialog.askdirectory(title="Choose a destination directory")
        if not destination:
            return
        success, message = movefiles(directory, file_name, destination)
        if success:
            self.file_name.set("")
            self.clear_output()
            self.write_output(message)
            self.status.set(message)
        else:
            messagebox.showerror("Move failed", message)
            self.status.set(message)

    def delete_copies(self):
        directory = self.get_directory()
        if directory is None:
            return
        if not messagebox.askyesno(
            "Delete copies",
            "This will look for duplicate names and common copy patterns.\n"
            "You will be asked about each file. Continue?",
        ):
            return
        deleted_by_name = deleteFilesByName(directory, messagebox.askyesno)
        deleted_by_pattern = deleteFilesByPattern(directory, messagebox.askyesno)
        deleted = deleted_by_name + deleted_by_pattern
        self.clear_output()
        self.write_output(
            f"Deleted {deleted} file(s): "
            f"{deleted_by_name} duplicate name(s), "
            f"{deleted_by_pattern} copy pattern(s)."
        )
        self.status.set(f"Deleted {deleted} file(s).")

    def write_output(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

def main():
    root = tk.Tk()
    FileSorterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
