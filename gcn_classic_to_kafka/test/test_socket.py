#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
import asyncio
from unittest import mock
import struct

import gcn
import pytest
import pytest_asyncio

from ..socket import client_connected

timeout = 0.125


def make_packet(bin_notice_type, voe_notice_type=None):
    if voe_notice_type is None:
        voe_notice_type = bin_notice_type
    voevent = f"""<?xml version="1.0" encoding="UTF-8"?>
    <voe:VOEvent
    version="2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:voe="http://www.ivoa.net/xml/VOEvent/v2.0"
    xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v2.0
    http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd"
    >
    <What>
        <Param name="Packet_Type" value="{voe_notice_type:d}" />
    </What>
    </voe:VOEvent>
    """.encode()
    text = b'Hello world'
    return (
        struct.pack('!l156xl', bin_notice_type, len(voevent)) + voevent +
        struct.pack('!l', len(text)) + text)


@pytest_asyncio.fixture
async def start_server():
    producer = mock.Mock()
    cb = client_connected(producer=producer, timeout=timeout)
    server = await asyncio.start_server(cb, '127.0.0.1')

    async with server:
        server_task = asyncio.create_task(server.serve_forever())
        socket, = server.sockets
        host, port = socket.getsockname()
        yield producer, host, port
        server_task.cancel()


@pytest.mark.asyncio
async def test_socket(start_server):
    producer, host, port = start_server
    iamalive_packet = make_packet(gcn.NoticeType.VOE_20_IM_ALIVE)
    lvc_test_packet = make_packet(gcn.NoticeType.LVC_TEST)

    # Test hanging up ont he server immediately.
    # The server should drop the connection too.
    reader, writer = await asyncio.open_connection(host, port)
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    assert reader.at_eof()
    producer.produce.assert_not_called()

    # Test writing an incomplete packet.
    # The server should time out and drop the connection.
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(lvc_test_packet[:-1])
    await writer.drain()
    await asyncio.sleep(1.5 * timeout)
    assert reader.at_eof()
    producer.produce.assert_not_called()
    writer.close()
    await writer.wait_closed()

    # Test writing a complete 'iamalive' packet.
    # The server should not time out,
    # but it should not send any Kafka messages.
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(iamalive_packet)
    await writer.drain()
    await asyncio.sleep(0.25 * timeout)
    assert not reader.at_eof()
    producer.produce.assert_not_called()

    # Test writing a complete alert packet.
    # The server should not time out and it should send Kafka messages.
    writer.write(lvc_test_packet)
    await writer.drain()
    await asyncio.sleep(0.25 * timeout)
    assert not reader.at_eof()
    producer.produce.assert_has_calls([
        mock.call('gcn.classic.binary.LVC_TEST', mock.ANY),
        mock.call('gcn.classic.voevent.LVC_TEST', mock.ANY),
        mock.call('gcn.classic.text.LVC_TEST', mock.ANY)])

    writer.close()
    await writer.wait_closed()
    await asyncio.sleep(0.25 * timeout)
