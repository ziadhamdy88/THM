import os
import re

def visual_print(string, data):
    print(f"\n{'#'*20} {string} {'#'*20}\n")
    print(data)

# Filtering to get only non .zip files
files = list(filter(lambda x: re.search("^(?!.*\.zip$).*", x), os.listdir("./extracted/")))

# Mapping files to the directory.
files = list(map(lambda x: "./extracted/" + x, files))

file_found = False

for file in files:
    visual_print("Current File ", file)
    
    with open(file, 'rb') as reader:
        lines = reader.read().splitlines()
    
    for line in lines:

        visual_print("Line", str(line))

        if "password" in str(line):
            visual_print("File Found", file)
            
            file_found = True
            break
    
    if file_found:
        break