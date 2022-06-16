#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
"""Prometheus metrics."""
import prometheus_client

connected = prometheus_client.Gauge(
    'connected', 'Number of active connections from GCN Classic',
    namespace=__package__)

iamalive_timestamp_seconds = prometheus_client.Gauge(
    'iamalive_timestamp_seconds',
    'Timestamp of last GCN notice received, including iamalives',
    namespace=__package__)

received_count = prometheus_client.Counter(
    'received_count',
    'Number of GCN Classic notices received by notice type and flavor',
    labelnames=['notice_type_int', 'notice_type_str', 'flavor'],
    namespace=__package__)

received_timestamp_seconds = prometheus_client.Gauge(
    'notices_received_timestamp_seconds',
    'Timestamp of last GCN Classic notice received by notice type and flavor',
    labelnames=['notice_type_int', 'notice_type_str', 'flavor'],
    unit='seconds', namespace=__package__)

delivered_count = prometheus_client.Counter(
    'delivered_count',
    'Number of Kafka messages delivered',
    labelnames=['topic', 'partition', 'successful'],
    namespace=__package__)

delivered_timestamp_seconds = prometheus_client.Gauge(
    'delivered_timestamp_seconds',
    'Timestamp of last Kafka message received',
    labelnames=['topic', 'partition', 'successful'],
    unit='seconds', namespace=__package__)
