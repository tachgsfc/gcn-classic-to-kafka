#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
"""Common utilities for all GCN Notice formats."""

import gcn


def topic_for_notice_type(notice_type, flavor):
    """Get a Kafka topic name for the given GCN Classic notice type.

    Parameters
    ----------
    notice_type : int
        The notice type. For possible values, see :class:`gcn.NoticeType`.
    flavor : str
        The GCN format flavor.

    Returns
    -------
    str
        The Kafka topic corresponding to the notice type.

    Example
    -------

    >>> kafka_topic_for_notice_type(150, 'voevent')
    'gcn.classic.voevent.LVC_PRELIMINARY'

    >>> kafka_topic_for_notice_type(5000, 'voevent')
    'gcn.classic.voevent.UNKNOWN'

    """
    try:
        notice_type_enum = gcn.NoticeType(notice_type)
    except ValueError:
        notice_type_str = 'UNKNOWN'
    else:
        notice_type_str = notice_type_enum.name
    return f'gcn.classic.{flavor}.{notice_type_str}'
