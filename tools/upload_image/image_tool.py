from tkinter import filedialog
from rapidocr import RapidOCR
import os


# Create OCR engine once
ocr = RapidOCR()


def upload_image(kwargs=None):
    """
    Select an image and extract text from it using OCR.
    """

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        return {
            "selected": False,
            "message": "No image selected."
        }

    try:
        # Run OCR
        result = ocr(file_path)

        # RapidOCR returns OCR results
        extracted_text = []

        if result.txts:
            extracted_text = result.txts

        text = "\n".join(extracted_text)

        return {
            "selected": True,
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "text": text
        }

    except Exception as e:
        return {
            "selected": True,
            "file_path": file_path,
            "error": str(e)
        }