from .research_planner import researchPlaner
from .evidence_extractor import evidenceExtractor
from .web_search import webSearch
from .source_fetcher import SourceFetcher

class webReasercher:
    def __init__(self,search_provider=None,llm_client=None,llm_model=None,max_llm_limit=10):
        self.searcher=webSearch(search_provider)
        self.planner=researchPlaner()
        self.extractor=evidenceExtractor()
        self.fetcher=SourceFetcher()
        

    def research(self, query, depth="standard", sources=None, evidence=None):
        plan = self.planner.create_plan(
            query,
            depth
        )

        print("=== Research plan ===")
        print("query:", plan.query)
        print("goal:", plan.goal)
        print("requirements:", plan.requirments)

    
        if sources is None:
            sources = self.searcher.search(
                query,
                max_results=5
            )

            fetched_sources = []

            for source in sources:
                fetched = self.fetcher.fetch(source)

                if fetched.content:
                    fetched_sources.append(fetched)
                else:
                    fetched_sources.append(source)

            sources = fetched_sources

    
        all_claims = []

        for source in sources:
            extracted = self.extractor.extract(
                source,
                plan.query,
                plan.requirments
            )

            all_claims.extend(extracted)

        print("=== Raw claims ===")
        print("Total claims:", len(all_claims))

        for index, claim in enumerate(all_claims, start=1):
            print()
            print("Claim:", index)
            print("Text:", claim.claim)
            print("Source:", claim.source_title)
            print("URL:", claim.source_url)

        return all_claims