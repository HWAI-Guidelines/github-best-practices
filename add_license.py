import os
import json

# Define the copyright text
license_text = "All content, trademarks, and data on this document are the property of Healthworks Analytics, LLC and are protected by applicable intellectual property laws. Unauthorized use, reproduction, or distribution of this material is strictly prohibited."

# Define the directory where your repository is located
repo_dir = '.'  # Use the relative path for GitHub Actions

# Define the file extensions and their respective comment styles
file_comment_styles = {
    '.py': '#', '.js': '//', '.jsx': '//', '.ts': '//', '.tsx': '//',
    '.html': '<!--', '.css': '/*', '.scss': '/*',
    '.yaml': '#', '.yml': '#', '.sh': '#', '.bat': 'REM', '.env': '#',
    '.cs': '//', '.csproj': '<!--', '.vb': "'", 'Dockerfile': '#',
    '.sql': '--', '.ps1': '#', '.config': '<!--', '.xml': '<!--',
    '.xaml': '<!--', '.php': '//', '.rb': '#', '.go': '//',
    '.java': '//', '.kt': '//', '.c': '//', '.cpp': '//', '.h': '//',
    '.swift': '//', '.pynb': '#', '.jsx': '//'
}

# Function to generate the license header
def generate_license_header(comment_style):
    if comment_style in ['#', '//', '--', 'REM']:
        return f"{comment_style} {license_text}\n"
    elif comment_style in ['<!--']:
        return f"{comment_style} {license_text} -->\n"
    elif comment_style in ['/*']:
        return f"{comment_style} {license_text} */\n"
    else:
        raise ValueError("Unsupported comment style")

# Function to add a license to text-based files
def add_license_to_text_file(file_path, comment_style):
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            license_header = generate_license_header(comment_style)
            # Ensure the license header is added only if it's not already present
            if not content.startswith(license_header):
                file.seek(0, 0)
                file.write(license_header + content)
                print(f"Added license header to {file_path}")
    except Exception as e:
        print(f"Failed to add license header to {file_path}: {e}")

# Function to add a license to JSON files
def add_license_to_json_file(file_path):
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = json.load(file)
            file.seek(0)
            file.truncate()
            json.dump(content, file, indent=4)
            file.write(f"\n// {license_text}\n")
            print(f"Added license header to {file_path}")
    except Exception as e:
        print(f"Failed to add license header to {file_path}: {e}")

# Walk through the directory
for root, dirs, files in os.walk(repo_dir):
    for file in files:
        # Skip README.md and add_license.py
        if file in ['README.md', 'add_license.py']:
            continue
        file_path = os.path.join(root, file)
        if file.endswith('.json') or file == 'package.json':
            add_license_to_json_file(file_path)
        else:
            for ext, comment_style in file_comment_styles.items():
                if file.endswith(ext) or file.lower() == 'dockerfile':
                    add_license_to_text_file(file_path, comment_style)
                    break

#print("All files have been updated.")
