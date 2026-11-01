from .web_models import searchResult
import requests
from bs4 import BeautifulSoup

class SourceFetcher:
    def __init__(self,timeout=10):
        self.timeout=timeout

    def fetch(self,results:searchResult)->searchResult:
        try:
            response=requests.get(
                results.url,
                timeout=self.timeout,
                headers={
                    "User-Agent":(
                        "Mozilla/5.0"
                        "(Window NT 10.0;Win64; x64)"
                        "AppleWebKit/537.36"
                        "(KHTML, like Gecko)"
                        "Chrome/120.0 Safari/537.36"
                    )
                }
            )
            response.raise_for_status()
            soup=BeautifulSoup(
                response.text,
                "html.parser"
            )
            for element in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside"
            ]):
                element.decompose()
            content=(
                soup.find("article")
                or soup.find("main")
                or soup.find("body")
            )
            if content:
                text=content.get_text(
                    separator=" ",
                    strip=True
                )
            else:
                text=""

            return searchResult(
                title=results.title,
                url=results.url,
                content=text,
                score=results.score,
                domain=results.domain
            )

        except requests.RequestException:
            return searchResult(
                title=results.title,
                url=results.url,
                content="",
                score=results.score,
                domain=results.domain
            )
