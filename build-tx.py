#!/usr/bin/env python3

import argparse
import glob
import os
import subprocess


FOUNDATION_ADDRESS = 'fetch1z75gmchl4nx5hacnxj2ck2hg9czwa6ahy2a30z'
FOUNDATION_ACCOUNT_NUM = 363056
CHAIN_ID = 'fetchhub-4'


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('local_multi_sig_name')
    parser.add_argument('transaction_filepaths', metavar='FILE', nargs='+')
    return parser.parse_args()


def _parse_sequence_number(value):
    return int(value[:3])


def _find_related_signatures(contents_path):
    parts = contents_path.split('.')
    glob_pattern = '.'.join(parts[:2] + ['*', 'sig', 'json'])
    return list(glob.glob(glob_pattern))


def main():
    # fetchcli tx multisign 005.deposit_30M.contents.json fetchai-multi 005.deposit_30M.sig.fetchai-ed.json 005.deposit_30M.sig.pb_mainnet_key.json --chain-id fetchhub-1 -a 15 -s 5 --offline > 005.deposit_30M.tx.json
    args = parse_commandline()

    print(args.transaction_filepaths)

    for contents_path in args.transaction_filepaths:
        seq_num = _parse_sequence_number(contents_path)
        sigs = _find_related_signatures(contents_path)
        print(sigs)

        cmd = [
            'fetchd',
            'tx',
            'multisign',
            contents_path,
            args.local_multi_sig_name,
        ] + sigs + [
            '--chain-id', CHAIN_ID,
            '-a', str(FOUNDATION_ACCOUNT_NUM),
            '-s', str(seq_num),
            '--offline',
        ]

        print("cmd:", " ".join(cmd))

        # form the output
        with open(os.devnull, 'w') as null_file:
            contents = subprocess.check_output(cmd, stderr=null_file).decode()

        # write output
        output_filename = '.'.join(contents_path.split('.')[:-2] + ['tx', 'json'])
        print("output_filename", output_filename)
        with open(output_filename, 'w') as signature_file:
            signature_file.write(contents)


if __name__ == '__main__':
    main()
