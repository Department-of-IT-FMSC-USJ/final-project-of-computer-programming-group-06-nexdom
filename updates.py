import os

# The directory to search (current directory)
root_dir = "."

# Target string and its replacement
target = "use_container_width=True"
replacement = "width='stretch'"

print(f"{'File Path':<50} | {'Line':<5}")
print("-" * 60)

for subdir, dirs, files in os.walk(root_dir):
    # Skip the venv and __pycache__ folders to save time
    if 'venv' in subdir or '__pycache__' in subdir:
        continue
        
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(subdir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for i, line in enumerate(lines):
                    if target in line:
                        print(f"{file_path:<50} | {i+1}")
            except Exception as e:
                print(f"Could not read {file_path}: {e}")