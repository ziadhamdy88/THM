import os
import re
from pyexiftool import exiftool

def visual_print(string, data):
    print(f"\n{'#'*20} {string} {'#'*20}\n")
    print(data)

# Filtering to get only non .zip files
files = list(filter(lambda x: re.search("^(?!.*\.zip$).*", x), os.listdir("./extracted/")))

visual_print("Filtered Files", files)

# Mapping files to the directory.
files = list(map(lambda x: "./extracted/" + x, files))

visual_print("Mapped Files", files)

with exiftool.ExifTool() as et:
    metadata = et.get_metadata_batch(files)

version_count = 0

for d in metadata:
    visual_print("New Entry", d)

    if "XMP:Version" in d:
        version_count += 1

visual_print("Version Count", version_count)