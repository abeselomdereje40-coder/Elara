from .web_models import ResearchRequest

class researchPlaner:
    def create_plan(self,query,depth="standard"):
        requirments=[]
        if depth=="quick":
            requirments=[
                "main answer",
                "authoritative source"
            ]

        elif depth=="deep":
            requirments=[
                "main answer",
                "detailed information",
                "multiple sources",
                "offical sources",
                "supporting evidence",
                "conflicting information"
            ]

        else:
            requirments=[
                "main answer",
                "important details",
                "multiple reliable sources",
                "supporting evidence"
            ]

        return ResearchRequest(
            query=query,
            depth=depth,
            goal=query,
            requirments=requirments
        )