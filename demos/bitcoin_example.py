#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Bitcoin example: From Page 49 of "Mastering Bitcoin", just made pylint clean is all."""

from bitcoin_lib import grab_raw_proxy()

def main():
    proxy = grab_raw_proxy()
    info = proxy.getblockchaininfo()
    print(info["blocks"])

if __name__ == "__main__":
    main()
