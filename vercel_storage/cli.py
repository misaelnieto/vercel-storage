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
    "--json", "-j", "print_json",
    help="Print the json response instead of a summary table",
    is_flag=True
)
@click.pass_context
def cli(ctx: click.Context, print_json:bool, token: str = None):
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


@cli.command
@click.argument("path", type=click.File(mode="rb"))
@click.pass_context
def put(ctx: click.Context, path: click.File):
    resp = blob.put(path.name, path.read(), options={"token": ctx.obj["token"]})
    click.echo(f"New file URL: {resp['url']}")


@cli.command
@click.pass_context
@click.argument("urls", nargs=-1, required=True)
def delete(ctx: click.Context, urls):
    blob.delete(urls, options={"token": ctx.obj["token"]})


@cli.command
@click.pass_context
def list(ctx: click.Context):
    resp = blob.list(options={"token": ctx.obj["token"]})
    if "blobs" in resp:
        if ctx.obj["print_json"]:
            click.echo(resp)
        else:
            table = [
                [item["pathname"], item["size"], item["url"]] for item in resp["blobs"]
            ]
            click.echo(tabulate(table, headers=["Path name", "Size in bytes", "url"]))

    # click.echo(resp)


@cli.command
@click.pass_context
@click.argument("url", required=True, type=click.STRING)
def head(ctx: click.Context, url:str):
    resp = blob.head(url, options={"token": ctx.obj["token"]})
    if ctx.obj["print_json"]:
        click.echo(resp)
    else:
        click.echo(tabulate([(k,v) for k,v in resp.items()]))


@cli.command
@click.pass_context
@click.argument("from_url", required=True, type=click.STRING)
@click.argument("to_pathname", required=True, type=click.STRING)
def copy(ctx: click.Context, from_url:str, to_pathname:str):
    resp = blob.copy(from_url, to_pathname, options={"token": ctx.obj["token"]})
    if ctx.obj["print_json"]:
        click.echo(resp)
    else:
        click.echo(tabulate([(k,v) for k,v in resp.items()]))

if __name__ == "__main__":
    cli()
