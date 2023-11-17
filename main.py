import urllib.parse
import re
import urllib3

from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel, field_validator, conlist
from bs4 import BeautifulSoup
import random
import concurrent.futures

app = FastAPI()


class SearchParameters(BaseModel):
    keywords: conlist(str, min_length=1)
    proxies: conlist(str, min_length=1)
    search_type: str

    @field_validator("keywords")
    def validate_keywords(cls, value):
        if not value:
            raise ValueError("Keywords cannot be empty")
        if not all(isinstance(keyword, str) for keyword in value):
            raise ValueError("Keywords should be a list of strings")
        return value

    @field_validator("proxies")
    def validate_proxies(cls, value):
        if not value:
            raise ValueError("Proxies cannot be empty")
        if not all(
            isinstance(proxy, str) and re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy)
            for proxy in value
        ):
            raise ValueError("Proxies should be a list of strings with the format 'ip_address:port'")
        return value

    @field_validator("search_type")
    def validate_search_type(cls, value):
        allowed_search_types = ["Repositories", "Issues", "Wikis"]
        if value and value not in allowed_search_types:
            raise ValueError(f"Invalid search type. Allowed types are {', '.join(allowed_search_types)}")
        return value


def get_main_page_links(soup):
    # List of boxes that contain search result
    result_div_list = soup.find("div", {"data-hpc": True})

    # This is class name for a tag that contains relative link
    a_class_name = "Link__StyledLink-sc-14289xe-0 fIqerb"
    result_links = [a["href"] for a in result_div_list.find_all("a", {"class": a_class_name}, href=True)]

    # Convert relative links to absolute links as they are relative
    result_links = [{"url": urllib.parse.urljoin("https://github.com", link)} for link in result_links]
    return result_links


def get_proxy(parameters=Body()):
    proxies = parameters.get("proxies", ["127.0.0.1:80"])
    proxy = random.choice(proxies) if proxies else "127.0.0.1:80"
    proxy_url = urllib.parse.urljoin("http://", proxy)
    http = urllib3.ProxyManager(proxy_url)
    return http


def get_repo_details(proxy, url_dict):
    html = proxy.request("GET", url_dict["url"])
    soup = BeautifulSoup(html.data, "html.parser")
    a_tag_name = "Repository, language stats search click, location:repo overview"
    language_list = soup.find_all("a", {"data-ga-click": a_tag_name})
    all_language_stats = []
    for language in language_list:
        language_stats = language.find_all("span")
        all_language_stats.append({language_stats[0].text: language_stats[1].text})

    author = soup.find("a", {"rel": "author"}).text.strip()
    url_dict.update({"extra": {"language_stats": all_language_stats, "owner": author}})


@app.post("/get_github_links")
def get_github_info(parameters: SearchParameters, proxy=Depends(get_proxy)):
    """
    Get search results for query from GitHub
    - **keywords**: List of keywords to search by
    - **proxies**: List of proxies IP-addresses
    - **type**: Type of search
    """
    search_query = urllib.parse.quote_plus("".join(parameters.keywords))
    url = urllib.parse.urljoin("https://github.com/search", f"?q={search_query}&type={parameters.search_type}")

    html = proxy.request("GET", url)
    soup = BeautifulSoup(html.data, "html.parser")

    result = get_main_page_links(soup)
    if parameters.search_type == "Repositories" and result:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(result)) as executor:
            futures = [executor.submit(get_repo_details, proxy, link_dict) for link_dict in result]
            concurrent.futures.wait(futures)

    return result
