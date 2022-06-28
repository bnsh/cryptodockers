#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Blah"""

import hashlib

import asn1
import ecdsa

def sha256_squared(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def hex2bin(hexval):
    return bytes(int(hexval[idx:(idx+2)], 16) for idx in range(0, len(hexval), 2))

def hex_rep(raw):
    return "".join(reversed([f"{int(val):02x}" for val in raw]))

def hex_rev(raw):
    return "".join([raw[idx:(idx+2)] for idx in range(len(raw)-2, -2, -2)])

def main():
    print(hex_rev("0123456789abcdef"), "efcdab8967452301")
    print(hex_rev("0123456789abcdef") == "efcdab8967452301")
    data = (
        "01000000018dd4f5fbd5e980fc02f35c6ce145935b11e284605bf599a13c6d41"
        "5db55d07a1000000001976a91446af3fb481837fadbb421727f9959c2d32a368"
        "2988acffffffff0200719a81860000001976a914df1bd49a6c9e34dfa8631f2c"
        "54cf39986027501b88ac009f0a5362000000434104cd5e9726e6afeae357b180"
        "6be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce33"
        "88fa1abd0fa88b06c44ce81e2234aa70fe578d455dac0000000001000000"
    )

    data_bytes = hex2bin(data)

# 692678553d1b85ccf87d4d4443095f276cdf600f2bb7dd44f6effbd7458fd4c2

    digest = bytes(reversed(sha256_squared(data_bytes)))
    digest = sha256_squared(data_bytes)
    print(hex_rep(digest))

    pubkey = hex2bin("042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb")
    # https://bitcoin.stackexchange.com/questions/12554/why-the-signature-is-always-65-13232-bytes-long
    # https://bitcoin.stackexchange.com/questions/107082/the-example-signature-in-bip143-doesnt-validate?rq=1 Seems promising.
    signature = hex2bin("30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e")
# 30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e
# 30 is the header byte indicating compound structure
# 45 is a length byte of what follows:
#     4 * 16 + 5 = 69: 69 * 2 = 138
#     0221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e
#     02 header byte indicating an integer
#     21 length descriptor for the R value (2 * 16 + 1 = 33)
#     R = 009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc413287
#     left with 02201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e
#     02 header byte indicating an integer
#     20 length descriptor for the S value (2 * 16 = 32)
#     S = 1aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e

    # sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    # data = "Supercalifragilisticespialodocious".encode("utf-8")
    # sig = sk.sign(data=data)
    # print(len(sig))
    # vk = sk.get_verifying_key()
    # print(dir(vk))
    # print(vk.verify(sig, data))
    # print(dir(vk))
    # exit()

    dec = asn1.Decoder()
    dec.start(signature)
    dummy_key, val = dec.read()
    dummy_hyp = val[5:(5+32)] + val[39:(39+32)]
    # hyp = val[37:(37+32)] + val[3:(3+32)]

    # verifying_key = ecdsa.VerifyingKey
    verkey = ecdsa.VerifyingKey.from_string(pubkey, curve=ecdsa.SECP256k1)
    for idx in range(0, len(signature)-64):
        try:
            verkey.verify(bytes(signature[idx:(idx+64)]), digest)
            print(f"WOOHOO! {idx:d}!")
            break
        except ecdsa.keys.BadSignatureError as bse:
            print(bse)

#     sig = somemagicfunction(pubkey, digest)
# const QByteArray pubkey ( QByteArray::fromHex ( "042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb" ) );
# const QByteArray signature ( QByteArray::fromHex ( "30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e" ) )

if __name__ == "__main__":
    main()
