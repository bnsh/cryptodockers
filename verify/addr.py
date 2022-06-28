#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""How do bitcoin addresses work??"""

import hashlib
import base58

def hasher(hashalg, value):
    hashalg = hashlib.new(hashalg)
    hashalg.update(value)
    return hashalg.digest()

def main():
    pubkey = bytearray.fromhex("042e930f39ba62c6534ee98ed20ca98959d34aa9e057cda01cfd422c6bab3667b76426529382c23f42b9b08d7832d4fee1d6b437a8526e59667ce9c4e9dcebcabb")
# Expect: 17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ
# 34 base58 digits.
# l(value) / l(58) = 34
# We want l(value) / l(256) for number of bytes.
# l(value) / l(58) * l(58) / l(256) = l(value) / l(256)
# 34 * l(58) / l(256) = 25 bytes.
    payload = hasher("ripemd160", hasher("sha256", pubkey))
    version = bytearray([0])
    checksum = hasher("sha256", hasher("sha256", version + payload))[0:4]
    bitcoin_address = base58.b58encode(version + payload + checksum).decode("utf-8")
    assert bitcoin_address == "17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ", bitcoin_address
    print("WOO HOO!")

if __name__ == "__main__":
    main()
