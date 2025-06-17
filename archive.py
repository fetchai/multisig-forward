#!/usr/bin/env python3

import re
import os
import subprocess


def _parse_sequence_number(value):
    return int(value[:3])


def main():
    results = os.listdir('.')

    # filter the results into things that look like transactions
    filtered = filter(
        lambda p: re.match(r'^\d{3}\..+\.json$', p) is not None,
        results,
    )

    # build the transaction sets
    transaction_sets = {}
    for item in sorted(filtered):
        seq = _parse_sequence_number(item)

        # update the list of transaction items
        existing = transaction_sets.get(seq, [])
        existing.append(item)
        transaction_sets[seq] = existing

    for seq, items in transaction_sets.items():
        contents_count = 0
        tx_count = 0
        sig_count = 0

        for item in items:
            if re.search(r'sig\.json$', item):
                sig_count += 1
            elif re.search(r'contents\.json$', item):
                contents_count += 1
            elif re.search(r'tx\.json$', item):
                tx_count += 1
            else:
                print('Unknown file type', item)
                assert False

        # sanity check the counts
        assert contents_count == 1
        assert sig_count >= 2
        assert tx_count == 1

        # add all the items to the git staging area
        for item in items:
            cmd = ['git', 'mv', item, 'archive/']
            subprocess.check_call(cmd)

        # commit
        cmd = ['git', 'commit', '-m', f'[{seq:03}] Archive TX']
        subprocess.check_call(cmd)


if __name__ == '__main__':
    main()
