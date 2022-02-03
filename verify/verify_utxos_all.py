#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This program starts at block _1_ and verifies Unspent Transaction Outputs and amounts _and_ the scripts"""

import hashlib
from decimal import Decimal
from pprint import pprint

from ecdsa import VerifyingKey, SECP256k1

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
        # 0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000
        raw_tx_bytes = bytes([int((raw_tx[x:(x+2)]), 16) for x in range(0, len(raw_tx), 2)])
        raw_tx_sha256_1 = hashlib.sha256(raw_tx_bytes).digest()
        raw_tx_sha256_2 = hashlib.sha256(raw_tx_sha256_1).digest() # Think about endian-ness tho.
        raw_tx_hash = raw_tx_sha256_2
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
	
        if tip != 0:
            print(f"{blockidx:d}: {transaction_id:s} tip: {tip}")

        if tip < 0:
            print(f"blockidx: {blockidx:d}")
            print(f"blockhash: {blockhash:s}")
            print(f"transaction_id: {transaction_id:s}")
            print(f"tip: {tip}")
            print("ins")
            for vin in vins:
                if "coinbase" not in vin:
                    print(f"    {utxos[(vin['txid'], vin['vout'])]['value']}")
            print("outs")
            for vout in vouts:
                print(f"    {vout['value']}")

            print(f"out_amount: {out_amount}")
            print(f"in_amount: {in_amount}")
            print(f"coinbase_amount: {coinbase_amount}")
        assert tip >= 0, (blockidx, blockhash, transaction_id, tip)

        for vin_idx, vin in enumerate(vins):
            # Coinbase transactions have no "inputs" to check, they come from God (Satoshi).
            if "coinbase" not in vin:
                purported_spend_txid = vin["txid"]
                purported_spend_idx = vin["vout"]
                # This pair _must_ be in our Unspent Transaction Outputs.
                if (purported_spend_txid, purported_spend_idx) in utxos:
                    # https://en.bitcoin.it/wiki/OP_CHECKSIG
                    # https://en.bitcoin.it/w/images/en/7/70/Bitcoin_OpCheckSig_InDetail.png
                    # https://www.blockchain.com/btc/block/170
                    # Let's use block 170 as in that doc in these comments:
                    # Pizza transaction explanation: https://bitcoin.stackexchange.com/questions/32305/how-does-the-ecdsa-verification-algorithm-work-during-transaction

                    print(f"{blockidx:d}: {transaction_id:s}:{vin_idx:d}: Burned {purported_spend_txid:s}:{purported_spend_idx:d}")
                    # 170: f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16:0: Burned 0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9:0

                    if transaction_id == "cca7507897abc89628f450e8b1e0c6fca4ec3f7b34cccf55f3f531c659ff4d79":
                        pprint(vin)
                    #
# 304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d09
# 30440220
# 4e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd41
# 0220
# 181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d09
# 01
                    #     {'scriptSig': {'asm': '304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d09[ALL]',
                    #                    'hex': '47304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901'},
                    #      'sequence': 4294967295,
                    #      'txid': '0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9',
                    #      'vout': 0}

                        pprint(utxos[(purported_spend_txid, purported_spend_idx)])
                    # TODO: Somehow we need to take the vin["scriptSig"]["asm"] and utxos[(...)]["scriptPubKey"]["asm"] and verify this...
                    #       As stated here, it presumes OP_CHECKSIG tho. But, let's cross the more complicated transactions after we figure
                    #       out the ecdsa business.
                    #     {'n': 0,
                    #      'scriptPubKey': {'asm': '0411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3 '
                    #                              'OP_CHECKSIG',
                    #                       'hex': '410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac',
                    #                       'type': 'pubkey'},
                    #      'value': Decimal('50.00000000')}


                    # comp_str = utxos[(purported_spend_txid, purported_spend_idx)]["scriptPubKey"]["asm"][0:130]
                    # verifying_key = VerifyingKey.from_string(bytearray.fromhex(comp_str), curve=NIST256p)
                    # verifying_key.verify(sig, tx_hash)
                    # # sig should be a bytesarray of size 64
                    # # tx_hash is arbitrary sized, but since it's a sha256(sha256(transaction)) it'll be 256 bits = 32 bytes long.

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
