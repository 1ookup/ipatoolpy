import click

from cli.logger import logger
from cli.models.account import Account
from networking.http_client import HTTPClient
from store_api.store.store_client import StoreClient


@click.group('auth')
@click.pass_context
def auth(ctx):
    """ Authenticate with the App Store. """
    pass


@auth.command('login')
@click.option('-e', '--email',
              prompt='Enter Apple ID email: ',
              help='The email address for the Apple ID.')
@click.option('-p', '--password',
              prompt='Enter Apple ID password: ',
              help='The password for the Apple ID.')
# @click.option('-c', '--auth-code',
#               help='The 2FA code for the Apple ID.')
@click.pass_context
def auth_login(ctx: click.core.Context, email, password):
    """Login to the App Store."""
    authenticate(email, password)


@auth.command('revoke')
def auth_revoke():
    """Revoke your App Store credentials."""
    pass


@auth.command('info')
def auth_info():
    account = Account()
    logger.info(f"name : {account.name}")
    logger.info(f"email: {account.email}")


def authenticate(email, passwd):
    logger.debug("Creating HTTP client...")
    http_client = HTTPClient()
    logger.debug("Creating App Store client...")
    store_client = StoreClient(http_client)

    logger.info("Authenticating with the App Store...")
    account = store_client.authenticate(email, passwd)
    if account:
        logger.success("App Store Auth Success")
        logger.info(f"Account: {account.name}")
        logger.info(f"DirectoryServicesIdentifier: {account.directory_services_identifier}")
    else:
        logger.warning("Auth Failed.")
