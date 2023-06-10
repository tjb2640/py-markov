# py-markov
Simple Markov chain logic for creating phrases in Python

Demonstrates a basic implementation of a funny-phrase Markov chain.
It keeps track of which words might come next as part of a sequence, but
does not keep track of the frequency at which they occur, which leads
to an extra layer of unpredictability and funnier output.

## Usage (CLI)
`build.py` builds a chain using an input corpus.
You can call this file multiple times using the same output chain
to add more data to the chain later:

```bash
# build.py:
#   -i INFILE: input corpus. the chain learns word ordering from the contents of this file
#   -o OUTFILE: output/where to save the chain data
#   -r RESOLUTION: the size `n` in word count used to resolve next words in generated phrases

# generate.py:
#   -i INFILE: the .json file containing a chain's data, generated as the outfile from build.py
#   -o OUTFILE: output/where to save the generated phrases. Use stdout to print to console
#   -c COUNT: number of phrases to generate
#   -l LENGTH: maximum length of generated phrases
```

```bash
# Examples
# example/example-input.txt contains public domain War of the Worlds copy from Project Gutenberg.

# Generate a chain from an input corpus (-i FILENAME)
python3 build.py -i example/example-input.txt -o chain.json -r 2

# Use the built chain in chain.json to generate phrases which will likely make little sense
python3 generate.py -i chain.json -o stdout -c 5 -l 32 
```

Example result:

```txt
to remain the darker after their dispersal. the papers except a little crowd towards woking village and send.

amazing subtlety-their mathematical learning is evidently far in excess of oxygen upon the planet as flaming gases rushed out of space hour by hour and day by day nearer and nearer.

on a long pole. started on its apparition and blindingly violet by contrast danced out the first touch of day.

came upon him in his narrative and i could go about their little affairs serene in their leisure but it certainly did not remember hearing any birds that morning there was fir.

several officers from the sun was setting. some invisible jet impinged upon them. it might be automatic. brightened their intellects enlarged their powers and hardened their hearts.
```
