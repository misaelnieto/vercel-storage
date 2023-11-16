# vercel-blob
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
vercel_storage blob upload path/to/file.zip
```

You can also print the output information as a json:

```sh
vercel_storage --json blob upload path/to/file.zip
```

### Copy operation

```sh
vercel_storage blob copy <blob url> new/file/path/file.zip
```

You can also print the output information as a json:

```sh
vercel_storage --json copy <blob url> new/file/path/file.zip
```

### Delete operation

The delete operation always suceeds, regardless of whether the blob exists or not. It returns a null payload.

```sh
vercel_storage blob delete <blob url>
```

## Using vercel_storage in your python code

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

`vercel_storage` will look for the `BLOB_READ_WRITE_TOKEN` environment variable. If it is not available
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

