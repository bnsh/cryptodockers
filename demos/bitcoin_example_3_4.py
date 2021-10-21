#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""Example 3-4 from Mastering Bitcoin"""

from bitcoin_lib import grab_raw_proxy

def main():
    proxy = grab_raw_proxy()

    # Alice's transaction ID
    txid = "0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2"

    # First, retrieve the raw transaction in hex
    raw_tx = proxy.getrawtransaction(txid)

    # Decode the transaction hex into a JSON object
    decoded_tx = proxy.decoderawtransaction(raw_tx)

    # Retrieve each of the outputs from the transaction
    for output in decoded_tx['vout']:
        print(output['scriptPubKey']['address'], output['value'])

if __name__ == "__main__":
    main()
