import os.path
from pathlib import Path

import pandas as pd


current_path = Path(__file__).parent.parent

# parameters
filepath = "euro_parl_data/parallels_de_original.tsv"
output_path = "fast_align/to_align"
source_lang = "de"
dest_lang = "en"


def create_source_target_files(parallel_dataset):
    _file = f'source_{source_lang}_{dest_lang}'
    with open(os.path.join(output_path, _file), 'w') as input_file:
        # Loop over your data
        for s_data, d_data in parallel_dataset:
            input_file.write(s_data + ' ||| ' + d_data +'\n')


if __name__ == "__main__":
    dataset = pd.read_table(filepath, sep="\t")
    filtered_data = dataset[(dataset['native_speaker'] == 1) & (dataset["src"] == source_lang) & (dataset[dest_lang].notnull())]
    parallel_data = list(zip(filtered_data[source_lang], filtered_data[dest_lang]))
    create_source_target_files(parallel_dataset=parallel_data)




