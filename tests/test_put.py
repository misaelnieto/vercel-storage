from requests_mock import Mocker
from vercel_storage import blob


def test_blob_upload(requests_mock: Mocker):
    file_name = 'user-12345.txt'
    file_path = f'profilesv1/{file_name}'
    response_payload = {
        'pathname': file_path,
        'contentType': 'text/plain',
        'contentDisposition': 'attachment; filename="user-12345.txt"',
        'url': 'https://ce0rcu23vrrdzqap.public.blob.vercel-storage.com/profilesv1/user-12345-NoOVGDVcqSPc7VYCUAGnTzLTG2qEM2.txt'
    }
    requests_mock.put(
        url='https://blob.vercel-storage.com/profilesv1/user-12345.txt',
        status_code="200",
        json=response_payload
    )

    resp = blob.put(
        pathname=file_path,
        body=b'loremipsum',
        options={'token': 'ABCD123foobar'}
    )

    assert resp == response_payload
