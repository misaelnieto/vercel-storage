import sys
import click
from tabulate import tabulate

from vercel_storage import blob


@click.group
@click.option('--token', help=f"The Vercel's blob read/write token. If not provided it will take it from the {blob.TOKEN_ENV} environment variable")
@click.pass_context
def cli(ctx:click.Context, token:str = None):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    _opts = {}
    if token:
        _opts['token'] = token
    try:
        ctx.obj['token'] = blob.get_token(_opts)
    except blob.ConfigurationError as err:
        click.echo(click.style(f'Error: {err}', fg='red'), err=True)
        sys.exit(1)


@cli.command
@click.argument('path', type=click.File(mode='rb'))
@click.pass_context
def put(ctx:click.Context, path:click.File):
    resp = blob.put(path.name, path.read(), options={"token":ctx.obj['token']})
    click.echo(f"New file URL: {resp['url']}")


@cli.command
@click.pass_context
@click.argument('urls', nargs=-1, required=True)
def delete(ctx:click.Context, urls):
    blob.delete(urls, options={"token":ctx.obj['token']})


@cli.command
@click.pass_context
@click.option('--print-json', help='Print the json response instead of a summary table', type=click.BOOL, default=False)
def list(ctx:click.Context, print_json: bool):
    resp = blob.list(options={"token":ctx.obj['token']})
    if 'blobs' in resp:
        if print_json:
            click.echo(resp)
        else:
            z = {'url': 'https://c6zu0uktwgrh0d3g.public.blob.vercel-storage.com/README-5dtvhxXabA3av51qgZFDQx1Zd8gLfJ.md', 'pathname': 'README.md', 'size': 147, 'uploadedAt': '2023-11-14T03:56:41.839Z', 'contentType': 'text/markdown', 'contentDisposition': 'attachment; filename="README.md"'}
            table = [[item['pathname'], item['size'], item['url']] for item in resp['blobs']]
            click.echo(tabulate(table, headers=['Path name', 'Size in bytes', 'url']))
            
    # click.echo(resp)

if __name__ == '__main__':
    cli()
