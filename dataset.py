import sys
import random
from utils import unpickle, to_text_file
from typing import List, Text, Iterator, Dict


def label(sentences: List, label: str, prefix: str, separator: str) -> List:
    return [prefix + label + separator + s for s in sentences]


def split_dataset(adds: List, rems: List):
    dataset = adds + rems
    dataset.sort()
    random.seed(230)
    random.shuffle(dataset)

    split_1 = int(0.8 * len(dataset))
    split_2 = int(0.9 * len(dataset))
    train = dataset[:split_1]
    dev = dataset[split_1:split_2]
    test = dataset[split_2:]
    to_text_file(train, output_dir + language.upper()
                 + '-' + classifier + '-train.txt')
    to_text_file(dev, output_dir + language.upper()
                 + '-' + classifier + '-dev.txt')
    to_text_file(test, output_dir + language.upper()
                 + '-' + classifier + '-test.txt')


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    language = sys.argv[3]
    classifier = sys.argv[4]
    data = unpickle(input_file)
    if classifier == "ft":
        add = label(data['add'], label='add',
                    prefix='__label__', separator='\t')
        rem = label(data['rem'], label='rem',
                    prefix='__label__', separator='\t')
    else:
        add = label(data['add'], label='add', prefix='', separator='\t')
        rem = label(data['rem'], label='rem', prefix='', separator='\t')
    split_dataset(add, rem)
    print('DONE')
