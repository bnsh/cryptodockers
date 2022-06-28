#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""
Hi.

We're trying to implement this code at https://bitcoin.stackexchange.com/a/32308/235711 in python with the
ecdsa library. Unfortunately, we're not clear on what language this code below is written in.. C++? C#?

const QByteArray xx ( QByteArray::fromHex ( "01000000018dd4f5fbd5e980fc02f35c6ce145935b11e284605bf599a13c6d41"
                                            "5db55d07a1000000001976a91446af3fb481837fadbb421727f9959c2d32a368"
                                            "2988acffffffff0200719a81860000001976a914df1bd49a6c9e34dfa8631f2c"
                                            "54cf39986027501b88ac009f0a5362000000434104cd5e9726e6afeae357b180"
                                            "6be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce33"
                                            "88fa1abd0fa88b06c44ce81e2234aa70fe578d455dac0000000001000000" ) );
const MyKey32 digest ( xx.constData ( ), xx.size ( ) ); // construct object of sha256 (sha256 ( xx ) )
_trace ( digest.toString ( ) );                         // print result
const QByteArray pubkey ( QByteArray::fromHex ( "042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb" ) );
const QByteArray signature ( QByteArray::fromHex ( "30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e" ) );
_trace ( QString ( "verify=%1" ).arg ( digest.verify ( pubkey, signature ) ) );
"""

import hashlib
import ecdsa

def from_hex(hexval):
    return bytes(int(hexval[idx:(idx+2)], 16) for idx in range(0, len(hexval), 2))

def to_hex(raw):
    return "".join(reversed([f"{int(val):02x}" for val in raw]))

def mykey32(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

#pylint: disable=invalid-name
def main():
    # We're preserving the same variable names as the sample code above
    # for clarity.
    xx = from_hex(
        "01000000018dd4f5fbd5e980fc02f35c6ce145935b11e284605bf599a13c6d41"
        "5db55d07a1000000001976a91446af3fb481837fadbb421727f9959c2d32a368"
        "2988acffffffff0200719a81860000001976a914df1bd49a6c9e34dfa8631f2c"
        "54cf39986027501b88ac009f0a5362000000434104cd5e9726e6afeae357b180"
        "6be25a4c3d3811775835d235417ea746b7db9eeab33cf01674b944c64561ce33"
        "88fa1abd0fa88b06c44ce81e2234aa70fe578d455dac0000000001000000"
    )
    digest = mykey32(xx)
    print(to_hex(digest)) # This clearly works as described in the post.

    pubkey = from_hex("042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb")
    dummy_signature = from_hex("30450221009908144ca6539e09512b9295c8a27050d478fbb96f8addbc3d075544dc41328702201aa528be2b907d316d2da068dd9eb1e23243d97e444d59290d2fddf25269ee0e")

    dummy_verkey = ecdsa.VerifyingKey.from_string(pubkey, curve=ecdsa.SECP256k1)

    # # This fails with ecdsa.keys.BadSignatureError: MalformedSignature('Invalid length of signature[...]')
    # # It seems like it wants a 64 byte signature.
    # verkey.verify(signature, digest)

    # How would we verify the pizza transaction as was done in the post
    # in python?
    # Thanks!
#pylint: enable=invalid-name

if __name__ == "__main__":
    main()
