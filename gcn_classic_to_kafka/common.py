#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
"""Common utilities for all GCN Notice formats."""

import gcn


def notice_type_int_to_str(notice_type_int):
    """Convert an integer notice type to a string.

    Parameters
    ----------
    notice_type_int : int
        The notice type. For possible values, see :class:`gcn.NoticeType`.
    flavor : str
        The GCN format flavor.

    Returns
    -------
    str
        The Kafka topic corresponding to the notice type.

    Example
    -------

    >>> notice_type_int_to_str(150, 'voevent')
    'LVC_PRELIMINARY'

    >>> notice_type_int_to_str(5000, 'voevent')
    'UNKNOWN'

    """
    try:
        notice_type_enum = gcn.NoticeType(notice_type_int)
    except ValueError:
        notice_type_str = 'UNKNOWN'
    else:
        notice_type_str = notice_type_enum.name
    return notice_type_str


def topic_for_notice_type_str(notice_type_str, flavor):
    """Get a Kafka topic name for the given GCN Classic notice type string.

    Parameters
    ----------
    notice_type_str : str
        The notice type string, as returned :meth:`notice_type_int_to_str`.
    flavor : str
        The GCN format flavor.

    Returns
    -------
    str
        The Kafka topic corresponding to the notice type.

    Example
    -------

    >>> topic_for_notice_type('LVC_PRELIMINARY', 'voevent')
    'gcn.classic.voevent.LVC_PRELIMINARY'

    """
    return f'gcn.classic.{flavor}.{notice_type_str}'
