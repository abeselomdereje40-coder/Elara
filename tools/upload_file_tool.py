from tools.file import run_upload_file
from tools.file_processor import FileProcessor
from tools.knowledge_chunker import KnowledgeChunker
from tools.embedding_model import EmbeddingModel


class UploadFileTool:

    def __init__(self, memory):

        self.processor = FileProcessor()
        self.chunker = KnowledgeChunker()
        self.embedder = EmbeddingModel()
        self.memory = memory

    def run(self):

        try:

            file_result = run_upload_file()

            if not file_result["selected"]:
                return file_result

            file_path = file_result["file_path"]


            processed = self.processor.process(file_path)

            if not processed["success"]:
                error = processed.get("error", "Unknown processing error")

                return {
                    "success": False,
                    "selected": True,
                    "error": error,
                    "file_name": file_result["file_name"]
                }

            title = file_result["file_name"]
            content = processed["content"]
            extension = file_result["extension"]


            if not content.strip():
                return {
                    "success": False,
                    "selected": True,
                    "error": "No text was extracted from the document."
                }


            knowledge_id = self.memory.save_knowledge(
                title=title,
                content=content,
                source=file_path,
                tags=extension
            )

            if knowledge_id is None:
                raise RuntimeError(
                    "save_knowledge() did not return a knowledge ID."
                )


            chunks = self.chunker.chunk_document(
                content,
                processed["type"]
            )

            if not chunks:
                raise RuntimeError(
                    "The document was saved, but no knowledge chunks were created."
                )

            texts = [
                chunk["content"]
                for chunk in chunks
            ]


            embeddings = self.embedder.embed_documents(texts)


            self.memory.save_knowledge_chunks(
                knowledge_id,
                chunks,
                embeddings
            )

            return {
                "success": True,
                "selected": True,
                "knowledge_id": knowledge_id,
                "file_path": file_path,
                "file_name": title,
                "extension": extension,
                "type": processed["type"],
                "content": content,
                "chunk_count": len(chunks)
            }

        except Exception as e:

            error = f"{type(e).name}: {e}"

            return {
                "success": False,
                "error": error
            }