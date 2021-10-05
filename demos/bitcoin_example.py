#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Test bitcoin api
    requires python3 -m pip install -U python-bitcoinlib
    Also, a better way needs to be found to copy the cookie.
    What a giant pain.
"""

import io
import tarfile
import docker
from bitcoin.rpc import RawProxy

def grab_cookie():
    name = "binesh/bitcoin_node:latest"
    client = docker.from_env()
    cookie = None
    for container in client.containers.list():
        if name in set(container.image.attrs["RepoTags"]):
            stream, dummy_stat = container.get_archive("/home/bitcoin/.bitcoin/.cookie")
            tarbin = b"".join(chunk for chunk in stream)
            with tarfile.open(mode="r", fileobj=io.BytesIO(tarbin)) as tarf:
                cookiefile = tarf.getmember(".cookie")
                cookie = tarf.extractfile(cookiefile).read().decode("utf-8")
    return cookie


def main():
    cookie = grab_cookie()
    if cookie:
        proxy = RawProxy(service_url=f"http://{cookie}@localhost:8332/")
        info = proxy.getblockchaininfo()
        print(info["blocks"])

if __name__ == "__main__":
    main()
