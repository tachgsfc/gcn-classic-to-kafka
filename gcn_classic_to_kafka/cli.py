"""Command line interface."""
import asyncio
import logging
import urllib

import click
import confluent_kafka

from .socket import client_connected

log = logging.getLogger(__name__)


@click.command()
@click.option(
    '--bootstrap-servers',
    metavar='hostname1,hostname2,hostname3', required=True,
    help='Comma-separated list of Kafka bootstrap servers')
@click.option(
    '--listen', type=str, default=':8081', show_default=True,
    help='Hostname and port to listen on for GCN Classic')
def main(bootstrap_servers, listen):
    """Pump GCN Classic notices to a Kafka broker."""
    logging.basicConfig(level=logging.INFO)

    # Parse netloc like it is done for HTTP URLs.
    # This ensures that we will get the correct behavior for hostname:port
    # splitting even for IPv6 addresses.
    listen_url = urllib.parse.urlparse(f'http://{listen}')

    config = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': __package__,
    }

    producer = confluent_kafka.Producer(config)
    client = client_connected(producer)

    async def serve():
        server = await asyncio.start_server(
            client, listen_url.hostname, listen_url.port)
        log.info('Listening on %s', listen_url.netloc)
        async with server:
            await server.serve_forever()

    asyncio.run(serve())
