import re


class KnowledgeChunker:

    def __init__(self, chunk_size=500, overlap=80):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text):
        if not text:
            return []

        text = text.strip()

        if not text:
            return []

        words = text.split()

        chunks = []
        start = 0

        while start < len(words):

            end = min(start + self.chunk_size, len(words))

            chunk = " ".join(words[start:end])

            if chunk.strip():
                chunks.append(chunk.strip())

            if end >= len(words):
                break

            start = end - self.overlap

        return chunks

    def chunk_document(self, content, file_type=None):
        if not content:
            return []

        # PDF pages
        if file_type == "pdf":
            return self.chunk_pdf(content)

        # PPT slides
        if file_type == "pptx":
            return self.chunk_slides(content)

        # Other documents
        chunks = self.chunk_text(content)

        return [
            {
                "content": chunk,
                "location": None
            }
            for chunk in chunks
        ]

    def chunk_pdf(self, content):

        pages = re.split(
            r"===pages\s*(\d+)\s*===",
            content,
            flags=re.IGNORECASE
        )

        page_sections = []

        # pages looks like:
        # ["", "1", "text", "2", "text", ...]

        i = 1

        while i < len(pages):

            page_number = pages[i]
            page_text = pages[i + 1].strip()

            if page_text:
                page_sections.append(
                    (page_number, page_text)
                )

            i += 2

        chunks = []

        current_words = []
        start_page = None
        end_page = None

        for page_number, page_text in page_sections:

            words = page_text.split()

            if not current_words:
                start_page = page_number

            current_words.extend(words)
            end_page = page_number

            while len(current_words) >= self.chunk_size:

                chunk_words = current_words[:self.chunk_size]

                chunks.append({
                    "content": " ".join(chunk_words),
                    "location": f"pages {start_page}-{end_page}"
                })

                current_words = current_words[
                    self.chunk_size - self.overlap:
                ]

                start_page = page_number

        if current_words:

            chunks.append({
                "content": " ".join(current_words),
                "location": f"pages {start_page}-{end_page}"
            })

        return chunks

    def chunk_slides(self, content):

        slides = re.split(
            r"===Slide\s*(\d+)\s*====",
            content,
            flags=re.IGNORECASE
        )

        chunks = []

        i = 1

        while i < len(slides):

            slide_number = slides[i]
            slide_text = slides[i + 1].strip()

            if slide_text:

                chunks.append({
                    "content": slide_text,
                    "location": f"slide {slide_number}"
                })

            i += 2

        return chunks
