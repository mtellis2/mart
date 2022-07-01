import click

from .map_artwork import map_art


@click.group()
def cli():
    """Group of artwork commands"""


cli.add_command(map_art)
