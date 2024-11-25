from os import path

from rapidfuzz import fuzz
from werkzeug.datastructures import FileStorage

MIN_SIMILARITY = 90

def classify_file(file: FileStorage):
    filename = file.filename.lower()
    # file_bytes = file.read()

    filename_no_extention = path.splitext(filename)[0]

    if fuzz.ratio(filename_no_extention, "drivers_license") > MIN_SIMILARITY:
        return "drivers_licence"

    if fuzz.ratio(filename_no_extention, "bank_statement") > MIN_SIMILARITY:
        return "bank_statement"

    if fuzz.ratio(filename_no_extention, "invoice") > MIN_SIMILARITY:
        return "invoice"

    return "unknown file"

