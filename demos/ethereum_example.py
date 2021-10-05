#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Ethereum example."""

from web3 import Web3

def main():
    eth = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    if eth.isConnected():
        print(eth.eth.get_block('latest'))

if __name__ == "__main__":
    main()
