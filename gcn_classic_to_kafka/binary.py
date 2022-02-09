"""Process GCN Notices in the 160-byte binary format."""

import logging
import socketserver
import struct

from confluent_kafka import Producer

from .common import kafka_topic_for_notice_type

log = logging.getLogger(__name__)

packet_type_struct = struct.Struct('!l')


def serve_forever(config):
    log.info('Connecting to Kafka')
    producer = Producer(config)

    class GCNBinaryHandler(socketserver.StreamRequestHandler):

        def handle(self):
            while True:
                payload = self.rfile.read(160)
                self.wfile.write(payload)
                notice_type = packet_type_struct.unpack_from(payload)
                kafka_topic = kafka_topic_for_notice_type(notice_type,
                                                          'binary')
                log.info('Sending notice type %d to %s',
                         notice_type, kafka_topic)
                producer.produce(kafka_topic, payload)

    address = ('127.0.0.1', 5190)
    server = socketserver.TCPServer(address, GCNBinaryHandler)
    server.serve_forever()
