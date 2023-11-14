from requests_mock import Mocker
from vercel_storage import blob


def test_blob_list(requests_mock: Mocker):
    requests_mock.get(
        url="https://blob.vercel-storage.com/",
        status_code=200,
        json={
            "hasMore": False,
            "blobs": [
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
            ],
        },
    )

    contents = blob.list(
        options={"token": "ABCD123foobar"},
    )

    assert requests_mock.called
    assert requests_mock.call_count == 1
    assert [z["pathname"] for z in contents['blobs']] == ["README.md", "tox.ini"]
