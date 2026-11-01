from .web_models import searchResult

class webSearch:
    def __init__(self,provider=None):
        self.provider=provider

    def search(self,query,max_results=5):
        """
        search web.
        returns:
        List[serachResult]
        """
        if self.provider is None:
            return RuntimeError("Web search provider is not set.")

        results=self.provider.search(
            query,
            max_results=max_results
        )
        if not isinstance(results,list):
            return TypeError(
                "Web search provider returned"
                f"{type(results)} instead of the expected List[searchResult]."
            )

        valid_results=[]
        for result in results:
            if isinstance(result,searchResult):
                valid_results.append(result)

        return valid_results