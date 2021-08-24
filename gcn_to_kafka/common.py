"""Common utilities for all GCN Notice formats."""

import gcn


def kafka_topic_for_notice_type(notice_type, flavor):
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

    """
    notice_type_str = gcn.NoticeType(notice_type).name
    return f'gcn.classic.{flavor}.{notice_type_str}'
