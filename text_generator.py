#!/usr/bin/env python3
from nltk.tokenize import WhitespaceTokenizer
from nltk import trigrams
from collections import defaultdict, Counter
import random
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Enter the filename or path to file')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    file_content = f.read()
tk = WhitespaceTokenizer()
tokens = tk.tokenize(file_content)


def generate_start(trigram_dict):
    starts = [pair for pair in trigram_dict.keys() if pair[0][0].isupper() and pair[0][-1] not in "!?."]
    return random.choice(starts)


def fetch(token_list):
    tri_count_dict = tri_count([*trigrams(token_list)])
    paragraph = []
    for _ in range(10):
        sentence = []
        head = generate_start(tri_count_dict)  # generate 2 word start for each of the 10 sentences
        sentence.append(' '.join(head))
        while True:
            tails_list = [*tri_count_dict[head].keys()]
            weight_list = [*tri_count_dict[head].values()]
            next_word = random.choices(tails_list, weight_list)
            sentence.append(*next_word)
            head = (head[1], *next_word)
            if len(sentence) > 4 and sentence[-1][-1] in '.?!':  # sentence is at least 5 words before any punctuation
                break
            elif sentence[-1][-1] in '.?!':  # restart loop if punctuation occurs too soon
                sentence = []
                head = generate_start(tri_count_dict)
                sentence.append(' '.join(head))
                continue
        paragraph.append(sentence)
    for s in paragraph:
        print(' '.join(s))


def tri_count(tri):
    head_tail_dict = defaultdict(list)
    for head1, head2, tail in tri:
        head_tail_dict[head1, head2].append(tail)  # head tuple as keys, list of all tails as values
    for key, value in head_tail_dict.items():  # turns value list into dict of counts for all the tails for each head
        head_tail_dict[key] = Counter(value)
    return head_tail_dict

if __name__ == '__main__': fetch(tokens)


