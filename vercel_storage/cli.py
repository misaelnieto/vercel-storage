import sys
import click

from .api import TOKEN_ENV, put


@click.command()
@click.option('--token', help=f"The Vercel's blob read/write token. If not provided it will take it from the {TOKEN_ENV} environment variable")
@click.argument('command', type=click.Choice(['put'], case_sensitive=False))
@click.argument('path', type=click.File(mode='rb'))
def main(command:str, path:click.File, token:str = None):
    _opts = None
    if token:
        _opts = {"token":token}
    resp = put(path.name, path.read(), options=_opts)
    print(f"File URL: {resp['url']}")


if __name__ == '__main__':
    main()
