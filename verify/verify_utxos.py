#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This program starts at block _1_ and _simply_ verifies Unspent Transaction Outputs.
   It does _not_ verify that enough money was in the inputs and outputs."""

from pprint import pprint
from bitcoin_lib import grab_raw_proxy

def verify(proxy, blockidx, utxos):
    blockhash = proxy.getblockhash(blockidx)
    block = proxy.getblock(blockhash)

    transaction_ids = block["tx"]

    for transaction_id in transaction_ids:
        raw_tx = proxy.getrawtransaction(transaction_id)
        decoded_tx = proxy.decoderawtransaction(raw_tx)
        vins = decoded_tx["vin"]
        vouts = decoded_tx["vout"]

        for vin_idx, vin in enumerate(vins):
            # Coinbase transactions have no "inputs" to check, they come from God (Satoshi).
            if "coinbase" not in vin:
                purported_spend_txid = vin["txid"]
                purported_spend_idx = vin["vout"]
                # This pair _must_ be in our Unspent Transaction Outputs.
                if (purported_spend_txid, purported_spend_idx) in utxos:
                    print(f"{blockidx:d}: {transaction_id:s}:{vin_idx:d}: Burned {purported_spend_txid:s}:{purported_spend_idx:d}")
                    del utxos[(purported_spend_txid, purported_spend_idx)]
                else:
                    print("HOLY SHIT BATMAN!")
                    pprint(vin)
                    pprint(utxos)
                    raise Exception("OH NO!")

        # Update the Unspent Transaction Outputs with this blocks outputs.
        utxos.update({(transaction_id, vout_idx): vout for vout_idx, vout in enumerate(vouts)})

def main():
    proxy = grab_raw_proxy()

    utxos = {}
    maxblock = proxy.getblockchaininfo()["blocks"]

    for blockidx in range(1, maxblock):
        verify(proxy, blockidx, utxos)

if __name__ == "__main__":
    main()
