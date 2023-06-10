#!/usr/bin/env python3

import argparse
from os import path
from chain import Chain

"""
    Takes a chain created with build.py to generate phrases
    For help, run python3 generate.py -h
"""

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--infile', type=str, help='A .json file containing chain data', required=True)
    argparser.add_argument('-o', '--outfile', type=str, help='Name of the file to write generated phrases to (default=stdout)', default='stdout', required=False)
    argparser.add_argument('-c', '--count', type=int, help='Number of phrases to generate (default=1)', default=1, required=False)
    argparser.add_argument('-l', '--length', type=int, help='Max phrase length (default=64)', default=64, required=False)
    args = argparser.parse_args()

    if not path.isfile(args.infile):
        print('Error: input chain file doesn\'t exist (%s)' % args.infile)
        exit()

    chain_file = open(args.infile, 'r')
    chain = Chain.from_json(chain_file.read(), resolution=0)
    chain_file.close()

    # We'll write these to the selected outfile after generation
    phrases = []
    for i in range(0, args.count):
        phrases.append(chain.generate(token_count=args.length))

    if args.outfile == 'stdout':
        print('\n\n'.join(phrases))
        exit()

    out_file = open(args.outfile, 'w')
    out_file.write('\n\n'.join(phrases))
    out_file.close()
    print('Wrote %d phrases to %s' % (args.count, args.outfile))