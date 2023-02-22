import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


def main() -> None:
    argparser = argparse.ArgumentParser('wg_cli')
    argparser.add_argument('name')
    argparser.add_argument('address')
    args = argparser.parse_args()

    wg_keys, wg_peer, wg_client_conf = add_client(
        wg_keys=generate_keys(),
        address=args.address,
        server_public_key=str(Path('publickey').read_text(encoding='utf-8')).strip(),
        endpoint=str(Path('endpoint').read_text(encoding='utf-8')).strip(),
    )

    print('Append the peer to wg0.conf')
    with Path('wg0.conf').open(mode='a', encoding='utf-8') as file:
        file.write(make_peer(wg_peer))

    print(f'Create {args.name}.conf')
    Path(f'{args.name}.conf').write_text(
        make_client_conf(wg_client_conf), encoding='utf-8'
    )

    print(f'Create {args.name}_privatekey')
    Path(f'{args.name}_privatekey').write_text(wg_keys.private_key, encoding='utf-8')

    print(f'Create {args.name}_publickey')
    Path(f'{args.name}_publickey').write_text(wg_keys.public_key, encoding='utf-8')


@dataclass
class WireguardKeys:
    private_key: str
    public_key: str


@dataclass
class WireguardPeer:
    public_key: str
    allowed_ips: str


@dataclass
class WireguardClientConf:
    # interface
    private_key: str
    address: str
    dns: str

    # peer
    public_key: str
    endpoint: str
    allowed_ips: str
    persistent_keepalive: int


def generate_keys() -> WireguardKeys:
    private_key = subprocess.run(
        ["wg", "genkey"], encoding="utf-8", stdout=subprocess.PIPE
    ).stdout.strip()
    public_key = subprocess.run(
        ["wg", "pubkey"], encoding="utf-8", stdout=subprocess.PIPE, input=private_key
    ).stdout.strip()
    return WireguardKeys(private_key=private_key, public_key=public_key)


def add_client(
    wg_keys: WireguardKeys,
    address: str,
    server_public_key: str,
    endpoint: str,
) -> Tuple[WireguardKeys, WireguardPeer, WireguardClientConf]:
    wg_peer = WireguardPeer(public_key=wg_keys.public_key, allowed_ips=address)

    wg_client_conf = WireguardClientConf(
        private_key=wg_keys.private_key,
        address=address,
        dns='8.8.8.8',
        public_key=server_public_key,
        endpoint=endpoint,
        allowed_ips='0.0.0.0/0',
        persistent_keepalive=20,
    )

    return wg_keys, wg_peer, wg_client_conf


def make_peer(peer: WireguardPeer) -> str:
    return (
        '[Peer]\n'
        f'PublicKey = {peer.public_key}\n'
        f'AllowedIPs = {peer.allowed_ips}\n'
    )


def make_client_conf(conf: WireguardClientConf) -> str:
    return (
        '[Interface]\n'
        f'PrivateKey = {conf.private_key}\n'
        f'Address = {conf.address}\n'
        f'DNS = {conf.dns}\n'
        '\n'
        '[Peer]\n'
        f'PublicKey = {conf.public_key}\n'
        f'Endpoint = {conf.endpoint}\n'
        f'AllowedIPs = {conf.allowed_ips}\n'
        f'PersistentKeepalive = {conf.persistent_keepalive}\n'
    )
