# vercel-storage

A wrapper around the vercel blob api


[![Lint and test](https://github.com/misaelnieto/vercel-storage/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/misaelnieto/vercel-storage/actions/workflows/python-app.yml)

## Current status

Currently it only implements the [Vercel Blob API](https://vercel.com/docs/storage/vercel-blob). You can use this package as a library as well as a command line utility.

## Installation

This package is still unreleased. You can only install it locally.

```sh
git clone https://github.com/misaelnieto/vercel-storage.git
cd vercel-storage
pip install -e .
```

### Installation in development mode

Probably only useful for the author and contributors.

```sh
pip install -e '.[test]
```

Run tests:

```sh
pytest
```

## Command line usage

### Configuration

You must set the `BLOB_READ_WRITE_TOKEN` environment variable to be able to use the library.

```sh
export BLOB_READ_WRITE_TOKEN="vercel_blob_rw_ABC1234XYz"
```

### Put operation

```sh
$ vercel_blob put disk_dump.bin
------------------  ----------------------------------------------------------------------------------------------------
url                 https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/disk_dump-OTgBsduT0QQcfXImNMZky1NSy3HfML.bin
pathname            disk_dump.bin
contentType         application/octet-stream
contentDisposition  attachment; filename="disk_dump.bin"
------------------  ----------------------------------------------------------------------------------------------------
```

You can also print the output information as a json:

```sh
$ vercel_blob --json put disk_dump.bin
{'url': 'https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/disk_dump-0eX9NYJnZjO31GsDiwDaQ6TR9QnWkH.bin', 'pathname': 'disk_dump.bin', 'contentType': 'text/plain', 'contentDisposition': 'attachment; filename="disk_dump.bin"'}
```

By default, Vercel's blob store will insert a randomly generated string to the name of your file. But you can turn off that feature:

```sh
$ vercel_blob put --no-suffix chart.png 
------------------  -----------------------------------------------------------------
url                 https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/chart.png
pathname            chart.png
contentType         image/png
contentDisposition  attachment; filename="chart.png"
------------------  -----------------------------------------------------------------
```

### List operation

The list method returns a list of blob objects in a Blob store. For example, let's upload a file to the bob store:

```sh
vercel_blob put profile.png 
------------------  --------------------------------------------------------------------------------------------------
url                 https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/profile-OtpJ1AUIxChAA6UZejVXPA1pkuBw2D.png
pathname            profile.png
contentType         image/png
contentDisposition  attachment; filename="profile.png"
------------------  --------------------------------------------------------------------------------------------------
```

Now you can see your file on your blob store:

```sh
vercel_blob list
Path name      Size in bytes  url
-----------  ---------------  -------------------------------------------------------------------
profile.png            11211  https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/profile-OtpJ1AUIxChAA6UZejVXPA1pkuBw2D.png
```


### Copy operation

```sh
$ vercel_blob copy https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/disk_dump-0eX9NYJnZjO31GsDiwDaQ6TR9QnWkH.bin file.zip

------------------  ----------------------------------------------------------------
url                 https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/file.zip
pathname            file.zip
contentType         application/octet-stream
contentDisposition  attachment; filename="file.zip"
------------------  ----------------------------------------------------------------

```

You can also print the output information as a json:

```sh
$ vercel_blob --json copy https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/disk_dump-0eX9NYJnZjO31GsDiwDaQ6TR9QnWkH.bin file.zip
{'url': 'https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/file.zip', 'pathname': 'file.zip', 'contentType': 'application/octet-stream', 'contentDisposition': 'attachment; filename="file.zip"'}
```

### Delete operation

The delete operation always suceeds, regardless of whether the blob exists or not. It returns a null payload.

```sh
$ vercel_blob delete https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/disk_dump-mSjTcLOIg8hlGNiWpWMUcGqVll1uST.bin
```

### Head operation

The head operation returns a blob object's metadata.


```sh
$ vercel_blob head https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/file.zip
------------------  ----------------------------------------------------------------
url                 https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/file.zip
pathname            file.zip
contentType         application/octet-stream
contentDisposition  attachment; filename="file.zip"
uploadedAt          2023-11-16T23:53:25.000Z
size                1998
cacheControl        public, max-age=31536000, s-maxage=300
------------------  ----------------------------------------------------------------
```

As with the other commands, you can generate json output:

```sh
$ vercel_blob --json head https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/file.zip
{'url': 'https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/file.zip', 'pathname': 'file.zip', 'contentType': 'application/octet-stream', 'contentDisposition': 'attachment; filename="file.zip"', 'uploadedAt': '2023-11-16T23:53:25.000Z', 'size': 1998, 'cacheControl': 'public, max-age=31536000, s-maxage=300'}
```


## Using vercel_storage in your python code

### List operation

Note: `vercel_storage` will look for the `BLOB_READ_WRITE_TOKEN` environment variable. If it is not available
it will raise an Exception.

If you have the token stored somewhere else, you can pass it directly to the put() function like this:


```python
    resp = blob.list(options={'token': 'ABCD123foobar'})
```

### Put operation

```python
from vercel_storage import blob

my_file = '/path/to/file.zip'
with open(my_file, 'rb') as fp:
    resp = blob.put(
        pathname=my_file,
        body=fp.read()
    )
```

Note: `vercel_storage` will look for the `BLOB_READ_WRITE_TOKEN` environment variable. If it is not available
it will raise an Exception.

If you have the token stored somewhere else, you can pass it directly to the put() function like this:

```python
  resp = blob.put(
      pathname=my_file,
      body=fp.read(),
      options={'token': 'ABCD123foobar'}
  )
```

### Copy operation

```python
retval = blob.copy(blob_url, to_path)
# or
retval = blob.copy(blob_url, to_path, options={"token": "ABCD123foobar"})
```

### Delete operation

```python
blob.delete(blob_url)
# or
blob.delete(blob_url, options={'token': 'ABCD123foobar'})
```

### Head operation

```python
blob.head(blob_url)
# or
blob.head(blob_url, options={'token': 'ABCD123foobar'})
```

