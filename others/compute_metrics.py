import pandas as pd
import pprint
import json

summary_path = "/Users/lap13494/workspace/ppl-extra-final/SIVAND/data/summary_result/mn_c2s/dd_mn_token_correct_results.csv"

def compute_summary_metrics(summary_data: pd.DataFrame):
    num_samples = summary_data.shape[0]
    return {
        'Task': summary_data.loc[0]['task'],
        'Model': summary_data.loc[0]['model'],
        '# Sample': num_samples,
        '# Tokens': {
            'Min': summary_data['len_final_tokens'].min(),
            'Avg': summary_data['len_final_tokens'].sum() / num_samples,
            'Max': summary_data['len_final_tokens'].max(),
        },
        'Reductions (%)': {
            'Min': summary_data['per_removed_tokens'].min(),
            'Avg': summary_data['per_removed_tokens'].sum() / num_samples,
            'Max': summary_data['per_removed_tokens'].max(),
        },
        '# DD Pass (Average)': {
            "Total": summary_data['dd_pass'].map(lambda summary_item: json.loads(summary_item.replace("\'", "\""))['n_total']).sum() / num_samples,
            "Valid": summary_data['dd_pass'].map(lambda summary_item: json.loads(summary_item.replace("\'", "\""))['n_valid']).sum() / num_samples,
            "Correct": summary_data['dd_pass'].map(lambda summary_item: json.loads(summary_item.replace("\'", "\""))['n_correct']).sum() / num_samples,
        },
        'Time (second)': {
            "Min": summary_data['dd_time'].min(),
            "Avg": summary_data['dd_time'].sum() / num_samples,
            "Max": summary_data['dd_time'].max(),
        }
    }

if __name__ == "__main__":
    summary_data = pd.read_csv(summary_path)
    print(summary_data)
    summary = compute_summary_metrics(summary_data)
    pprint.pprint(summary)