"""Command line interface."""
import json
import logging

import click
import confluent_kafka

log = logging.getLogger(__name__)


@click.group()
@click.option(
    '--config', metavar='FILE.json',
    help='JSON configuration file for Kafka client. '
    'See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md.')
@click.pass_context
def main(ctx, config):
    """Pump GCN Classic notices to a Kafka broker."""
    logging.basicConfig(level=logging.INFO)

    if config:
        with open(config, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    producer = confluent_kafka.Producer(config)

    ctx.ensure_object(dict)
    ctx.obj['producer'] = producer


@main.command()
@click.pass_context
@click.option(
    '--host', type=str, default='127.0.0.1', show_default=True,
    help='Hostname to listen on for GCN Classic')
@click.option(
    '--port', type=int, default=8081, show_default=True,
    help='Port to listen on for GCN Classic')
def binary(ctx, host, port):
    """Ingest binary and VOEvent notices."""
    import asyncio
    from .socket import client_connected

    client = client_connected(ctx.obj['producer'])

    async def serve():
        server = await asyncio.start_server(client, host, port)
        log.info('Listening on %s:%d', host, port)
        async with server:
            await server.serve_forever()

    asyncio.run(serve())
