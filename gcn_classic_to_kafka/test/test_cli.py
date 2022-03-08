#
# Copyright © 2022 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. No copyright is claimed
# in the United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# SPDX-License-Identifier: NASA-1.3
#
from .. import cli


def test_kafka_config_from_env():
    env = {
        'FOO_BAR_BAT__BAZ___': '123',
        'XYZZ_BAR_BAT__BAZ___': '456'
    }
    config = cli.kafka_config_from_env(env, 'FOO_')
    assert config == {'bar.bat-baz_': '123'}
