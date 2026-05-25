from app import get_google_results


def test_output_structure(monkeypatch):

    fake_data = {
        "organic_results": [
            {
                "position": 1,
                "title": "Example title",
                "link": "https://example.com",
                "snippet": "Example snippet"
            }
        ]
    }

    class FakeResponse:
        def json(self):
            return fake_data


    def fake_get(url, params):
        return FakeResponse()


    monkeypatch.setattr("requests.get", fake_get)

    results = get_google_results("test keyword")

    assert isinstance(results, list)
    assert len(results) == 1

    result = results[0]

    assert result["position"] == 1
    assert result["title"] == "Example title"
    assert result["url"] == "https://example.com"
    assert result["snippet"] == "Example snippet"