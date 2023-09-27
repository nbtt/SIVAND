import pickle
from argparse import ArgumentParser

import numpy as np

import common

'''
This script preprocesses the data from MethodPaths. It truncates methods with too many contexts,
and pads methods with less paths with spaces.
'''


def process_file(file_path, data_file_role, dataset_name, max_contexts, max_data_contexts):
    sum_total = 0
    sum_sampled = 0
    total = 0
    max_unfiltered = 0
    max_contexts_to_sample = max_data_contexts if data_file_role == 'train' else max_contexts
    output_path = '{}.{}.c2s'.format(dataset_name, data_file_role)
    with open(output_path, 'w') as outfile:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.rstrip('\n').split(' ')
                target_name = parts[0]
                contexts = parts[1:]

                if len(contexts) > max_unfiltered:
                    max_unfiltered = len(contexts)

                sum_total += len(contexts)
                if len(contexts) > max_contexts_to_sample:
                    contexts = np.random.choice(contexts, max_contexts_to_sample, replace=False)

                sum_sampled += len(contexts)

                csv_padding = " " * (max_data_contexts - len(contexts))
                total += 1
                outfile.write(target_name + ' ' + " ".join(contexts) + csv_padding + '\n')

    print('File: ' + file_path)
    print('Average total contexts: ' + str(float(sum_total) / total))
    print('Average final (after sampling) contexts: ' + str(float(sum_sampled) / total))
    print('Total examples: ' + str(total))
    print('Max number of contexts per word: ' + str(max_unfiltered))
    return total


def context_full_found(context_parts, word_to_count, path_to_count):
    return context_parts[0] in word_to_count \
           and context_parts[1] in path_to_count and context_parts[2] in word_to_count


def context_partial_found(context_parts, word_to_count, path_to_count):
    return context_parts[0] in word_to_count \
           or context_parts[1] in path_to_count or context_parts[2] in word_to_count


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ted", "--test_data", dest="test_data_path",
                        help="path to test data file", required=True)
    parser.add_argument("-mc", "--max_contexts", dest="max_contexts", default=200,
                        help="number of max contexts to keep in test+validation", required=False)
    parser.add_argument("-mdc", "--max_data_contexts", dest="max_data_contexts", default=1000,
                        help="number of max contexts to keep in the dataset", required=False)
    parser.add_argument("-svs", "--subtoken_vocab_size", dest="subtoken_vocab_size", default=186277,
                        help="Max number of source subtokens to keep in the vocabulary", required=False)
    parser.add_argument("-tvs", "--target_vocab_size", dest="target_vocab_size", default=26347,
                        help="Max number of target words to keep in the vocabulary", required=False)
    parser.add_argument("-o", "--output_name", dest="output_name",
                        help="output name - the base name for the created dataset", required=True, default='data')
    args = parser.parse_args()

    test_data_path = args.test_data_path

    num_training_examples = 0
    for data_file_path, data_role in zip([test_data_path], ['test']):
        num_examples = process_file(file_path=data_file_path, data_file_role=data_role, dataset_name=args.output_name,
                                    max_contexts=int(args.max_contexts), max_data_contexts=int(args.max_data_contexts))
        if data_role == 'train':
            num_training_examples = num_examples
