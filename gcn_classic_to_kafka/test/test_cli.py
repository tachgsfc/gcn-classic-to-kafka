from .. import cli


def test_kafka_config_from_env():
    env = {
        'FOO_BAR_BAT__BAZ___': '123',
        'XYZZ_BAR_BAT__BAZ___': '456'
    }
    config = cli.kafka_config_from_env(env, 'FOO_')
    assert config == {'bar.bat-baz_': '123'}
