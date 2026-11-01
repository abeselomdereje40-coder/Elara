from tkinter import filedialog
import os

def run_upload_file():
    file_path=filedialog.askopenfilename(
        title="Select a file"
    )

    if not file_path:
        return {
            "selected":False,
            "message":"No file selected."
        }

    file_name=os.path.basename(file_path)
    extension=os.path.splitext(file_path)[1].lower()

    return {
        "selected": True,
        "file_path":file_path,
        "file_name":file_name,
        "extension":extension
    }