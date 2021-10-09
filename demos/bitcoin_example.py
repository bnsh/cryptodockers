#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Test bitcoin api
    requires python3 -m pip install -U python-bitcoinlib
    Also, a better way needs to be found to copy the cookie.
    What a giant pain.
"""

import os
import io
import configparser
import tarfile
import docker
from bitcoin.rpc import RawProxy

def grab_user():
    config = configparser.ConfigParser()
    localmkfn = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../local.mk"))
    with open(localmkfn, "rt", encoding="utf-8") as cfp:
        config.read_string(f"[DEFAULT]\n{cfp.read():s}\n")
    return config["DEFAULT"]["USERNAME"]

def grab_cookie():
    name = f"{grab_user()}/bitcoin_node:latest"
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
