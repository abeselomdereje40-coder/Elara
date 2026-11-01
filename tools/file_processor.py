import os
import csv
import openpyxl
import pymupdf
import numpy as np
import cv2

from docx import Document
from pptx import Presentation
from pypdf import PdfReader


class FileProcessor:

    def __init__(self):
        self.processor = {
            ".txt": self.process_txt,
            ".pdf": self.process_pdf,
            ".docx": self.process_docx,
            ".csv": self.process_csv,
            ".xlsx": self.process_xlsx,
            ".pptx": self.process_pptx
        }

        self.ocr_engine = None

    def process(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in self.processor:
            return {
                "success": False,
                "error": f"Unsupported file type: {extension}"
            }

        try:
            return self.processor[extension](file_path)

        except Exception as e:
            return {
                "success": False,
                "error": f"{type(e).name}: {e}"
            }

    

    def get_ocr_engine(self):

        if self.ocr_engine is None:
            from rapidocr import RapidOCR
            self.ocr_engine = RapidOCR()

        return self.ocr_engine

    def extract_image_text(self, image):

        engine = self.get_ocr_engine()
        result = engine(image)

        if result is None:
            return ""

        # Support common RapidOCR result formats.
        if hasattr(result, "txts"):
            texts = result.txts or []

            return "\n".join(
                str(text).strip()
                for text in texts
                if text and str(text).strip()
            )

        if isinstance(result, tuple):
            result = result[0]

        if not result:
            return ""

        lines = []

        for item in result:

            if not item or len(item) < 2:
                continue

            text = item[1]

            if text:
                lines.append(str(text).strip())

        return "\n".join(lines)

   
    def process_txt(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return {
            "success": True,
            "type": ".txt",
            "file_path": file_path,
            "content": content
        }

    
    def process_pdf(self, file_path):

        reader = PdfReader(file_path)

        pages = []
        ocr_pages = 0
        pdf_document = None

        try:
            for page_number, page in enumerate(
                reader.pages,
                start=1
            ):

                # First try ordinary PDF text extraction.
                text = (page.extract_text() or "").strip()

                # If no text is available, try OCR.
                if not text:

                    if pdf_document is None:
                        pdf_document = pymupdf.open(file_path)

                    pdf_page = pdf_document[page_number - 1]

                    pixmap = pdf_page.get_pixmap(
                        dpi=200,
                        alpha=False
                    )

                    image_bytes = pixmap.tobytes("png")

                    image_array = np.frombuffer(
                        image_bytes,
                        dtype=np.uint8
                    )

                    image_array = cv2.imdecode(
                        image_array,
                        cv2.IMREAD_COLOR
                    )

                    if image_array is None:
                        raise RuntimeError(
                            f"Could not render PDF page {page_number}"
                        )

                    text = self.extract_image_text(
                        image_array
                    ).strip()


                    if text:
                        ocr_pages += 1

                if text:
                    pages.append(
                        f"=== Page {page_number} ===\n{text}"
                    )
                else:
                    pages.append(
                        f"=== Page {page_number} ===\n"
                        "[No readable text detected on this page.]"
                    )

        finally:
            if pdf_document is not None:
                pdf_document.close()

        content = "\n\n".join(pages)

        return {
            "success": True,
            "type": ".pdf",
            "file_path": file_path,
            "content": content,
            "page_count": len(reader.pages),
            "ocr_pages": ocr_pages
        }

    

    def process_docx(self, file_path):

        document = Document(file_path)
        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return {
            "success": True,
            "type": ".docx",
            "file_path": file_path,
            "content": "\n".join(paragraphs)
        }

   

    def process_csv(self, file_path):

        rows = []

        with open(
            file_path,
            "r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.reader(file)

            for row in reader:
                rows.append(" | ".join(row))

        return {
            "success": True,
            "type": ".csv",
            "file_path": file_path,
            "content": "\n".join(rows)
        }

    

    def process_xlsx(self, file_path):

        workbook = openpyxl.load_workbook(
            file_path,
            data_only=True
        )

        rows = []

        for sheet in workbook.worksheets:

            rows.append(f"=== Sheet: {sheet.title} ===")

            for row in sheet.iter_rows(values_only=True):

                values = [
                    str(value)
                    for value in row
                    if value is not None
                ]

                if values:
                    rows.append(" | ".join(values))

        return {
            "success": True,
            "type": ".xlsx",
            "file_path": file_path,
            "content": "\n".join(rows)
        }

    
    def process_pptx(self, file_path):

        presentation = Presentation(file_path)
        slides = []

        for slide_number, slide in enumerate(
            presentation.slides,
            start=1
        ):

            slides.append(f"=== Slide {slide_number} ===")

            for shape in slide.shapes:

                if hasattr(shape, "text"):

                    text = shape.text.strip()

                    if text:
                        slides.append(text)

        return {
            "success": True,
            "type": ".pptx",
            "file_path": file_path,
            "content": "\n".join(slides)
        }
