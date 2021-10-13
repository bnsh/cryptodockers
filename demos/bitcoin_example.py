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
from bitcoin_common import grab_config

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
            f"{scphost}:/this/location/should/be/cookie",
            cookiefilename
        ])
        with open(cookiefilename, "rt", encoding="utf-8") as cfp:
            cookie = cfp.read()
    return cookie

def main():
    cookie = grab_remote_cookie()
    if cookie:
        proxy = RawProxy(service_url=f"http://{cookie}@raspberrypi.home.hex21.com:19142/bitcoin/")
        info = proxy.getblockchaininfo()
        print(info["blocks"])

if __name__ == "__main__":
    main()
