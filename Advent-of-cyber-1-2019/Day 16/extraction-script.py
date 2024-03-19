import os
import zipfile
import re

def visual_print(string):
    print(f"\n{'#'*20} {string} {'#'*20}")

zip_files = ["final-final-compressed.zip"]
extracted = set()

while zip_files:
    zip_file = "./extracted/" + zip_files[0]
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall("./extracted/")
    visual_print("Working on zip file")
    print(zip_file)

    visual_print("Extracted")
    print(len(os.listdir('./extracted/')))
    
    extracted.add(zip_files[0])

    visual_print("Extracted zip files")
    print(extracted)
    
    zip_files.remove(zip_file[12:])

    zip_files = list(filter(lambda x: re.search("\.zip", x), os.listdir("./extracted/")))
    zip_files = list(filter(lambda x: x not in extracted, zip_files))

    # zip_files.extend(list_of_files)

    visual_print("Zip files")
    print(zip_files)

visual_print("Number of extracte files (excluding .zip)")
print(len(os.listdir("./extracted/")) - len(extracted))