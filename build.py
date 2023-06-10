#!/usr/bin/env python3

"""
    Uses the Chain class from chain.py to build a Markov chain
    For help, run python3 build.py -h
"""

import argparse
from os import path
from chain import Chain

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--infile', type=str, help='A file of text on which to build the chain', required=True)
    argparser.add_argument('-o', '--outfile', type=str, help='Name of the chain file (default=chain.json)', default='chain.json', required=False)
    argparser.add_argument('-r', '--resolution', type=int, help='Phrase resolution (default=2)', default=2, required=False)
    args = argparser.parse_args()

    chain = Chain(resolution=args.resolution)
    if path.isfile(args.outfile):
        print('Using old chain file %s...' % args.outfile)
        chain_file = open(args.outfile, 'r')
        chain = Chain.from_json(chain_file.read(), resolution=args.resolution)
        chain_file.close()
    else:
        print('Creating a new chain')

    input_corpus = open(args.infile, 'r')
    for line in input_corpus:
        chain.read_line(line)
    input_corpus.close()
    
    output_file = open(args.outfile, 'w')
    output_file.write(chain.to_json())
    output_file.close()
    print('Wrote chain data to %s' % args.outfile)