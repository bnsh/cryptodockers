#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Ethereum example."""

from common_config import grab_config
from web3 import Web3

def main():
    config = grab_config()
    host = config["REMOTEHOST"]
    port = int(config["REMOTEPORT"])
    eth = Web3(Web3.HTTPProvider('http://{host:s}:{port:d}/ethereum/'))
    if eth.isConnected():
        print(eth.eth.get_block('latest'))

if __name__ == "__main__":
    main()
