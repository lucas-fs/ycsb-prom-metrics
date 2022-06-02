from os import scandir
from json import load, dump

LOG_FILES_PATH = "./execution_logs"

merged_logs = []
for entry in scandir(LOG_FILES_PATH):
    if entry.is_file():
        with open(entry.path, 'r') as logfile:
            merged_logs.extend(list(load(logfile)))

with open("raw_logs_merged.json", 'w') as merged_logfile:
    dump(merged_logs, merged_logfile, indent=4, ensure_ascii=False)