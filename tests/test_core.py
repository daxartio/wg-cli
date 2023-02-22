from wg_cli.core import (
    WireguardClientConf,
    WireguardKeys,
    WireguardPeer,
    add_client,
    make_client_conf,
    make_peer,
)


def test_add_client():
    wg_keys, wg_peer, wg_client_conf = add_client(
        wg_keys=WireguardKeys('pkey', 'pubkey'),
        address='10.0.0.5/32',
        server_public_key='5cbISqOl5ospTztHylliT1H4oEV38tfbFKZXcq7xMGc=',
        endpoint='localhost:51830',
    )

    assert wg_keys
    assert wg_peer
    assert wg_client_conf


def test_make_peer():
    assert make_peer(WireguardPeer('pkey', '10.0.0.5/32'))


def test_make_client_conf():
    assert make_client_conf(
        WireguardClientConf(
            private_key='private_key',
            address='address',
            dns='dns',
            public_key='public_key',
            endpoint='endpoint',
            allowed_ips='allowed_ips',
            persistent_keepalive='persistent_keepalive',
        )
    )
