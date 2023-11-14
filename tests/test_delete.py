from requests_mock import Mocker
from vercel_storage import blob

def test_blob_delete(requests_mock: Mocker):
    requests_mock.delete(
        url='https://blob.vercel-storage.com/delete',
        status_code='200'
    )

    blob.delete(
        url='https://ce0rcu23vrrdzqap.public.blob.vercel-storage.com/profilesv1/user-12345-NoOVGDVcqSPc7VYCUAGnTzLTG2qEM2.txt',
        options={'token': 'ABCD123foobar'}
    )

    assert requests_mock.called
    assert requests_mock.call_count == 1