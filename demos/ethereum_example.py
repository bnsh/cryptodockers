#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Ethereum example."""

from web3 import Web3

def main():
    eth = Web3(Web3.HTTPProvider('http://raspberrypi2.home.hex21.com:19142/ethereum/'))
    if eth.isConnected():
        print(eth.eth.get_block('latest'))

if __name__ == "__main__":
    main()
