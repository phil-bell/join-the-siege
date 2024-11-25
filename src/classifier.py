from os import path

from rapidfuzz import fuzz
from werkzeug.datastructures import FileStorage

MIN_SIMILARITY = 90
FILE_CLASSES = {
    "drivers_licence",
    "bank_statement",
    "invoice",
}

def classify_file(file: FileStorage):
    filename = file.filename.lower()
    # file_bytes = file.read()

    filename_no_extention = path.splitext(filename)[0]

    for file_class in FILE_CLASSES:
        if fuzz.ratio(filename_no_extention, file_class) > MIN_SIMILARITY:
            return file_class

    return "unknown file"

