import click
import logging

from .map_artwork import map_art

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


@click.group()
def cli():
    """Group of artwork commands"""


cli.add_command(map_art)
