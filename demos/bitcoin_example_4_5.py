#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This is Example 4-5 on page 77 of "Mastering Bitcoin" by Andreas M. Antonopoulos

    The original example used pybitcointools from Vitalik Buterin (of Ethereum fame), but that
        git repo now says:
            "I really don't have time to maintain this library further. If you want to fork it or use it despite lack of maintenance, feel free to clone locally and revert one commit.

            This externally-maintained fork looks good though I did not personally write it so can't vouch for security: https://github.com/primal100/pybitcointools"
        -- https://github.com/vbuterin/pybitcointools

    So, we went there: https://github.com/primal100/pybitcointools
        which _also_ says:
            "REPOSITORY HAS BEEN ARCHIVED AND IS NO LONGER MAINTAINED FOR NOW"
        but, let's plow ahead, and try anyway. And, yes, this works as a dropin replacement for "bitcoin" in the example.
"""

import cryptos

def main():
    valid_private_key = False
    while not valid_private_key:
        private_key = cryptos.random_key()
        decoded_private_key = cryptos.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < cryptos.N

if __name__ == "__main__":
    main()
