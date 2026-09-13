from __future__ import annotations

import ultimate_provider as provider_module
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


def test_execute_maps_code_people_and_collection_capabilities(monkeypatch):
    provider = JavdbProvider()

    class Adapter(FakeAdapter):
        def get_video_by_code(self, code):
            return {"code": code}

        def search_actor(self, actor_name):
            return [{"name": actor_name}]

        def get_actor_works(self, actor_id, page=1, max_pages=1):
            return {"actor_id": actor_id, "page": page, "max_pages": max_pages}

    monkeypatch.setattr(provider, "_get_adapter", lambda config, existing_tags=None: Adapter())

    assert provider.execute("catalog.by_code", {"code": "FIX-001"}, {}, {}) == {"code": "FIX-001"}
    assert provider.execute("person.search", {"actor_name": "Fixture Actor"}, {}, {}) == [{"name": "Fixture Actor"}]
    assert provider.execute("person.works", {"actor_id": "actor-1", "page": 2, "max_pages": 3}, {}, {}) == {
        "actor_id": "actor-1", "page": 2, "max_pages": 3
    }


def test_execute_proxy_and_transport_capabilities_forward_params(monkeypatch):
    provider = JavdbProvider()
    monkeypatch.setattr(provider, "_proxy_url", lambda params, config: {"kind": "proxy", "params": params})
    monkeypatch.setattr(provider, "_transport_request", lambda params, config: {"kind": "transport", "params": params})

    proxy_params = {"url": "https://example.test/media.m3u8"}
    transport_params = {"method": "GET", "url": "https://example.test/detail"}
    assert provider.execute("playback.proxy.url", proxy_params, {}, {}) == {"kind": "proxy", "params": proxy_params}
    assert provider.execute("transport.http.request", transport_params, {}, {}) == {"kind": "transport", "params": transport_params}


def test_execute_rejects_unknown_capability():
    provider = JavdbProvider()

    try:
        provider.execute("unsupported.capability", {}, {}, {})
    except ValueError as exc:
        assert "unsupported capability" in str(exc)
    else:
        raise AssertionError("unknown capability must be rejected")
