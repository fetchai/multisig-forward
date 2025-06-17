#!/usr/bin/env python3

import subprocess
import argparse
import json
import os
import time


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='+', help='The transaction file(s) to broadcast to the network')
    return parser.parse_args()


def _parse_sequence_number(value):
    return int(value[:3])


def main():
    args = parse_commandline()

    cmd = [
        'fetchd',
        'config',
    ]
    resp = json.loads(subprocess.check_output(cmd).decode())

    assert resp.get('chain-id') == 'fetchhub-4'
    assert resp.get('node') == 'https://rpc-fetchhub.fetch.ai:443'
    assert resp.get('broadcast-mode') == 'sync'


    for tx_file in sorted(args.filename):
        seq_num = _parse_sequence_number(tx_file)

        cmd = [
            'fetchd',
            'tx',
            'broadcast',
            '--output', 'json',
            tx_file
        ]
        resp = json.loads(subprocess.check_output(cmd).decode())
        print(resp)

        code = int(resp['code'])
        if code != 0:
            assert False, "Unsuccessfully broadcast the transaction, check tx signatures"

        tx_hash = str(resp['txhash'])

        cmd = [
            'fetchd',
            'query',
            'tx',
            str(tx_hash),
            '--output', 'json',
        ]

        while True:
            try:
                with open(os.devnull, 'w') as null_file:
                    output = json.loads(subprocess.check_output(cmd, stderr=null_file).decode())

                code = int(output['code'])

                print(f'Link: https://mintscan.io/fetchai/tx/{tx_hash}')
                print(f'      https://companion.fetch.ai/fetchhub-4/transactions/{tx_hash}')

                if code == 0:
                    print('Transaction Successful')
                    status = 'Final'
                else:
                    print('Transaction UNSUCCESSFUL')
                    status = 'FAILED'

                cmd = ['git', 'add', tx_file]
                subprocess.check_call(cmd)

                cmd = ['git', 'commit', '-m', f'[{seq_num:03}] {status} TX: {tx_hash}']
                subprocess.check_call(cmd)

                break

            except subprocess.CalledProcessError:
                print('Transaction lookup failed')

            print('Waiting....')
            time.sleep(4)



if __name__ == '__main__':
    main()
