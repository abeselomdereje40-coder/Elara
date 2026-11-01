from .web_models import Evidence

class evidenceExtractor:
    def extract(self,source,query="",requirments=None):
        requirments=requirments or []
        evidence=[]
        if not source.content:
            return evidence

        query_words={
            word.lower().strip(".,?!():;\"'")
            for word in query.split()
            if len(word)>3
        }
        
        sentences=[
            sentence.strip()
            for sentence in source.content.replace("\n","").split(".")
            if sentence.strip()
        ]

        candidates=[]

        for sentence in sentences:
            if len(sentence)<40:
                continue
            sentence_word={
                word.lower().strip(".,?!():;\"'")
                for word in sentence.split()
                if len(word)>3
            }
            command_word=query_words.intersection(sentence_word)

            if command_word:
                candidates.append(sentence)

            candidates=candidates[:20]

        for sentence in candidates:
            evidence.append(
                Evidence(
                    claim=sentence,
                    evidence=sentence,
                    source_url=source.url,
                    source_title=source.title,
                    confidence="unknown",
                    verified=False
                )
            )
        return evidence