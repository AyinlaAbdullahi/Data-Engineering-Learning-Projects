from pathlib import Path

base_dir = Path.home() / "Documents" / "unorgFolder"

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".tar"],
}

for folder in list(categories.keys()) + ["others"]:
    (base_dir/folder).mkdir(exist_ok=True)
    
for file in base_dir.iterdir():
    if file.is_file():
        for folder, extensions in categories.items():
            if file.suffix.lower() in extensions:
                file.rename(base_dir/folder/file.name)
                break
        else:
            file.rename(base_dir/"others"/file.name)
                
print("Done organizing files.")