"""Command line interface."""

import logging

import click


@click.group()
def main():
    """Pump GCN Classic notices to a Kafka broker."""
    logging.basicConfig(level=logging.INFO)


@main.command()
def voevent():
    """Process VOEvent-formatted GCN Notices."""
    from .voevent import serve_forever
    serve_forever()
