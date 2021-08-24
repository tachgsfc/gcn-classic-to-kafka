# GCN Classic to Kafka bridge

Pump GCN Classic notices to a Kafka broker.

## To install

    $ pip install .

## To test

    $ docker run --rm -it --hostname localhost -p 9092:9092 scimma/server --noSecurity
    $ gcn-to-kafka voevent

In another shell, run this command to list available topics:

    $ docker run --rm -it --net=host confluentinc/cp-kafkacat kafkacat -b localhost:9092 -L

Run this command to monitor the records on a given topic (replacing
`gcn.classic.voevent.FERMI_GBM_POS_TEST` with the topic that you are interested
in):

    $ docker run --rm -it --net=host confluentinc/cp-kafkacat kafkacat -b localhost:9092 -C -t docker run --rm -it --net=host confluentinc/cp-kafkacat kafkacat -b localhost:9092 -C -t gcn.classic.voevent.FERMI_GBM_POS_TEST

## To hack

This project uses [Poetry]. To hack on it, first [install Poetry]. Then, run
the following commands to set up and enter the development virtual environment:

    $ poetry install
    $ poetry shell

## To do

1. Implement binary (160 byte) notices.
2. Implement text (email) notices.
3. Add command line arguments to control Kafka broker configuration.
4. Add unit tests.

[Poetry]: https://python-poetry.org/
[install Poetry]: https://python-poetry.org/docs/#installation
