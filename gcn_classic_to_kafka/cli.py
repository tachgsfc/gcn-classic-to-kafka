#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
"""Command line interface."""
import asyncio
import logging
import os
import re
import urllib
import signal
import sys

import click
import confluent_kafka
import prometheus_client

from .socket import client_connected
from . import metrics

log = logging.getLogger(__name__)

env_key_splitter = re.compile(r'_+')
replacement_dict = {'_': '.', '__': '-', '___': '_'}


def replacement(match: re.Match) -> str:
    text = match[0]
    return replacement_dict.get(text) or text


def kafka_config_from_env(env: dict[str, str], prefix: str) -> dict[str, str]:
    """Construct a Kafka client configuration dictionary from env variables.

    This uses the same rules as
    https://docs.confluent.io/platform/current/installation/docker/config-reference.html
    to convert from configuration variables to environment variable names:

    * Start the environment variable name with the given prefix.
    * Convert to upper-case.
    * Replace periods (`.`) with single underscores (`_`).
    * Replace dashes (`-`) with double underscores (`__`).
    * Replace underscores (`-`) with triple underscores (`___`).

    """
    config = {}
    for key, value in env.items():
        if key.startswith(prefix):
            key = env_key_splitter.sub(replacement, key.removeprefix(prefix))
            config[key.lower()] = value
    return config


def signal_handler(signum, frame):
    log.info('Exiting due to signal %d', signum)
    sys.exit(128 + signum)


def kafka_delivered_cb(err, msg):
    successful = not err
    metrics.delivered_count.labels(
        msg.topic(), msg.partition(), successful).inc()
    metrics.delivered_timestamp_seconds.labels(
        msg.topic(), msg.partition(), successful).set_to_current_time()


def host_port(host_port_str):
    # Parse netloc like it is done for HTTP URLs.
    # This ensures that we will get the correct behavior for hostname:port
    # splitting even for IPv6 addresses.
    return urllib.parse.urlparse(f'http://{host_port_str}')


@click.command()
@click.option(
    '--listen', type=host_port, default=':8081', show_default=True,
    help='Hostname and port to listen on for GCN Classic')
@click.option(
    '--prometheus', type=host_port, default=':8000', show_default=True,
    help='Hostname and port to listen on for Prometheus metric reporting')
@click.option(
    '--loglevel', type=click.Choice(logging._levelToName.values()),
    default='DEBUG', show_default=True, help='Log level')
def main(listen, prometheus, loglevel):
    """Pump GCN Classic notices to a Kafka broker.

    Specify the Kafka client configuration in environment variables using the
    conventions described in
    https://docs.confluent.io/platform/current/installation/docker/config-reference.html#confluent-enterprise-ak-configuration:

    * Start the environment variable name with `KAFKA_`.
    * Convert to upper-case.
    * Replace periods (`.`) with single underscores (`_`).
    * Replace dashes (`-`) with double underscores (`__`).
    * Replace underscores (`-`) with triple underscores (`___`).
    """
    logging.basicConfig(level=loglevel)

    prometheus_client.start_http_server(prometheus.port,
                                        prometheus.hostname or '0.0.0.0')
    log.info('Prometheus listening on %s', prometheus.netloc)

    config = kafka_config_from_env(os.environ, 'KAFKA_')
    config['client.id'] = __package__
    config['on_delivery'] = kafka_delivered_cb

    producer = confluent_kafka.Producer(config)
    client = client_connected(producer)

    async def serve():
        server = await asyncio.start_server(
            client, listen.hostname, listen.port)
        log.info('GCN server listening on %s', listen.netloc)
        async with server:
            await server.serve_forever()

    # Exit cleanly on SIGTERM
    signal.signal(signal.SIGTERM, signal_handler)

    asyncio.run(serve())
