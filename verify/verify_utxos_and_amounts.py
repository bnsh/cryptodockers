#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This program starts at block _1_ and verifies Unspent Transaction Outputs and amounts.
   It does _not_ verify the scripts."""

from decimal import Decimal
from pprint import pprint
from bitcoin_lib import grab_raw_proxy

#pylint: disable=too-many-locals
def verify(proxy, blockidx, utxos):
    blockhash = proxy.getblockhash(blockidx)
    block = proxy.getblock(blockhash)
    half = Decimal(1) / Decimal(2)
    block_reward = 50 * half ** (blockidx//210000)

    transaction_ids = block["tx"]

    coinbase_amount = None
    total_tip = 0
    total_in = 0
    total_out = 0
    for transaction_id in transaction_ids:
        raw_tx = proxy.getrawtransaction(transaction_id)
        decoded_tx = proxy.decoderawtransaction(raw_tx)
        vins = decoded_tx["vin"]
        vouts = decoded_tx["vout"]

        # EITHER a coinbase is in our vins, or it's not in _any_ of them.
        assert (all("coinbase" in vin for vin in vins) and len(vins) == 1) or all("coinbase" not in vin for vin in vins)
        in_amount = 0
        out_amount = 0
        if all("coinbase" in vin for vin in vins) and len(vins) == 1:
            # If this is the coinbase transaction
            assert coinbase_amount is None
            coinbase_amount = sum(vout["value"] for vout in vouts)
            tip = 0
        else:
            in_amount = sum(utxos[(vin["txid"], vin["vout"])]["value"] for vin in vins if "coinbase" not in vin)
            out_amount = sum(vout["value"] for vout in vouts)
            tip = in_amount - out_amount

        total_in += in_amount
        total_out += out_amount
        total_tip += tip

        assert tip >= 0, (blockidx, blockhash, transaction_id, tip)

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

    assert coinbase_amount is not None
    assert total_tip == total_in - total_out
    assert coinbase_amount == block_reward + total_tip, (coinbase_amount, block_reward, total_tip)
#pylint: enable=too-many-locals

def main():
    proxy = grab_raw_proxy()

    utxos = {}
    maxblock = proxy.getblockchaininfo()["blocks"]

    for blockidx in range(1, maxblock):
        verify(proxy, blockidx, utxos)

if __name__ == "__main__":
    main()
