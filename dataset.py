import sys
import random
import getopt
from utils import unpickle, to_text_file
from typing import List, Text, Iterator, Dict


def label(sentences: List, label: str, prefix: str, separator: str) -> List:
    return [prefix + label + separator + s for s in sentences]


def split_dataset(adds: List, rems: List, lang):
    dataset = adds + rems
    dataset.sort()
    random.seed(230)
    random.shuffle(dataset)

    split_1 = int(0.8 * len(dataset))
    split_2 = int(0.9 * len(dataset))
    train = dataset[:split_1]
    dev = dataset[split_1:split_2]
    test = dataset[split_2:]
    to_text_file(train, lang.upper() + '-train.txt')
    to_text_file(dev, lang.upper() + '-dev.txt')
    to_text_file(test, lang.upper() + '-test.txt')


def main(argv):
    inputfile = None
    lang = None
    prefix = ""
    cmd_line = 'dataset.py -i <inputfile> -l <lang> (-p <prefix>)'

    try:
        opts, args = getopt.getopt(argv, "l:i:p:", ["ifile=", "lang=", "prefix="])
    except getopt.GetoptError:
        print(cmd_line)
        print(argv)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(cmd_line)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            # text file containing revision pairs
            inputfile = arg
        elif opt in ("-l", "--lang"):
            # two-letter ISO code for the language
            if len(arg) == 2:
                lang = arg
            else:
                print("Define language by its two-letter ISO code")
                sys.exit(2)
        elif opt in ("-p", "--prefix"):
            # classifier-specific label prefix, e.g. __label__
            prefix = arg

    # Sanity check if all mandatory parameters are there
    if not lang or not inputfile:
        print("Missing parameter")
        print(cmd_line)
        sys.exit(2)

    data = unpickle(inputfile)
    add = label(data['add'], label='neutral', prefix=prefix, separator='\t')
    rem = label(data['rem'], label='biased', prefix=prefix, separator='\t')
    split_dataset(add, rem, lang)


if __name__ == '__main__':
    main(sys.argv[1:])
