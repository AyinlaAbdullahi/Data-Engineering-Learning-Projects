from pathlib import Path

log_file=Path("app.log")

if not log_file.exists():
    raise FileNotFoundError("Log file does not exist!")

log_counts={
    "INFO": 0,
    "WARNING": 0,
    "ERROR": 0, 
}

with log_file.open() as file:
    for line in file:
        line=line.strip()
        
        if not line:
            continue
        
        parts=line.split()
        
        for part in parts:
            if part in log_counts:
                log_counts[part] += 1
                
print("Log summary")
print("-----------")
for level, count in log_counts.items():
    print(f"{level}; {count}")


        