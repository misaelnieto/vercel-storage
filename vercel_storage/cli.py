import sys
import urllib.parse

import click
from tabulate import tabulate

from vercel_storage import blob


@click.group
@click.option(
    "--token",
    help=f"The Vercel's blob read/write token. If not provided it will take it from the {blob.TOKEN_ENV} environment variable",
)
@click.option(
    "--json",
    "-j",
    "print_json",
    help="Print the json response instead of a summary table",
    is_flag=True,
)
@click.option(
    "--debug",
    help="Will print the request headers sent to the API endpoint",
    is_flag=True,
)
@click.pass_context
def cli(ctx: click.Context, print_json: bool, debug: bool, token: str = None):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    _opts = {}
    if token:
        _opts["token"] = token
    try:
        ctx.obj["token"] = blob.get_token(_opts)
    except blob.ConfigurationError as err:
        click.echo(click.style(f"Error: {err}", fg="red"), err=True)
        sys.exit(1)
    ctx.obj["print_json"] = print_json
    ctx.obj["debug"] = debug


@cli.command
@click.argument("path", type=click.File(mode="rb"))
@click.option(
    "--no-suffix",
    help="Will not add a random suffix to the pathname of your file",
    is_flag=True,
)
@click.pass_context
def put(ctx: click.Context, path: click.File, no_suffix: bool):
    _opts = {
        "token": ctx.obj["token"],
        "debug": ctx.obj["debug"],
    }
    if no_suffix:
        _opts["no_suffix"] = True
    resp = blob.put(path.name, path.read(), options=_opts)
    if ctx.obj["print_json"]:
        click.echo(resp)
    else:
        click.echo(tabulate([(k, v) for k, v in resp.items()]))


@cli.command
@click.pass_context
@click.argument("urls", nargs=-1, required=True)
def delete(ctx: click.Context, urls):
    blob.delete(urls, options={"token": ctx.obj["token"], "debug": ctx.obj["debug"]})


@cli.command
@click.pass_context
@click.option(
    "--limit",
    help=f"The maximum number of blob objects to return (defaults to 100)",
    type=click.INT,
    default=100,
)
@click.option(
    "--prefix",
    help=f"A string used to filter for blob objects contained in a specific folder assuming that the folder name was used in the pathname when the blob object was uploaded",
    type=click.STRING,
)
@click.option(
    "--cursor",
    help=f"A string obtained from a previous response for pagination of results",
    type=click.STRING,
)
@click.option(
    "--mode",
    help=f"Will change the response format. "
    "In folded mode all blobs that are located inside a folder will be folded "
    "into a single folder string entry (defaults to expanded)",
    type=click.Choice(["expanded", "folded"]),
    default="expanded",
)
def list(ctx: click.Context, limit: int, prefix: str, cursor: str, mode: str):
    _opts = {
        "token": ctx.obj["token"],
        "debug": ctx.obj["debug"],
        "limit": str(limit),
        "mode": mode,
    }

    if prefix:
        _opts["prefix"] = prefix

    if cursor:
        _opts["cursor"] = cursor

    if mode:
        _opts["mode"] = mode

    resp = blob.list(options=_opts)

    if "blobs" in resp:
        if ctx.obj["print_json"]:
            click.echo(resp)
        else:
            table = [
                [item["pathname"], item["size"], item["url"]] for item in resp["blobs"]
            ]
            click.echo(tabulate(table, headers=["Path name", "Size in bytes", "url"]))


@cli.command
@click.pass_context
@click.argument("url", required=True, type=click.STRING)
def head(ctx: click.Context, url: str):
    resp = blob.head(
        url, options={"token": ctx.obj["token"], "debug": ctx.obj["debug"]}
    )
    if ctx.obj["print_json"]:
        click.echo(resp)
    else:
        click.echo(tabulate([(k, v) for k, v in resp.items()]))


@cli.command
@click.pass_context
@click.argument("from_url", required=True, type=click.STRING)
@click.argument("to_pathname", required=True, type=click.STRING)
def copy(ctx: click.Context, from_url: str, to_pathname: str):
    resp = blob.copy(
        from_url,
        to_pathname,
        options={"token": ctx.obj["token"], "debug": ctx.obj["debug"]},
    )
    if ctx.obj["print_json"]:
        click.echo(resp)
    else:
        click.echo(tabulate([(k, v) for k, v in resp.items()]))


if __name__ == "__main__":
    cli()
