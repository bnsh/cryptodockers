#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Test bitcoin api
    requires python3 -m pip install -U python-bitcoinlib
    Also, a better way needs to be found to copy the cookie.
    What a giant pain.
"""

import os
import tempfile
from subprocess import check_call
from bitcoin.rpc import RawProxy
from common_config import grab_config

def grab_remote_cookie():
    config = grab_config()
    scplocation = config["SCPLOCATION"]
    scphost = config["SCPHOST"]

    for remove in ("SSH_AGENT_PID", "SSH_AUTH_SOCK"):
        if remove in os.environ:
            del os.environ[remove]
    # scp the cookie
    with tempfile.TemporaryDirectory() as tmpdir:
        cookiefilename = os.path.join(tmpdir, "cookie")
        check_call([
            scplocation,
            "-q",
            f"{scphost:s}:/this/location/should/be/cookie",
            cookiefilename
        ])
        with open(cookiefilename, "rt", encoding="utf-8") as cfp:
            cookie = cfp.read()
    return cookie

def grab_raw_proxy():
    config = grab_config()
    host = config["BITCOINHOST"]
    port = int(config["BITCOINPORT"])

    cookie_fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bitcoin-cookie")
    proxy = None
    if os.path.exists(cookie_fn):
        cookie = None
        with open(cookie_fn, "rt", encoding="utf-8") as cookiefp:
            cookie = cookiefp.read()
        if cookie:
            try:
                proxy = RawProxy(service_url=f"http://{cookie:s}@{host:s}:{port:d}/bitcoin/")
            except bitcoin.rpc.JSONRPCError:
                os.unlink(cookie_fn)
                proxy = None
    if proxy is None:
        cookie = grab_remote_cookie()
        try:
            proxy = RawProxy(service_url=f"http://{cookie:s}@{host:s}:{port:d}/bitcoin/")
        except bitcoin.rpc.JSONRPCError:
            proxy = None
        if proxy is not None:
            with open(cookie_fn, "wt", encoding="utf-8") as cookiefp:
                cookiefp.write(cookie)
    return proxy

def main():
    proxy = grab_raw_proxy()
    if proxy:
        info = proxy.getblockchaininfo()
        print(info["blocks"])

if __name__ == "__main__":
    main()
