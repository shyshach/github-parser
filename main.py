import urllib.parse
import urllib3

from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel
from bs4 import BeautifulSoup
import random
import concurrent.futures

app = FastAPI()


class SearchParameters(BaseModel):
    keywords: list
    proxies: list
    search_type: str


def get_main_page_links(soup):
    # List of boxes that contain search result
    result_div_list = soup.find("div", {"data-hpc": True})

    # This is class name for a tag that contains relative link
    a_class_name = "Link__StyledLink-sc-14289xe-0 fIqerb"
    result_links = [a["href"] for a in result_div_list.find_all("a", {"class": a_class_name}, href=True)]

    # Convert relative links to absolute links as they are relative
    result_links = [{"url": "https://github.com" + link} for link in result_links]
    return result_links


def get_proxy(parameters=Body()):
    http = urllib3.PoolManager()
    return http
    proxy = random.choice(parameters.proxies)
    http = urllib3.ProxyManager(f"http://{proxy}")
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
async def get_github_info(parameters: SearchParameters, proxy=Depends(get_proxy)):
    """
    Get search results for query from GitHub
    - **keywords**: List of keywords to search by
    - **proxies**: List of proxies IP-addresses
    - **type**: Type of search
    """
    search_query = urllib.parse.quote_plus("".join(parameters.keywords))
    url = f"https://github.com/search?q={search_query}&type={parameters.search_type}"

    html = proxy.request("GET", url)
    soup = BeautifulSoup(html.data, "html.parser")

    result = get_main_page_links(soup)
    if parameters.search_type == "Repositories":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(get_repo_details, proxy, link_dict) for link_dict in result]
            concurrent.futures.wait(futures)

    return result
