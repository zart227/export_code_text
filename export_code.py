import os

# Parameters
EXCLUDE_DIRS = [
    "vendor",
    "storage",
    "bootstrap",
    "config",
    "database",
    "public",
    "resources",
    "routes",
    "tests",
    "__pycache__",
    "node_modules",
]  # Directories to exclude
EXCLUDE_FILES = [
    "artisan",
    "composer.json",
    "composer.lock",
    "package.json",
    "webpack.mix.js",
    "yarn.lock",
    "phpunit.xml",
    os.path.basename(__file__),
]  # Files to exclude
CHAR_LIMIT = 20000  # Maximum number of characters in one file
ROOT_DIR = "."  # Root directory of the project
OUTPUT_FILE_PREFIX = "project_code"  # Prefix for output files

# Additional files to process
INCLUDE_EXTENSIONS = [".php", ".js", ".vue", ".html", ".css", ".scss"]  # File extensions to process

def print_tree_structure(root_dir, exclude_dirs, exclude_files, include_extensions):
    """Print the project structure as a tree."""

    def walk_dir(dir_path, prefix=""):
        dirnames = []
        filenames = []
        for entry in sorted(os.listdir(dir_path)):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                if entry not in exclude_dirs:
                    dirnames.append(entry)
            elif os.path.isfile(full_path):
                if (
                    any(entry.endswith(ext) for ext in include_extensions)
                    and entry not in exclude_files
                ):
                    filenames.append(entry)

        # Print directories
        for i, dirname in enumerate(dirnames):
            is_last = i == len(dirnames) - 1 and not filenames
            print(f"{prefix}├── {dirname}/")
            new_prefix = prefix + ("│   " if not is_last else "    ")
            walk_dir(os.path.join(dir_path, dirname), new_prefix)

        # Print files
        for i, filename in enumerate(filenames):
            is_last = i == len(filenames) - 1
            print(f"{prefix}└── {filename}")

    print(f"{os.path.basename(os.path.abspath(root_dir))}/")
    walk_dir(root_dir, prefix="  ")

def write_code_to_files(
    root_dir,
    exclude_dirs,
    exclude_files,
    include_extensions,
    char_limit,
    output_file_prefix,
):
    """Write the project code to text files."""
    file_count = 1
    char_count = 0
    current_file_path = f"{output_file_prefix}_{file_count}.txt"
    current_file = open(current_file_path, "w", encoding="utf-8")

    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude directories
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

            for filename in filenames:
                if filename in exclude_files or not any(
                    filename.endswith(ext) for ext in include_extensions
                ):
                    continue

                # Full path and relative path
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, root_dir)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()

                    # Add relative path and file content
                    content = f"# {relative_path}\n{code}\n\n"
                    if char_count + len(content) > char_limit:
                        # Close the current file and open a new one
                        current_file.close()
                        file_count += 1
                        current_file_path = f"{output_file_prefix}_{file_count}.txt"
                        current_file = open(current_file_path, "w", encoding="utf-8")
                        char_count = 0

                    current_file.write(content)
                    char_count += len(content)

                except Exception as e:
                    print(f"Error reading file {relative_path}: {e}")

    finally:
        current_file.close()
        print(f"Project code written to {file_count} file(s).")

# Print project structure
print("Project structure:")
print_tree_structure(ROOT_DIR, EXCLUDE_DIRS, EXCLUDE_FILES, INCLUDE_EXTENSIONS)

# Write code to files
write_code_to_files(
    ROOT_DIR,
    EXCLUDE_DIRS,
    EXCLUDE_FILES,
    INCLUDE_EXTENSIONS,
    CHAR_LIMIT,
    OUTPUT_FILE_PREFIX,
)
