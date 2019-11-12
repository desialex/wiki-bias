#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import argparse


def to_pickle(data, output_pickle_path):
    if output_pickle_path.endswith('.pickle'):
        with open(output_pickle_path, 'wb') as f:
            pickle.dump(data, f)
    else:
        with open(output_pickle_path + '.pickle', 'wb') as f:
            pickle.dump(data, f)


def unpickle(input_pickle_path):
    if input_pickle_path.endswith('.pickle'):
        with open(input_pickle_path, 'rb') as file:
            data = pickle.load(file)
            return data
    else:
        with open(input_pickle_path + '.pickle', 'rb') as file:
            data = pickle.load(file)
            return data


def to_text_file(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(data))


def check_lang(string):
    if len(string) != 2:
        msg = "Language code must be 2 characters long"
        raise argparse.ArgumentTypeError(msg)
    return string


def check_date(string):
    if len(string) != 8:
        msg = "Date must be in the following format: YYYYMMDD"
        raise argparse.ArgumentTypeError(msg)
    return string
