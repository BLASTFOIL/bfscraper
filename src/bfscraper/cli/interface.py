import click

from ..scrapers.site_scraper import SiteScraper
from .defaults import DEFAULTS


@click.command("bfscraper")
@click.option(
    "--count",
    "-c",
    default=DEFAULTS["count"],
    show_default=True,
    type=click.IntRange(min=-1, clamp=True),
    help="Number of airfoils to scrape (-1 for all available)."
)
@click.option(
    "--output",
    "-o",
    default=DEFAULTS["output"],
    show_default=True,
    type=click.Path(exists=False, dir_okay=False, writable=True),
    help="Output file path."
)
@click.option(
    "--timeout",
    "-t",
    default=DEFAULTS["timeout"],
    show_default=True,
    type=click.IntRange(min=-1, clamp=True),
    help="Request timeout in seconds (-1 for no timeout)."
)
@click.option(
    "--limit",
    "-l",
    default=DEFAULTS["limit"],
    show_default=True,
    type=click.IntRange(min=1, clamp=True),
    help="Simultaneous requests limit."
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose mode."
)
def cli(*args, **kwargs):
    """Command line interface."""
    SiteScraper(**kwargs).run()
