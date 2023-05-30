import ast
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from pathlib import Path
import pandas as pd

current_dir = Path(__file__).parent

# parameters
aligned_data_file_name = "eflomal/aligned_data.csv"
pos_visual = "PRON"


def get_pos_w_text(un_aligned_data):
    pos_freq_w_text = defaultdict(dict)
    for sent_value in un_aligned_data.values():
        for _index, _text, _pos, _left, _right in sent_value:
            pos_freq_w_text[_pos][_text] = pos_freq_w_text[_pos].get(_text, 0)+1
    return pos_freq_w_text


def get_pos_frequency(unaligned_words):
    pos_freq = defaultdict(int)
    for sent_value in unaligned_words.values():
        for _, _, _pos, _, _ in sent_value:
            pos_freq[_pos] += 1
    return pos_freq


def get_unaligned_as_data(unaligned_words):
    unaligned_data = defaultdict(list)
    for i, data in enumerate(unaligned_words):
        unaligned_data[i].extend(ast.literal_eval(data))
    return unaligned_data


def visualize_w_pos(pos_text_freq, pos_tag, top_n=10):
    plt.bar(pos_text_freq.keys(), pos_text_freq.values())
    plt.xlabel('Words')
    plt.ylabel('Frequencies')
    plt.title(f'Frequencies of Words with {pos_tag}')
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(current_dir, aligned_data_file_name),
                     names=['source_lang', 'target_lang', 'aligned_words', 'unaligned_words'])
    unaligned_data_sent = get_unaligned_as_data(df.unaligned_words)
    pos_frequency = get_pos_frequency(unaligned_data_sent)
    pos_fre_w_text = get_pos_w_text(unaligned_data_sent)
    visualize_w_pos(pos_fre_w_text.get(pos_visual), pos_visual)
