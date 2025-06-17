#!/usr/bin/env python3

import argparse
import subprocess
import os


FOUNDATION_ADDRESS = 'fetch1z75gmchl4nx5hacnxj2ck2hg9czwa6ahy2a30z'
FOUNDATION_ACCOUNT_NUM = 0
CHAIN_ID = 'fetchhub-4'


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('local_key_name')
    parser.add_argument('transaction_filepaths', metavar='FILE', nargs='+')
    parser.add_argument('-c', '--commit', action='store_true', help='Flag to enable automatic commit')
    return parser.parse_args()


def _parse_sequence_number(value):
    return int(value[:3])


def main():
    args = parse_commandline()
    for contents_path in args.transaction_filepaths:
        seq_num = _parse_sequence_number(contents_path)

        # build up the command
        cmd = [
            'fetchd',
            'tx',
            'sign',
            contents_path,
            '--multisig', FOUNDATION_ADDRESS,
            '--from', args.local_key_name,
            '--chain-id', CHAIN_ID,
            '-a', str(FOUNDATION_ACCOUNT_NUM),
            '-s', str(seq_num),
            '--offline',
        ]

        print(' '.join(cmd))
        with open(os.devnull, 'w') as null_file:
            contents = subprocess.check_output(cmd, stderr=null_file).decode()

        # the command will generate a whole load of legacy warnings we need to junk
        generated_signature = None
        for line in contents.splitlines():
            if line.strip().startswith('{'):
                generated_signature = line.strip()
                break

        output_filename = '.'.join(contents_path.split('.')[:-2] + [args.local_key_name, 'sig', 'json'])
        with open(output_filename, 'w') as signature_file:
            signature_file.write(generated_signature)

        if args.commit:
            cmd = [
                'git',
                'add',
                output_filename
            ]
            subprocess.check_call(cmd)

            cmd = [
                'git',
                'commit',
                '-m', f'[v4 {seq_num:03}] Signed by {args.local_key_name}'
            ]
            subprocess.check_call(cmd)


if __name__ == '__main__':
    main()
