import os
import shutil
from pathlib import Path

def create_project_structure():
    # Define the base project directory
    project_name = "face_recognition_attendance"
    base_dir = Path.home() / "Desktop" / project_name
    
    # Create main project directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Create subdirectories
    directories = [
        "static/css",
        "static/js",
        "templates",
        "uploads"
    ]
    
    for dir_path in directories:
        os.makedirs(base_dir / dir_path, exist_ok=True)
    
    # List of files to copy
    files_to_copy = {
        "app.py": "",
        "auth.py": "",
        "face_utils.py": "",
        "forms.py": "",
        "main.py": "",
        "models.py": "",
        "routes.py": "",
        "README.md": "",
        "pyproject.toml": "",
        "static/css/style.css": "static/css",
        "static/js/attendance.js": "static/js",
        "static/js/webcam.js": "static/js",
        "templates/404.html": "templates",
        "templates/500.html": "templates",
        "templates/attendance.html": "templates",
        "templates/base.html": "templates",
        "templates/dashboard.html": "templates",
        "templates/login.html": "templates",
        "templates/register.html": "templates",
        "templates/reports.html": "templates",
        "templates/view_history.html": "templates"
    }
    
    # Copy files
    for src_file, dest_dir in files_to_copy.items():
        src_path = Path(src_file)
        dest_path = base_dir / (dest_dir if dest_dir else "") / src_path.name
        
        if src_path.exists():
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_path} to {dest_path}")
        else:
            print(f"Warning: Source file {src_path} not found")
    
    print(f"\nProject files have been organized in: {base_dir}")
    print("\nMake sure to:")
    print("1. Set up your environment variables (FLASK_SECRET_KEY and DATABASE_URL)")
    print("2. Install the required Python packages as listed in the README.md")
    print("3. Initialize the database before running the application")

if __name__ == "__main__":
    create_project_structure()
