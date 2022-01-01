"""Command line interface."""

import json
import logging

import click


@click.group()
@click.option('--config', metavar='FILE.json', help='JSON configuration file for Kafka client. See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md.')
@click.pass_context
def main(ctx, config):
    """Pump GCN Classic notices to a Kafka broker."""
    logging.basicConfig(level=logging.INFO)

    if config:
        with open(config, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    ctx.ensure_object(dict)
    ctx.obj['config'] = config


@main.command()
@click.pass_context
def binary(ctx):
    """Process binary (160 byte) formatted GCN Notices."""
    from .binary import serve_forever
    serve_forever(ctx.obj['config'])


@main.command()
@click.pass_context
def voevent(ctx):
    """Process VOEvent-formatted GCN Notices."""
    from .voevent import serve_forever
    serve_forever(ctx.obj['config'])
