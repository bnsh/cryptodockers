#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This program starts at block _1_ and verifies Unspent Transaction Outputs and amounts _and_ the scripts"""

import os
import re
import bz2
import pickle
import hashlib
from decimal import Decimal
from pprint import pprint

import ecdsa

from bitcoin_lib import grab_raw_proxy

def hasher(hashalg, value):
    hashalg = hashlib.new(hashalg)
    hashalg.update(value)
    return hashalg.digest()

def tohex(byts):
    return "".join(f"{int(val):02x}" for val in byts)

def extract_ecdsa_rs(dersig):
# 30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e
    assert int(dersig[0]) == 0x30 # ASN.1 Sequence
    full_length = int(dersig[1])
    assert full_length + 2 == len(dersig)
    assert int(dersig[2]) == 0x02 # ASN.1 Int
    rlen = int(dersig[3])
    rbytes = dersig[4:(4+rlen)]
    assert int(dersig[4+rlen]) == 0x02 # ASN.1 Int
    slen = int(dersig[5+rlen])
    sbytes = dersig[(5+rlen+1):(5+rlen+1+slen)]
    return rbytes[-32:] + sbytes[-32:]

def extract_signature_pubkey(script_sig_hex):
# 48
# 30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e01
# 41
# 042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb
    script_sig = bytearray.fromhex(script_sig_hex)
    length = int(script_sig[0])-1 # Minus one because this signature has a SIGHASH_ALL appended.
    pubkey_length = int(script_sig[1+length+1])
    pubkey = script_sig[(length+3):(length+3+pubkey_length)]
    return script_sig[1:1+length], pubkey

def update_construction(constructed, vin_idx, funding_script_hex):
    """Update vin_idx of constructed, which should be the raw_transaction _at first_, but
       will gradually get modified to be something to be hashed and verified."""

    funding_script = bytearray.fromhex(funding_script_hex)
    assert constructed[0:4] == bytearray.fromhex("01000000") # Version should be 1 (little endian). output: bytearray(b'\x01\x00\x00\x00')
    num_inputs = int(constructed[4]) #huh....the len is 4? what is constructed[4] then...?

    pos = 5
    positions = []
    for inpidx in range(0, num_inputs):
        spend_txid = constructed[pos:(pos+32)] # sha256 txid
        spend_idx = constructed[(pos+32):(pos+32+4)] # 32 bit index into utxo specified by txid (in the utxo which index are we talking about.)

        input_script_length = constructed[(pos+32+4)]
        positions.append((pos+32+4, pos+32+4+1+input_script_length))

        pos += 32+4+1+input_script_length+1
        pos += 4    # sequence number (Does this belong inside the loop or outside the loop? Basically is there a sequence number
                    # after each input, or after _all_ the inputs?)

    newconstruction = constructed[0:positions[vin_idx][0]] + bytearray([len(funding_script)]) + funding_script + constructed[positions[vin_idx][1]:]
    return newconstruction

#pylint: disable=too-many-locals,too-many-branches,too-many-statements
def verify(proxy, blockidx, utxos):
    """Verify a particular blockidx (this presumes the utxos here are valid.)"""
    
    # get the blockhash from block idx, and block from the hash
    blockhash = proxy.getblockhash(blockidx)
    block = proxy.getblock(blockhash)
    
    # calculate the block reward, which is lower the higher the block number is
    # block index doesn't necessarily correspond to block height...?
    half = Decimal(1) / Decimal(2)
    block_reward = 50 * half ** (blockidx//210000)

    transaction_ids = block["tx"]

    coinbase_amount = None
    total_tip = 0
    total_in = 0
    total_out = 0

    # find the pizza txn in our block
    for transaction_id in transaction_ids:
        raw_tx = proxy.getrawtransaction(transaction_id)
# I think the _actual_ pizza transaction is _not_ in block 57044, as per the stack exchange article, but in 57043.
# It's transaction id is a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d. Or perhaps more accurately,
# 57043 is some guy _buying_ the pizza with bitcoin
# 57044 is the pizza store person doing *something* with the bitcoin they just received.
        # if transaction_id in ("cca7507897abc89628f450e8b1e0c6fca4ec3f7b34cccf55f3f531c659ff4d79", "f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"):
        # if transaction_id in ("a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d",):
        if transaction_id in ("cca7507897abc89628f450e8b1e0c6fca4ec3f7b34cccf55f3f531c659ff4d79",):
            print("pizza", raw_tx)
        #pylint: disable=line-too-long

# Full piza transaction: 01000000018dd4f5fbd5e980fc02f35c6ce145935b11e284605bf599a13c6d415db55d07a1000000008b4830450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e0141042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabbffffffff0200719a81860000001976a914df1bd49a6c9e34dfa8631f2c54cf39986027501b88ac009f0a5362000000434104cd5e9726e6afeae357b1806be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce3388fa1abd0fa88b06c44ce81e2234aa70fe578d455dac00000000

# What follows is our understanding of what is _in_ the pizza transaction
# Version (fixed at 1, little endian)
# 01000000

# number of inputs (?)
# 01 (1 byte)

# incoming transaction (coins that we will spend)
# 8dd4f5fbd5e980fc02f35c6ce145935b11e284605bf599a13c6d415db55d07a1 => reversed becomes a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d

# index 0
# 00000000

# script: 8b = 8 * 16 + 11 = 139 bytes or 278 hexadecimal digits
# 8b
#     (These are all _under_ the "8b (139 bytes)" that is mentioned above.)
#     48 <= Length of Signature
#     30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e01
#     41 <= Length of public address
#     042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb

# sequence number
# ffffffff

# number of outputs (?)
# 02

# 1st output
# Amount
# 00719a8186000000 => reversed and turned to an int becomes 577700000000 satoshis

# lock script length
# 19

# lock script
# 76a914df1bd49a6c9e34dfa8631f2c54cf39986027501b88ac

# 2nd output
# Amount
# 009f0a5362000000 => reversed and turned to an int becomes 422300000000 satoshis

# lock script length
# 43
# 4104cd5e9726e6afeae357b1806be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce3388fa1abd0fa88b06c44ce81e2234aa70fe578d455dac

# What is this? (last 8 bytes)
# Locktime (0 in this case)
# 00000000

# We don't know what the first 9 bytes are and the last 8 bytes are.)
        #pylint: enable=line-too-long
        # raw_tx_bytes = bytes([int((raw_tx[x:(x+2)]), 16) for x in range(0, len(raw_tx), 2)])
        # raw_tx_sha256_1 = hashlib.sha256(raw_tx_bytes).digest()
        # raw_tx_sha256_2 = hashlib.sha256(raw_tx_sha256_1).digest() # Think about endian-ness tho.
        # raw_tx_hash = raw_tx_sha256_2
        
        # get the inputs and outputs in the transaction we're looking at
        decoded_tx = proxy.decoderawtransaction(raw_tx)
        vins = decoded_tx["vin"]
        vouts = decoded_tx["vout"]

        # EITHER a coinbase is in our vins, or it's not in _any_ of them.
        # coinbase transactions ONLY contain the coinbase (len == 1)
        assert (all("coinbase" in vin for vin in vins) and len(vins) == 1) or all("coinbase" not in vin for vin in vins)
        in_amount = 0
        out_amount = 0
        if all("coinbase" in vin for vin in vins) and len(vins) == 1:
            # If this is the coinbase transaction, the output is all part of the coinbase txn
            assert coinbase_amount is None
            coinbase_amount = sum(vout["value"] for vout in vouts)
            tip = 0
        else:
            # non-coinbase txns include miner tips 
            in_amount = sum(utxos[(vin["txid"], vin["vout"])]["value"] for vin in vins if "coinbase" not in vin)
            out_amount = sum(vout["value"] for vout in vouts)
            tip = in_amount - out_amount
        
        # block totals
        total_in += in_amount
        total_out += out_amount
        total_tip += tip

        if tip != 0:
            print(f"{blockidx:d}: {transaction_id:s} tip: {tip}")

        # tips should be at least 0
        # miners "pouring one out for Satoshi" claim 0 tips
        # rude transactors could also not leave a tip, I guess 
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

        constructed = bytearray.fromhex(raw_tx)
        dersig = None
        pubkey = None
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
                    # https://en.bitcoin.it/wiki/Script

                    print(f"{blockidx:d}: {transaction_id:s}:{vin_idx:d}: Burned {purported_spend_txid:s}:{purported_spend_idx:d}")
                    # 170: f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16:0: Burned 0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9:0

                    if transaction_id == "cca7507897abc89628f450e8b1e0c6fca4ec3f7b34cccf55f3f531c659ff4d79":
                        print("vin")
                        pprint(vin)
# 48 = 64+8 = 72
# 30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e01
# 41
# 042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb
# 042e930f39ba...dcebcabb somehow maps to 17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ: Come back to this later.
# 17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ => 
                        print("utxo")
                        pprint(utxos[(purported_spend_txid, purported_spend_idx)])


# vin
# {'scriptSig': {'asm': '30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e[ALL] '
#                       '042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb',
#                'hex': '4830450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e0141042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb'},
#  'sequence': 4294967295,
#  'txid': 'a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d',
#  'vout': 0}
# utxo
# {'n': 0,
#  'scriptPubKey': {'address': '17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ',
#                   'asm': 'OP_DUP OP_HASH160 '
#                          '46af3fb481837fadbb421727f9959c2d32a36829 '
#                          'OP_EQUALVERIFY OP_CHECKSIG',
#                   'hex': '76a91446af3fb481837fadbb421727f9959c2d32a3682988ac',
#                   'type': 'pubkeyhash'},
#  'value': Decimal('10000.00000000')}

# OP_DUP OP_HASH160 46af3fb481837fadbb421727f9959c2d32a36829 OP_EQUALVERIFY OP_CHECKSIG
# 1976a91446af3fb481837fadbb421727f9959c2d32a3682988ac
# 19 is the length (16+9 = 25 bytes)
# 76 is OP_DUP (?)
# a9 is OP_HASH160 (?)
# 14 is a length
# 46af3fb481837fadbb421727f9959c2d32a36829
# 88 is OP_EQUALVERIFY (?)
# ac is OP_CHECKSIG
                    

                    # comp_str = utxos[(purported_spend_txid, purported_spend_idx)]["scriptPubKey"]["asm"][0:130]
                    # verifying_key = VerifyingKey.from_string(bytearray.fromhex(comp_str), curve=NIST256p)
                    # verifying_key.verify(sig, tx_hash)
                    # # sig should be a bytesarray of size 64
                    # # tx_hash is arbitrary sized, but since it's a sha256(sha256(transaction)) it'll be 256 bits = 32 bytes long.

                    dersig, pubkey = extract_signature_pubkey(vin["scriptSig"]["hex"])
                    constructed = update_construction(constructed, vin_idx, utxos[(purported_spend_txid, purported_spend_idx)]["scriptPubKey"]["hex"])
                    del utxos[(purported_spend_txid, purported_spend_idx)]
                else:
                    print("HOLY SHIT BATMAN!")
                    pprint(vin)
                    pprint(utxos)
                    raise Exception("OH NO!")

        sighash_all = bytearray.fromhex("01000000")
        constructed = constructed + sighash_all
        
        sha256_hash = hasher("sha256", constructed)
        if dersig is None:
            print("HOLY SHIT")
        else:
            ecdsasig = extract_ecdsa_rs(dersig)
            verkey = ecdsa.VerifyingKey.from_string(pubkey, curve=ecdsa.SECP256k1)
            verkey.verify(ecdsasig, sha256_hash, hashlib.sha256)
            print("WOOT!")
        # Update the Unspent Transaction Outputs with this blocks outputs.
        utxos.update({(transaction_id, vout_idx): vout for vout_idx, vout in enumerate(vouts)})

    assert coinbase_amount is not None
    assert total_tip == total_in - total_out
    assert coinbase_amount == block_reward + total_tip, (coinbase_amount, block_reward, total_tip)
#pylint: enable=too-many-locals,too-many-branches,too-many-statements

def retrieve_utxos(utxofn=None):
    if utxofn is None:
        utxos_dir = "/tmp/utxos"
        # utxos_re is utxos-57044.pickle.bz2 right now
        utxos_re = re.compile(r'^(.*/)?utxos-([0-9]+).pickle.bz2')
        # sort the utxo filenames for the specified utxos (come back to this line)
        utxofns = sorted([os.path.join(utxos_dir, fname) for fname in os.listdir(utxos_dir) if utxos_re.match(fname) is not None], key=lambda fname: int(utxos_re.match(fname).group(2)), reverse=True)
        # we care about the first utxo (ugh...why again?)
        utxofn = utxofns[0]
    with bz2.open(utxofn, "rb") as pfp:
        raw = pickle.load(pfp)
        return raw["utxos"], raw["blockidx"]

def main():
    proxy = grab_raw_proxy()

    utxos, blockidx = retrieve_utxos("utxos-57044.pickle.bz2")

    verify(proxy, blockidx, utxos)

if __name__ == "__main__":
    main()
