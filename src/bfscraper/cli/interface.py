import json
import os

import click

from ..scrapers.site_scraper import SiteScraper

# Default config loading:
with open(os.path.join(os.path.dirname(__file__), "defaults.json")) as fp:
    default = json.load(fp)


@click.command("bfscraper")
@click.option(
    "--count",
    "-c",
    default=default["count"],
    show_default=True,
    type=click.IntRange(min=-1, clamp=True),
    help="Number of airfoils to scrape (-1 for all available)."
)
@click.option(
    "--output",
    "-o",
    default=default["output"],
    show_default=True,
    type=click.Path(exists=False, dir_okay=False, writable=True),
    help="Output file path."
)
@click.option(
    "--timeout",
    "-t",
    default=default["timeout"],
    show_default=True,
    type=click.IntRange(min=-1, clamp=True),
    help="Request timeout in seconds (-1 for no timeout)."
)
@click.option(
    "--limit",
    "-l",
    default=default["limit"],
    show_default=True,
    type=click.IntRange(min=1, clamp=True),
    help="Simultaneous requests limit."
)
@click.option(
    "--verbose",
    "-v",
    default=default["verbose"],
    show_default=True,
    is_flag=True, help="Verbose mode."
)
def cli(*args, **kwargs):
    """Command line interface."""
    SiteScraper(**kwargs).run()
