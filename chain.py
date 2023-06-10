import json
import random
from typing import Dict, List, Set

# Used to ensure we serialize the endings property (a set) correctly
# when writing the chain JSON to the disk
class ChainEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return o.__dict__

class Chain:
    inputs: Dict
    word_stack: List[str]
    endings: Set[str]
    resolution: int
    version: int

    # Blanks out the token stack
    def reset_stack(self):
        self.word_stack = ['\n' for i in range(0, self.resolution)]

    # Adds a new token to the set of possible paths from the given key.
    def push_input(self, key='', token=''):
        if key == '\n \n':
            return
        if not key in self.inputs:
            self.inputs[key] = []
        
        # could use a set to elim this check but the efficiency of choosing randomly from a set is atrocious
        if not token in self.inputs[key]:
            self.inputs[key].append(token)

    # Consumes a line of text and stores its words in the input dict
    def read_line(self, line=''):
        sanitized_line = line.strip()
        if len(sanitized_line) == 0:
            self.reset_stack()
            return

        tokens = sanitized_line.split()
        for token in tokens:
            if token == '\n':
                pass
            # TODO: allow for some kind of easy-to-implement sanitization overrides if the need ever arises
            sanitized_token = token.lower().strip('"').strip('\u201c').strip('\u201d').replace('\u2014', '-').strip(',')

            b_end = False
            if len(token) > 1 and token[-1] in self.endings:
                sanitized_token = sanitized_token[:-1]
                b_end = True
            
            input_index = self.token_separator.join(self.word_stack)
            self.push_input(input_index, sanitized_token)
            self.word_stack.pop(0)
            self.word_stack.append(sanitized_token)

            # If the sentence ended after the current token, we want to make sure we
            # mark this as a possible path by using '\n' to represent the end of a sentence.
            if b_end:
                self.push_input(self.token_separator.join(self.word_stack), '\n')
                self.reset_stack()

    def __init__(self, resolution=2, token_separator=' '):
        self.version = 1
        self.resolution = resolution
        self.token_separator = token_separator
        self.inputs = dict()
        self.endings = ['.', '?', '!', ':', ';']
        self.reset_stack()
    
    # 
    def set_endings(self, endings: str):
        self.endings.clear()
        for ending in endings:
            self.endings.add(ending)

    # Generates a phrase using the data in the chain. token_count represents an upper limit,
    # and generated phrases are likely to never actually reach that length.
    def generate(self, token_count=64):
        keys = list(self.inputs.keys())
        key = random.choice(keys)
        generated_tokens = key.split(self.token_separator)

        # Generate up to token_count tokens and then lob off the last incomplete sentence
        while len(generated_tokens) < token_count:
            shall_rekey = False
            chosen_next = random.choice(self.inputs[key])
            if len(self.inputs[key]) == 1 and self.inputs[key][0] == '\n':
                shall_rekey = True
            elif chosen_next == '\n':
                shall_rekey = True
            else:
                generated_tokens.append(chosen_next)
                split_key = key.split(self.token_separator)
                if len(split_key) == self.resolution:
                    split_key.pop(0)
                split_key.append(chosen_next)
                key = self.token_separator.join(split_key)
                if not key in self.inputs:
                    shall_rekey = True

            # We need a new key, because the old key either didn't exist in the input dict,
            # or we've hit the end of a sentence after choosing a '\n' from the input dict.
            if shall_rekey:
                generated_tokens.append('%s.' % generated_tokens.pop())
                key = random.choice(keys)
                for token_in_key in key.split(self.token_separator):
                    generated_tokens.append(token_in_key)
                    
        generated_sentences = self.token_separator.join(generated_tokens)
        return '%s.' % generated_sentences[:generated_sentences.rfind('.')]
    
    def to_json(self):
        return json.dumps(self, cls=ChainEncoder, sort_keys=True, indent=2)
    
    @staticmethod
    def from_json(json_str, resolution=2):
        chain = Chain(resolution=resolution)
        loaded_data = json.loads(json_str)
        if resolution == 0:
            chain.resolution = loaded_data['resolution']
        
        if chain.version != loaded_data['version']:
            print('Error: Version mismatch (this script supports V%d, existing output chain is V%d)' % (chain.version, loaded_data['version']))
            exit()
        if chain.resolution != loaded_data['resolution']:
            print('Error: Existing chain\'s resolution does not match wanted resolution (Wanted %d, got %d)' % (chain.resolution, loaded_data['resolution']))
            exit()
        if chain.resolution != loaded_data['resolution']:
            print('Error: Existing chain\'s token separator does not match wanted separator (Wanted \'%s\', got \'%s\')' % (chain.token_separator, loaded_data['token_separator']))
            exit()

        chain.inputs = loaded_data['inputs']
        chain.word_stack = loaded_data['word_stack']
        chain.endings = set(loaded_data['endings'])
        return chain
