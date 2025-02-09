import requests
import re
from bs4 import BeautifulSoup

class MetabaseFetcher:
    """
    Class to fetch and extract various kinds of data from the Metabase website.
    It does preprocessing of scrapped data to make the data in decent shape for creating embeddings.
    """
    def fetch_and_extract(self, url: str) -> str:
        """
        Metabase stores most of its content inside 'learn__post__content' in its DOM.
        """
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        content_div = soup.find("div", class_="learn__post__content")
        if not content_div:
            raise ValueError("Content div not found")
        
        raw_text = content_div.get_text(separator="\n", strip=True)
        clean_text = re.sub(r'\n+', '\n', raw_text)
        return clean_text

    def fetch_expressions_data(self) -> str:
        """
        Fetch expression-related data from multiple Metabase pages.
        """
        base_url = "https://www.metabase.com/docs/latest/questions/query-builder/"
        urls = [base_url + "expressions", base_url + "expressions-list"]
        full_text = ""
        for url in urls:
            full_text += self.fetch_and_extract(url) + "\n"
        return full_text

