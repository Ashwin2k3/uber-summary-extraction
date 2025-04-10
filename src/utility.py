import tempfile
import os
import re
from fastapi import Request, UploadFile
from typing import List, Tuple, Union


async def get_requested_files(request: Request, file_key: str = "file") -> Tuple[bool, str, Union[List[UploadFile], None]]:
    """Extract valid files from request."""
    form = await request.form()
    files = form.getlist(file_key)

    valid_files = [file for file in files if file.filename.strip()]
    if not valid_files:
        return False, "No valid files uploaded.", None
    
    return True, "success", valid_files

def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """Save uploaded files to a temporary directory and return their paths."""
    file_paths = []
    temp_dir = tempfile.mkdtemp()

    for pdf_file in files:
        file_path = os.path.join(temp_dir, pdf_file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(pdf_file.file.read())
        file_paths.append(file_path)
    
    return file_paths


# added changes in post_process_cin 
def post_process_cin(cin):
    """
    Replaces specific alphabets with corresponding digits in:
    1. First 5 characters (index 1-5).
    2. Middle 4 characters (index 8-11).
    3. Last 6 characters of the CIN.
    """
    replacements = {'O': '0', 'I': '1', 'Z': '2', 'S': '5', 'B': '8'}

    if len(cin) < 21:
        return cin  # Return the original CIN if it's less than 21 characters long
    
    # Function to replace characters based on the dictionary
    def replace_chars(segment):
        return ''.join(replacements.get(char, char) for char in segment)

    # First 5 characters (index 1-5)
    if len(cin) >= 6:
        cin = cin[0] + replace_chars(cin[1:6]) + cin[6:]

    # Middle 4 characters (index 8-11)
    if len(cin) >= 12:
        cin = cin[:8] + replace_chars(cin[8:12]) + cin[12:]

    # Last 6 characters
    cin = re.sub(r'(\w{6})$', lambda m: replace_chars(m.group()), cin)

    return cin

def post_processing(structured_data):

    # Check if structured_data is already a list
    if not isinstance(structured_data, list):
        raise ValueError("structured_data must be a list of lists!")

    for group in structured_data:  # Directly iterate over the list
        if not isinstance(group, list):
            raise ValueError("Each group inside structured_data must be a list!")

        for record in group:
            if not isinstance(record, dict) or "CIN" not in record:
                continue  # Skip invalid records

            # Remove special characters from "CIN"
            clean_cin = re.sub(r'[^a-zA-Z0-9]', '', record["CIN"])
            record["CIN"] = post_process_cin(clean_cin)  # Apply CIN processing

    return structured_data