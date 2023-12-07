#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Check for high bitcoin miners"""

import json
import decimal
from collections import Counter

from tqdm import tqdm

from bitcoin_lib import grab_raw_proxy

def json_handler(data):
    if isinstance(data, decimal.Decimal):
        return float(data)
    raise TypeError(f'Object of type {data.__class__.__name__} is not JSON serializable')

def report(block_idx, window):
    ctr = Counter([spk for _, spk in window])
    print(block_idx, ctr.most_common())

def grab_transaction(proxy, coinbase_txid, depth=0):
    trans = proxy.decoderawtransaction(proxy.getrawtransaction(coinbase_txid))
    if depth == 0:
        vins = trans["vin"]
        for vin in tqdm(vins, ncols=0, leave=False, desc="single_transaction"):
            if "txid" in vin:
                decoded = grab_transaction(proxy, vin["txid"], depth=1+depth)
                vin["decoded_inputs"] = [blah["scriptPubKey"]["address"] for blah in decoded["vout"] if "scriptPubKey" in blah and "address" in blah["scriptPubKey"]]
    return trans

def main():
    proxy = grab_raw_proxy()
    targets = set(["38XnPvu9PmonFU9WouPXUjYbW91wa5MerL"])
    window = []

    for block_idx in range(819842, -1, -1):
        # Get the block hash of block block_idx
        block_hash = proxy.getblockhash(block_idx)

        # Retrieve the block based on the hash
        block = proxy.getblock(block_hash)

        # The first transaction in the block is the coinbase transaction
        coinbase_txid = block['tx'][0]

        # Retrieve the details of the coinbase transaction
        coinbase_tx = proxy.getrawtransaction(coinbase_txid, True)

        script_pub_key = coinbase_tx["vout"][0]["scriptPubKey"]["address"]
        if script_pub_key in targets or block_idx == 819842:
            augmented = [(txid, grab_transaction(proxy, txid)) for txid in tqdm(block['tx'], ncols=0, leave=True, desc=f"augmenting block {block_idx:d}")]
            block["augmented"] = augmented
            with open(f"/tmp/blocks/{block_idx:08d}.json", "wt", encoding="utf-8") as jsfp:
                json.dump(block, jsfp, indent=4, sort_keys=True, default=json_handler)
            break
        window.append((block_idx, script_pub_key))
        if len(window) > 144:
            window = window[1:]
            report(block_idx, window)

if __name__ == "__main__":
    main()
