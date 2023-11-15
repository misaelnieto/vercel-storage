from requests_mock import Mocker
from vercel_storage import blob


def test_blob_head(requests_mock: Mocker):
    assert not requests_mock.called
    assert requests_mock.call_count == 0
    blob_url = "https://xyz123.public.blob.vercel-storage.com/file-XrRb5Y3rC0H30fIXhL6yDYtTOPG8TL.txt"
    to_path = "foo/bar/newfilename.md"
    response_payload = {
        "url": blob_url,
        "pathname": to_path,
        "contentType": "text/markdown",
        "contentDisposition": 'attachment; filename="newfilename.md"',
    }
    requests_mock.put(
        url=f"https://blob.vercel-storage.com/{to_path}", status_code=200, json=response_payload
    )

    retval = blob.copy(blob_url, to_path, options={"token": "ABCD123foobar"})

    assert requests_mock.called
    assert requests_mock.call_count == 1
    assert retval == response_payload
