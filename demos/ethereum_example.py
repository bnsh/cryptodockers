#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Ethereum example."""

from web3 import Web3
from common_config import grab_config

def hexify(bts):
    blah = "".join(f"{x:02x}" for x in bts)
    return f"0x{blah:s}"

def main():
    config = grab_config()
    host = config["ETHEREUMHOST"]
    web3 = Web3(Web3.HTTPProvider(f'http://{host:s}/ethereum/'))
    if web3.isConnected():
        latest_block = web3.eth.get_block('latest')
        highest_block_number = latest_block.number
        for block_number in range(highest_block_number, -1, -1):
            block = web3.eth.get_block(block_number)
            for txidx, transaction in enumerate(block.transactions):
                trans = web3.eth.getTransaction(transaction)
                if trans.to is None:
                    print(block_number, txidx, trans)

        # trans = web3.eth.getTransaction("0xf6236641198c21e52d0be39635616dd4b6432a5a5bc9ce11edb7b48fe2782ab1")
        # print(trans)


#         print(dir(web3.eth))
#         code = web3.eth.getCode("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
#         hexcode = "".join(f"{x:02x}" for x in code)
#         print(hexcode)

if __name__ == "__main__":
    main()
