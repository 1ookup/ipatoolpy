import os
import time

import click
import requests

from cli.logger import logger
from cli.models.account import Account
from networking.http_client import HTTPClient
from store_api.itunes.itunes_client import iTunesClient
from store_api.signature.signature_client import SignatureClient
from store_api.store.store_client import StoreClient


def download_app(bundle_identifier, country_code, device_family):
    logger.debug("Creating HTTP client...")
    http_client = HTTPClient()

    logger.debug("Creating iTunes client...")
    itunes_client = iTunesClient(http_client)

    try:
        return itunes_client.lookup(bundle_identifier, country_code=country_code, device_family=device_family)
    except Exception as e:
        logger.exception("download")


def download_item(app, account, external_version_id):
    logger.debug("Creating HTTP client...")
    http_client = HTTPClient()

    logger.debug("Creating iTunes client...")
    store_client = StoreClient(http_client)

    try:
        return store_client.item(identifier=app['identifier'],
                                 directory_services_identifier=account.directory_services_identifier,
                                 external_version_id=external_version_id)
    except Exception as e:
        logger.exception("download_item")


def download_output_path(app, item):
    file_name = f"{app['bundle_identifier']}_{app['identifier']}_" + \
                f"v{item['metadata']['bundleVersion']}_" + \
                f"{item['metadata']['softwareVersionExternalIdentifier']}.ipa"
    current_path = os.getcwd()
    output = os.path.join(current_path, file_name)
    return output


def progressbar(url, filepath):
    start = time.time()
    kwargs = {}
    if HTTPClient.proxy:
        kwargs['verify'] = False
        kwargs['proxies'] = {
            "https": HTTPClient.proxy
        }
    response = requests.get(url, stream=True, **kwargs)
    size = 0
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    try:
        if response.status_code == 200:
            logger.debug('[ipa size]:{size:.2f} MB'.format(
                size=content_size / chunk_size / 1024))
            logger.bind(end="")
            with open(filepath, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    logger.opt(raw=True).info(
                        "\rDownloading app package... [%.2f%%]" % (float(size / content_size * 100))
                    )
            logger.opt(raw=True).info("\n")
        end = time.time()
        logger.debug('used: %.2fs' % (end - start))
    except Exception:
        pass


def download_start(item, path):
    progressbar(item['URL'], path)


def apply_atches(item, email, path):
    logger.debug("Creating signature client...")
    signature_client = SignatureClient(path)
    logger.info("Applying patches...")
    signature_client.append_metadata(item, email)
    signature_client.append_signature(item)


@click.command('download')
@click.option('-b', '--bundle-identifier',
              prompt='Enter App bundle identifier',
              help='The bundle identifier of the target iOS app.')
@click.option('-e', '--external_version_id',
              default="",
              help='The iOS app externalVersionId to downloading older versions.')
@click.option('-c', '--country',
              default='US',
              help='The two-letter (ISO 3166-1 alpha-2) country code for the iTunes Store. (default: US)')
@click.option('-d', '--device-family',
              default='iPhone',
              help='The device family to limit the search query to. (default: iPhone)')
@click.pass_context
def download(ctx: click.core.Context,
             bundle_identifier,
             external_version_id,
             country,
             device_family
             ):
    """Download (encrypted) iOS app packages from the App Store."""
    account = Account()

    app = download_app(bundle_identifier=bundle_identifier, country_code=country, device_family=device_family)
    # logger.debug(app)
    logger.info(f"Found app: {app['name']}\t{app['version']}")
    logger.info(f"Requesting a signed copy of {app['identifier']} from the App Store...")
    item = download_item(app, account, external_version_id)
    # logger.debug(item)
    logger.info(f"Received a response of the signed copy: {item['md5']}.")

    path = download_output_path(app, item)
    logger.info(f"Output path: {path}")

    download_start(item, path)

    apply_atches(item, account.email, path)
    logger.info("Done.")
