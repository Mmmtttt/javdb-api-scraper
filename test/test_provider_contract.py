from __future__ import annotations

from ultimate_provider import JavdbProvider


class FakeAdapter:
    def search_videos(self, keyword, page=1, max_pages=1):
        return {"keyword": keyword, "page": page, "max_pages": max_pages}

    def get_video_detail(self, video_id):
        return {"video_id": video_id}


def test_normalize_config_parses_cookie_and_preserves_domain():
    provider = JavdbProvider()

    config = provider.normalize_config(
        {"enabled": True, "cookie_string": "_jdb_session=abc; over18=1", "domain_index": "2"}
    )

    assert config["cookies"]["_jdb_session"] == "abc"
    assert config["cookies"]["over18"] == "1"
    assert config["domain_index"] == 2
    assert config["enabled"] is True


def test_execute_maps_catalog_capabilities_to_adapter(monkeypatch):
    provider = JavdbProvider()
    monkeypatch.setattr(provider, "_get_adapter", lambda config, existing_tags=None: FakeAdapter())

    assert provider.execute("catalog.search", {"keyword": "ABC", "page": 2, "max_pages": 3}, {}, {}) == {
        "keyword": "ABC", "page": 2, "max_pages": 3
    }
    assert provider.execute("catalog.detail", {"video_id": "ABC-001"}, {}, {}) == {"video_id": "ABC-001"}
