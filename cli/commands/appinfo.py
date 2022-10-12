import click

from cli.logger import logger
from cli.models.account import Account
from networking.http_client import HTTPClient
from store_api.itunes.itunes_client import iTunesClient
from store_api.store.store_client import StoreClient


@click.command('appinfo')
@click.option('-b', '--bundle-identifier',
              prompt='Enter App bundle identifier',
              help='The bundle identifier of the target iOS app.')
@click.option('-c', '--country',
              default='US',
              help='The two-letter (ISO 3166-1 alpha-2) country code for the iTunes Store. (default: US)')
@click.option('-d', '--device-family',
              default='iPhone',
              help='The device family to limit the search query to. (default: iPhone)')
@click.pass_context
def appinfo(ctx: click.core.Context,
            bundle_identifier,
            country,
            device_family
            ):
    """Show app info and history versions"""
    logger.debug("Creating HTTP client...")
    http_client = HTTPClient()

    logger.debug("Creating iTunes client...")
    itunes_client = iTunesClient(http_client)

    logger.info(f"Querying the iTunes Store for '{bundle_identifier}' in country '{country}'...")
    app = itunes_client.lookup(bundle_identifier=bundle_identifier,
                               country_code=country,
                               device_family=device_family)
    logger.debug(app)
    if not app:
        logger.warning(f"{bundle_identifier} not found.")
        return False
    account = Account()
    store_client = StoreClient(http_client)
    result = store_client.item(identifier=app['identifier'],
                               directory_services_identifier=account.directory_services_identifier)
    versions = result['metadata']['softwareVersionExternalIdentifiers']
    logger.info(f"versions: {versions}")
