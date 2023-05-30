import csv
import os.path
from pathlib import Path

import spacy

current_dir = Path(__file__).parent


# parameters
aligned_file_path = 'eflomal/aligned/de_en.ealign'
parallel_text_file = 'eflomal/to_align/source_de_en'
origin_lang = "de"
target_lang = "en"
target_filename = "eflomal/aligned_data.csv"

if target_lang == "de":
    nlp = spacy.load("de_dep_news_trf")
elif target_lang == "de":
    nlp = spacy.load("fr_dep_news_trf")
elif target_lang == "es":
    nlp = spacy.load("es_dep_news_trf")
elif target_lang == "pl":
    nlp = spacy.load("pl_core_news_lg")
else:
    nlp = spacy.load("en_core_web_trf")


def change_aligned_data(parallel_text, alignment_code):
    with open(alignment_code, 'r') as aligned_file, open(parallel_text, 'r') as parallel_file:
        aligned_content = aligned_file.read()
        parallel_sent = parallel_file.read()

    post_align_lines = aligned_content.split('\n')
    pre_align_lines = parallel_sent.split('\n')
    aligned_data = {}
    for i, (post_a_line, pre_a_line) in enumerate(zip(post_align_lines, pre_align_lines)):
        if not pre_a_line or not post_a_line:
            continue
        source_sen, target_sen = pre_a_line.split(' ||| ')
        alignments = post_a_line.split()
        aligned_words = {}
        unaligned_words = {}
        target_tokens = target_sen.split()
        source_tokens = source_sen.split()
        for alignment in alignments:
            source_index, target_index = map(int, alignment.split('-'))
            source_word = source_tokens[source_index]
            target_word = target_tokens[target_index]
            aligned_words[target_index] = (source_word, target_word)
        for j in range(len(target_tokens)):
            if j not in aligned_words:
                unaligned_words[j] = target_tokens[j]

        doc = nlp(target_sen)
        complete_pos = [(w.text, w.pos_) for w in doc if w.pos_ != 'PUNCT']
        unaligned_pos = []
        left = ''
        right = ''
        for j, (w, p) in enumerate(complete_pos):
            if j in unaligned_words:
                if p == 'PROPN':
                    if j > 0:
                        left = complete_pos[j-1]
                    if j < len(complete_pos)-1:
                        right = complete_pos[j+1]
                unaligned_pos.append((j, w, p, left, right))

        aligned_data[(source_sen, target_sen)] = (aligned_words, unaligned_pos)

    return aligned_data

def convert_to_csv(aligned_data_to_csv):
    data = []
    for (ori_sen, tar_sen), (ali_words, unalign_pos) in aligned_data_to_csv.items():
        data.append((ori_sen, tar_sen, ali_words.items(), unalign_pos))
    with open(os.path.join(current_dir, target_filename), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


if __name__ == "__main__":
    aligned_complete_data = change_aligned_data(
        os.path.join(current_dir, parallel_text_file), os.path.join(current_dir, aligned_file_path)
    )
    convert_to_csv(aligned_complete_data)
