from dataclasses import dataclass
from os import getenv
from typing import Optional

import requests

from . import ConfigurationError


VERCEL_API_URL = "https://blob.vercel-storage.com"
TOKEN_ENV = "BLOB_READ_WRITE_TOKEN"
API_VERSION = '4'
DEFAULT_CACHE_AGE = 365 * 24 * 60 * 60  # 1 Year
DEFAULT_ACCESS = 'public'


def get_token(options: dict):
    _tkn = options.get('token', getenv(TOKEN_ENV, None))
    if not _tkn:
        raise ConfigurationError("Vercel's BLOB_READ_WRITE_TOKEN is not set")
    return _tkn


def _coerce_bool(value):
    return str(int(bool(value)))


def put(pathname:str, body:bytes, options:Optional[dict]=None) -> dict:
    _opts = dict(options) if options else dict()
    headers = {
        'access': 'public',
        'authorization': f'Bearer {get_token(_opts)}',
        'x-api-version': API_VERSION,
        'x-content-type': _opts.get("contentType", 'text/plain'),
        'x-add-random-suffix': _coerce_bool(_opts.get("addRandomSuffix", True)),
        'x-cache-control-max-age': _opts.get('cacheControlMaxAge', str(DEFAULT_CACHE_AGE))
    }
    _resp = requests.put(f'{VERCEL_API_URL}/{pathname}', data=body, headers=headers)
    return _resp.json()
