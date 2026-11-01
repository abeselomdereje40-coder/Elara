import os

class promptLoader:

    def load(self):
        files=[
            "identity.md",
            "general_rules.md",
            "memory_rules.md",
            "project_rules.md",
            "coding_rules.md",
            "response_rules.md",
            "elara_philosophy.md"
        ]
        sections=[]
        for file in files:
            if os.path.exists(file):
                with open(file,"r",encoding="utf-8") as f:
                    sections.append(f.read())

        return "\n\n".join(sections)
