from requests_mock import Mocker
from vercel_storage import blob

_mock_blobs = [
    {
        "url": "https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/README-PWeZ5e2SC66TZgvFcvzVOMz2ZcUqnR.md",
        "pathname": "README.md",
        "size": 263,
        "uploadedAt": "2023-11-14T23:26:52.759Z",
        "contentType": "text/markdown",
        "contentDisposition": 'attachment; filename="README.md"',
    },
    {
        "url": "https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/tox-XrRb5Y3rC0H30fIXhL6yDYtTOPG8TL.ini",
        "pathname": "tox.ini",
        "size": 195,
        "uploadedAt": "2023-11-14T23:26:43.364Z",
        "contentType": "text/plain",
        "contentDisposition": 'attachment; filename="tox.ini"',
    },
]


def test_blob_list(requests_mock: Mocker):
    requests_mock.get(
        url="https://blob.vercel-storage.com/",
        status_code=200,
        json={"hasMore": False, "blobs": _mock_blobs},
    )

    contents = blob.list(
        options={"token": "ABCD123foobar"},
    )

    assert requests_mock.called
    assert requests_mock.call_count == 1
    assert [z["pathname"] for z in contents["blobs"]] == ["README.md", "tox.ini"]


def test_blob_list_params(requests_mock: Mocker):
    requests_mock.get(url="https://blob.vercel-storage.com/", status_code=200, json={})

    blob.list(
        options={
            "token": "ABCD123foobar",
        },
    )
    blob.list(
        options={
            "token": "ABCD123foobar",
            "limit": "1337",
            "prefix": "/foo/bar",
            "cursor": "ABC1223RXYZ",
            "mode": "folded",
            "unsupported-parameter": "bar-baz",
        },
    )

    assert requests_mock.called
    assert requests_mock.call_count == 2
    # First request with default parameters
    api_rq = requests_mock.request_history[0]
    assert api_rq.headers["limit"] == "100"
    assert "prefix" not in api_rq.headers
    assert "cursor" not in api_rq.headers
    assert "mode" not in api_rq.headers
    assert "unsupported-parameter" not in api_rq.headers

    # Second request with user-defined parameters
    api_rq = requests_mock.request_history[1]
    assert api_rq.headers["limit"] == "1337"
    assert api_rq.headers["prefix"] == "/foo/bar"
    assert api_rq.headers["cursor"] == "ABC1223RXYZ"
    assert api_rq.headers["mode"] == "folded"
    assert "unsupported-parameter" not in api_rq.headers
