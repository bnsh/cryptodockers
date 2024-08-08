#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Test bitcoin api
    requires python3 -m pip install -U python-bitcoinlib
    Also, a better way needs to be found to copy the cookie.
    What a giant pain.
"""

import sys
import os
import re
import bz2
import pickle
import tempfile
from subprocess import check_call
import bitcoin.rpc as bitcoin_rpc
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

    cookie_fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bitcoin-cookie")
    proxy = None
    if os.path.exists(cookie_fn):
        cookie = None
        with open(cookie_fn, "rt", encoding="utf-8") as cookiefp:
            cookie = cookiefp.read()
        if cookie:
            try:
                proxy = bitcoin_rpc.RawProxy(service_url=f"http://{cookie:s}@{host:s}/bitcoin/")
                # Check to see if the proxy is valid.
                dummy_info = proxy.getblockchaininfo()
            except bitcoin_rpc.JSONRPCError:
                os.unlink(cookie_fn)
                proxy = None
    if proxy is None:
        cookie = grab_remote_cookie()
        try:
            proxy = bitcoin_rpc.RawProxy(service_url=f"http://{cookie:s}@{host:s}/bitcoin/")
            # Check to see if the proxy is valid.
            dummy_info = proxy.getblockchaininfo()
        except bitcoin_rpc.JSONRPCError:
            proxy = None
        if proxy is not None:
            with open(cookie_fn, "wt", encoding="utf-8") as cookiefp:
                cookiefp.write(cookie)
    return proxy

def dump_utxos(blockidx, utxos):
    fname = f"/tmp/utxos/utxos-{blockidx:d}.pickle.bz2"
    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname), mode=0o775)
    with bz2.open(fname, "wb") as pfp:
        pickle.dump({
            "blockidx": blockidx,
            "utxos": utxos
        }, pfp)
    print(f"{fname:s}\t{os.stat(fname).st_size:d}")

def retrieve_utxos(utxofn=None):
    if utxofn is None:
        utxos_dir = "/tmp/utxos"
        utxofn = None
        if os.path.exists(utxos_dir):
            utxos_re = re.compile(r'^(.*/)?utxos-([0-9]+).pickle.bz2')
            utxofns = sorted([os.path.join(utxos_dir, fname) for fname in os.listdir(utxos_dir) if utxos_re.match(fname) is not None], key=lambda fname: int(utxos_re.match(fname).group(2)), reverse=True)
            utxofn = utxofns[0]

    utxos, blockidx = {}, 0
    if utxofn is not None:
        with bz2.open(utxofn, "rb") as pfp:
            sys.stderr.write(f"Loading {utxofn:s}...\n")
            raw = pickle.load(pfp)
            sys.stderr.write(f"Loaded {utxofn:s}\n")
            utxos, blockidx = raw["utxos"], raw["blockidx"]

    return utxos, blockidx

def main():
    proxy = grab_raw_proxy()
    if proxy:
        info = proxy.getblockchaininfo()
        print(info["blocks"])

if __name__ == "__main__":
    main()
