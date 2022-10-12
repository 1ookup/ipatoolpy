import click

from cli.logger import logger
from networking.http_client import HTTPClient
from store_api.itunes.itunes_client import iTunesClient


@click.command('search')
@click.option('-l', '--limit',
              default=5,
              help='The maximum amount of search results to retrieve. (default: 5)')
@click.option('-c', '--country',
              default='US',
              help='The two-letter (ISO 3166-1 alpha-2) country code for the iTunes Store. (default: US)')
@click.option('-d', '--device-family',
              default='iPhone',
              help='The device family to limit the search query to. (default: iPhone)')
@click.argument('term')
@click.pass_context
def search(ctx: click.core.Context,
           limit, country, device_family,
           term):
    """Search for iOS apps available on the App Store."""
    http_client = HTTPClient()
    itunes_client = iTunesClient(http_client=http_client)
    logger.info(f"Searching for '{term}' using the '{country}' store front...")
    results = itunes_client.search(term, limit=limit, country_code=country, device_family=device_family)
    index = 0
    for item in results:
        name = item['name']
        bundle_identifier = item['bundle_identifier']
        identifier = item['identifier']
        version = item['version']
        index += 1
        logger.info(f'{str(index).ljust(2)} {name} | {bundle_identifier} | {identifier} | {version}')
