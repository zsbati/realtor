import os
from pathlib import Path

def is_important_file(f):
    """Check if file should be included in tree."""
    # Include only .py files and important config files
    return f.endswith('.py') and not f.startswith('.') and not f.endswith('.pyc')

def generate_tree(startpath):
    print("Project Structure")
    print("=" * 50)
    
    # Only show important directories
    important_dirs = ['realtor', 'agenda', 'templates']
    
    for root, dirs, files in os.walk(startpath):
        # Skip virtual environment and other directories
        if any(d in root for d in ['venv', '__pycache__', '.git']):
            continue
            
        # Skip non-important directories
        if not any(d in root for d in important_dirs):
            continue
            
        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        # Only show directory name if it's in important_dirs
        dir_name = os.path.basename(root)
        if dir_name in important_dirs or any(d in dir_name for d in important_dirs):
            print(f"{indent}{dir_name}/")
        
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if is_important_file(f):
                print(f"{subindent}{f}")

if __name__ == "__main__":
    project_path = Path(__file__).resolve().parent
    generate_tree(project_path)
