# GCN Classic to Kafka bridge

Pump GCN Classic notices to a Kafka broker.

GCN Classic sends binary and VOEvent format notices to us over TCP/IP.
We act as the server and GCN Classic acts as the client. The packet format
consists of the following fields:

1.  The 160-byte binary notice. The first 4 bytes are the notice type as a
    network byte order integer.
2.  A 4-byte network byte order integer that is the length of the VOEvent.
3.  The VOEvent.

GCN Classic does not expect us to send any data back. GCN sends a packet at
least every 60 seconds, including keepalive packets. Keepalive packets have
the same format as notice packets, except that the notice type is
`gcn.NoticeType.IM_ALIVE`, `gcn.NoticeType.VOE_11_IM_ALIVE`, or
`gcn.NoticeType.VOE_20_IM_ALIVE`.

## To install

    $ pip install .

## To hack

This project uses [Poetry]. To hack on it, first [install Poetry]. Then, run
the following commands to set up and enter the development virtual environment:

    $ poetry install
    $ poetry shell

[Poetry]: https://python-poetry.org/
[install Poetry]: https://python-poetry.org/docs/#installation
