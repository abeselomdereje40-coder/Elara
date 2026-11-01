from typing import List
from ..web_models import searchResult
from ddgs import DDGS
from urllib.parse import urlparse

class DDGSPovider:
    def __init__(self):
        self.client=DDGS()

    def search(self,query,max_results=5)->List[searchResult]:
        try:
            raw_results=self.client.text(
                query,
                max_results=max_results
            )
            results=[]

            for index,item in enumerate(raw_results):
                url=item.get("href","")
                domain=urlparse(url).netloc
                score=max(
                    0.0,
                    1.0-(index*0.05)
                )
                results.append(
                    searchResult(
                        title=item.get("title",""),
                        url=url,
                        content=item.get("body",""),
                        score=score,
                        domain=domain
                    )
                )

            return results

        except Exception as e:
            print("DDGS search error:",e)
            raise