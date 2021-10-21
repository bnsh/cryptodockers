#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Ethereum example."""

from web3 import Web3
from common_config import grab_config

def main():
    config = grab_config()
    host = config["ETHEREUMHOST"]
    port = int(config["ETHEREUMPORT"])
    eth = Web3(Web3.HTTPProvider(f'http://{host:s}:{port:d}/ethereum/'))
    if eth.isConnected():
        print(eth.eth.get_block('latest'))

if __name__ == "__main__":
    main()
