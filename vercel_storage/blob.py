from dataclasses import dataclass
from os import getenv
from typing import Any, Optional, Union

import requests

from . import ConfigurationError, APIResponseError


VERCEL_API_URL = "https://blob.vercel-storage.com"
TOKEN_ENV = "BLOB_READ_WRITE_TOKEN"
API_VERSION = "4"
DEFAULT_CACHE_AGE = 365 * 24 * 60 * 60  # 1 Year
DEFAULT_ACCESS = "public"


def get_token(options: dict):
    if not options or not isinstance(options, dict):
        _tkn = getenv(TOKEN_ENV, None)
    else:
        _tkn = options.get("token", None)
    if not _tkn:
        raise ConfigurationError("Vercel's BLOB_READ_WRITE_TOKEN is not set")
    return _tkn


def _coerce_bool(value):
    return str(int(bool(value)))


def _handle_response(response: requests.Response):
    if str(response.status_code) == '200':
        return response.json()
    raise APIResponseError(f"Oops, something went wrong: {response.json()}")


def put(pathname: str, body: bytes, options: Optional[dict] = None) -> dict:
    _opts = dict(options) if options else dict()
    headers = {
        "access": "public",
        "authorization": f"Bearer {get_token(_opts)}",
        "x-api-version": API_VERSION,
        "x-content-type": _opts.get("contentType", "text/plain"),
        "x-add-random-suffix": _coerce_bool(_opts.get("addRandomSuffix", True)),
        "x-cache-control-max-age": _opts.get(
            "cacheControlMaxAge", str(DEFAULT_CACHE_AGE)
        ),
    }
    _resp = requests.put(f"{VERCEL_API_URL}/{pathname}", data=body, headers=headers)
    return _handle_response(_resp)


def delete(
    url: Union[str, list[str], tuple[str]], options: Optional[dict] = None
) -> dict:
    """
    Deletes a blob object from the Blob store.
    Args:
        url (str|list[str]|tuple[str]): A string or a list of strings specifying the
            unique URL(s) of the blob object(s) to delete.
        options (dict): A dict with the following optional parameter:
            token (Not required) A string specifying the read-write token to
                  use when making requests. It defaults to the BLOB_READ_WRITE_TOKEN
                  environment variable when deployed on Vercel as explained
                  in Read-write token

    Returns:
        None: A delete action is always successful if the blob url exists. A delete action won't throw if the blob url doesn't exists.
    """
    _opts = dict(options) if options else dict()
    headers = {
        "authorization": f"Bearer {get_token(_opts)}",
        "x-api-version": API_VERSION,
        "content-type": "application/json",
    }
    _resp = requests.post(
        f"{VERCEL_API_URL}/delete",
        json={
            "urls": [
                url,
            ]
            if isinstance(url, str)
            else url
        },
        headers=headers,
    )
    return _handle_response(_resp)


def list(options: Optional[dict] = None) -> Any:
    """
    The list method returns a list of blob objects in a Blob store.
    Args:
        options (dict): A dict with the following optional parameter:
            token (Not required) A string specifying the read-write token to
                  use when making requests. It defaults to the BLOB_READ_WRITE_TOKEN
                  environment variable when deployed on Vercel as explained
                  in Read-write token
            limit
            prefix
            cursor
            mode

    Returns:
        ???
    """
    _opts = dict(options) if options else dict()
    headers = {
        "authorization": f"Bearer {get_token(_opts)}",
    }
    _resp = requests.get(
        f"{VERCEL_API_URL}",
        headers=headers,
    )
    return _handle_response(_resp)
