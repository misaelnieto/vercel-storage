from requests_mock import Mocker
from vercel_storage import blob


def test_blob_head(requests_mock: Mocker):
    blob_url = "https://xyz123.public.blob.vercel-storage.com/file-XrRb5Y3rC0H30fIXhL6yDYtTOPG8TL.txt"
    response_payload = {
        "url": blob_url,
        "pathname": "file.txt",
        "contentType": "text/plain",
        "contentDisposition": 'attachment; filename="file.txt"',
        "uploadedAt": "2023-11-14T23:26:43.000Z",
        "size": 195,
        "cacheControl": "public, max-age=31536000, s-maxage=300",
    }
    requests_mock.get(
        url="https://blob.vercel-storage.com/", status_code=200, json=response_payload
    )

    retval = blob.head(url=blob_url, options={"token": "ABCD123foobar"})

    assert requests_mock.called
    assert requests_mock.call_count == 1
    assert retval == response_payload
