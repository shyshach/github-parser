import pytest
import urllib3

from main import app, get_proxy, get_repo_details, get_main_page_links, get_github_info
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def mock_proxy_manager(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_beautiful_soup(mocker):
    return mocker.patch("main.BeautifulSoup")


def test_get_github_info_with_dependency(mocker):
    mock_proxy = mocker.Mock()
    mocker.patch("main.get_proxy", return_value=mock_proxy)
    mock_proxy.request.return_value = mocker.Mock(data="")

    with mocker.patch("main.BeautifulSoup") as mock_beautiful_soup:
        mock_beautiful_soup_instance = mocker.Mock()
        mock_beautiful_soup_instance.find.return_value = mocker.Mock()
        mock_beautiful_soup_instance.find_all.return_value = [mocker.Mock(href="https://github.com/test")]
        mocker.patch("main.get_main_page_links", return_value=["test"])
        res = get_github_info(
            mocker.Mock(search_type="Repositories", proxies=["127.0.0.1"], keywords=["1", "2"]), mock_proxy
        )
    assert res == ["test"]


def test_get_proxy(mocker):
    mock_proxy_manager = mocker.patch("main.urllib3.ProxyManager")
    get_proxy({"keywords": "test", "proxies": ["proxy1", "proxy2"], "search_type": "Repositories"})
    mock_proxy_manager.assert_called_once()


def test_get_repo_details(mocker):
    mocker.patch("main.urllib3.ProxyManager")
    mock_beautiful_soup = mocker.patch("main.BeautifulSoup")
    mock_beautiful_soup_instance = mock_beautiful_soup.return_value
    mock_beautiful_soup_instance.find_all.return_value = []
    url_dict = {"url": "https://github.com/example"}
    proxy = urllib3.ProxyManager("")
    get_repo_details(proxy, url_dict)
    assert "extra" in url_dict


def test_get_main_page_links(mocker):
    soup_mock = mocker.Mock()
    soup_mock.find.return_value = mocker.Mock()
    soup_mock.find.return_value.find_all.return_value = [{"href": "/test"}]
    res = get_main_page_links(soup_mock)
    assert res == [{"url": "https://github.com/test"}]


def test_empty_keywords():
    response = client.post("/get_github_links", json={"keywords": [1], "proxies": ["1"], "search_type": "Repositories"})
    assert response.status_code == 422


def test_invalid_keyword_type():
    response = client.post(
        "/get_github_links", json={"keywords": "", "proxies": ["1.2.3.4:1111"], "search_type": "Repositories"}
    )
    assert response.status_code == 422


def test_invalid_proxy_format():
    response = client.post(
        "/get_github_links", json={"keywords": ["openstack"], "proxies": ["invalid"], "search_type": "Repositories"}
    )
    assert response.status_code == 422


def test_invalid_search_type():
    invalid_search_type = "InvalidType"
    response = client.post(
        "/get_github_links",
        json={"keywords": ["openstack"], "proxies": ["1.1.1.1:2222"], "search_type": invalid_search_type},
    )
    assert response.status_code == 422
    assert f"Invalid search type. Allowed types are Repositories, Issues, Wikis" in response.text


def test_empty_proxies():
    response = client.post("/get_github_links", json={"keywords": ["openstack"], "proxies": [], "search_type": "Repositories"})
    assert response.status_code == 422
