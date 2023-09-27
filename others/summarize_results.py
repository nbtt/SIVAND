import os
import json
import pandas as pd
from typing import List
from datetime import datetime

from get_tokens_java import get_tokens, get_main_tokens

# data directory
data_dir = "/Users/lap13494/workspace/ppl-extra-final/SIVAND/models/dd-code2seq/code2seq/dd_data"
# maximum number of files for processing
MAX_NO_FILES = 1000
# output file
out_path = '/Users/lap13494/workspace/ppl-extra-final/SIVAND/data/summary_result/mn_c2s/dd_mn_token_correct_results.csv'
# list of columns in output file
columns = ('filename', 'model', 'task', 'filter_type', 'initial_score', 'final_score', 'initial_loss', 'final_loss', 'dd_pass', 'dd_time', 'initial_program', 'final_program', 'initial_tokens', 'final_tokens', 'len_initial_tokens', 'len_final_tokens', 'len_minimal_tokens', 'len_initial_chars', 'len_final_chars', 'len_minimal_chars', 'per_removed_chars', 'per_removed_tokens', 'attn_nodes', 'final_nodes', 'common_nodes', 'len_attn_nodes', 'len_final_nodes', 'len_common_nodes', 'per_common_tokens', 'ground_truth')
model_name = 'code2seq'
task_name = 'METHOD_NAME'
filter_type = 'token_correct'
time_format = "%Y-%m-%d %H:%M:%S.%f"

def summarize_data_by_traces(
        data_traces: List[dict],
        data_filename: str,
        model_name: str,
        task_name: str,
        filter_type: str,
        time_format: str,
        ):
    
    inital_program = data_traces[0]['code']
    final_program = data_traces[-1]['code']
    inital_tokens = get_tokens(inital_program)
    final_tokens = get_tokens(final_program)

    return pd.Series({
        'filename': data_filename,
        'model': model_name,
        'task': task_name,
        'filter_type': filter_type,
        'initial_score': data_traces[0]['score'],
        'final_score': data_traces[-1]['score'],
        'initial_loss': data_traces[0]['loss'],
        'final_loss': data_traces[-1]['loss'],
        'dd_pass': "{{'n_total': {}, 'n_valid': {}, 'n_correct': {}}}".format(*data_traces[-1]['n_pass']),
        'dd_time': (datetime.strptime(data_traces[-1]["time"], time_format) - datetime.strptime(data_traces[0]["time"], time_format)).total_seconds(),
        'initial_program': inital_program,
        'final_program': final_program,
        'initial_tokens': str(inital_tokens),
        'final_tokens': str(final_tokens),
        'len_initial_tokens': len(inital_tokens),
        'len_final_tokens': len(final_tokens),
        'len_initial_chars': len(inital_program),
        'len_final_chars': len(final_program),
        'per_removed_tokens': (1 - len(get_main_tokens(final_program)) / len(get_main_tokens(inital_program))) * 100,
        'ground_truth': True,
    })

if __name__ == "__main__":
    # get data list
    data_filenames = os.listdir(data_dir)
    # sort the list by iteration
    data_filenames.sort(key=lambda data_file: int(data_file.split('_')[0][1:]))
    
    data_output = pd.DataFrame(columns=columns)

    for i, data_filename in enumerate(data_filenames):
        if i >= MAX_NO_FILES:
            break

        data_path = os.path.join(data_dir, data_filename)
        with open(data_path, "r") as reader:
            data_lines = reader.readlines()[7:-5]
        data_traces = list(map(json.loads, data_lines))
        if len(data_traces) == 0:
            continue

        data_item = summarize_data_by_traces(
            data_traces,
            data_filename,
            model_name,
            task_name,
            filter_type,
            time_format)
        
        data_output = pd.concat([data_output, data_item.to_frame(name=i).T])

    data_output.to_csv(out_path, sep=',', index=False)