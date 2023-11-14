# vercel-blob
A wrapper around the vercel blob api


Install in development mode:

```sh
pip install -e '.[test]'
```

Run tests:

```sh
pytest
```

## Using the command line:


```sh
BLOB_READ_WRITE_TOKEN="vercel_blob_rw_ABC1234XYz" vercel_blob put README.md
```