#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
"""Protocol handler for GCN socket connection."""
import asyncio
import logging
import struct

import confluent_kafka
import gcn
import lxml.etree

from .common import topic_for_notice_type

log = logging.getLogger(__name__)

bin_length = 160
int4 = struct.Struct('!l')
ignore_notice_types = {gcn.NoticeType.IM_ALIVE,
                       gcn.NoticeType.VOE_11_IM_ALIVE,
                       gcn.NoticeType.VOE_20_IM_ALIVE}


def client_connected(producer: confluent_kafka.Producer, timeout: float = 90):

    async def client_connected_cb(reader: asyncio.StreamReader,
                                  writer: asyncio.StreamWriter):
        async def read():
            bin_payload = await reader.readexactly(bin_length)
            voe_length, = int4.unpack(await reader.readexactly(int4.size))
            voe_payload = await reader.readexactly(voe_length)
            return bin_payload, voe_payload

        async def process():
            bin_payload, voe_payload = await asyncio.wait_for(read(), timeout)

            bin_notice_type, = int4.unpack_from(bin_payload)
            if bin_notice_type in ignore_notice_types:
                return

            voe = lxml.etree.fromstring(voe_payload)
            voe_notice_type = gcn.handlers.get_notice_type(voe)

            if bin_notice_type != voe_notice_type:
                log.warning(
                    'Binary (%d) and VOEvent (%d) notice types differ',
                    bin_notice_type, voe_notice_type)

            log.info('Received notice of type %d', bin_notice_type)
            bin_topic = topic_for_notice_type(bin_notice_type, 'binary')
            voe_topic = topic_for_notice_type(voe_notice_type, 'voevent')
            producer.produce(bin_topic, bin_payload)
            producer.produce(voe_topic, voe_payload)

        peer, *_ = writer.get_extra_info('peername')
        log.info('Client connected from %s', peer)
        try:
            while True:
                await process()
        finally:
            log.info('Closing connection from %s', peer)
            writer.close()
            await writer.wait_closed()

    return client_connected_cb
