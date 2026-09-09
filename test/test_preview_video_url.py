import sys
from pathlib import Path

from bs4 import BeautifulSoup

plugin_root = str(Path(__file__).resolve().parents[1])
backend_root = str(Path(__file__).resolve().parents[3])
sys.path.insert(0, backend_root)
sys.path.insert(0, plugin_root)

from javdb_api import JavdbAPI
from ultimate_provider import JavdbProvider


class _FakeResponse:
    def json(self):
        return {
            "url": "/movies/ttm3u8/preview/abcde/0/720p.m3u8?sign=test&t=1",
        }


def test_extract_preview_video_resolves_preview_url_endpoint(monkeypatch):
    api = JavdbAPI()
    requested = []

    def fake_get(path):
        requested.append(path)
        return _FakeResponse()

    monkeypatch.setattr(api, "get", fake_get)
    soup = BeautifulSoup('<div data-url="/v/WwVZPR/preview_url"></div>', "html.parser")

    preview_video = api._extract_preview_video(soup)

    assert requested == ["https://javdb.com/v/WwVZPR/preview_url"]
    assert preview_video == "https://javdb.com/movies/ttm3u8/preview/abcde/0/720p.m3u8?sign=test&t=1"


class _FakeSession:
    headers = {}

    def request(self, method, url, **kwargs):
        return type(
            "Response",
            (),
            {
                "status_code": 200,
                "headers": {"content-type": "application/vnd.apple.mpegurl"},
                "content": b"#EXTM3U\nsegment.ts\n",
                "url": url,
                "close": lambda self: None,
            },
        )()


class _FakeApi:
    base_url = "https://javdb.com"
    session = _FakeSession()


def test_javdb_proxy_url_rewrites_m3u8_segments(monkeypatch):
    provider = JavdbProvider(manifest={}, manifest_path="")
    monkeypatch.setattr(provider, "_get_collection_api", lambda config: _FakeApi())

    response = provider._proxy_url(
        {
            "method": "GET",
            "query_string": "url=https%3A%2F%2Fjavdb.com%2Fmovies%2Fpreview.m3u8",
            "proxy_base_path": "/api/v1/video",
        },
        {"timeout": 30},
    )

    assert response.status_code == 200
    assert response.content.startswith(b"#EXTM3U")
    assert b"/api/v1/video/proxy2?url=" in response.content
