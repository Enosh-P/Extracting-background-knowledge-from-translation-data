import csv
import os.path
from collections import defaultdict
from pathlib import Path

import spacy
import re

current_dir = Path(__file__).parent


# parameters
aligned_file_path = 'eflomal/aligned/de_en.ealign'
parallel_text_file = 'eflomal/to_align/source_de_en'
origin_lang = "de"
target_lang = "en"
target_filename = "eflomal/unaligned_data.csv"

if target_lang == "de":
    nlp = spacy.load("de_dep_news_trf")
elif target_lang == "de":
    nlp = spacy.load("fr_dep_news_trf")
else:
    nlp = spacy.load("en_core_web_trf")


def filter_unaligned(parallel_text, alignment_code, target_lan="en"):
    with open(alignment_code, 'r') as aligned_file, open(parallel_text, 'r') as parallel_file:
        aligned_content = aligned_file.read()
        parallel_sent = parallel_file.read()

    post_align_lines = aligned_content.split('\n')
    pre_align_lines = parallel_sent.split('\n')
    un_aligned_text = defaultdict(list)
    for i, (post_a_line, pre_a_line) in enumerate(zip(post_align_lines, pre_align_lines)):
        if not pre_a_line or not post_a_line:
            continue
        regex_matches = re.findall(r'(?<!\d)([1-9]\d*)\D0\D?', post_a_line)  # number-0
        original_sen, target_sen = pre_a_line.split(' ||| ')

        if not regex_matches:
            continue
        doc = nlp(target_sen)
        for n in regex_matches:
            token = doc[int(n)-1]
            pos_tag = token.pos_
            if pos_tag == 'PUNCT':
                token = doc[int(n)]
                pos_tag = token.pos_
            entity_type = token.ent_type_
            un_aligned_text[(original_sen, target_sen)].append((token.text, pos_tag, entity_type))
    return un_aligned_text


def convert_to_csv(un_aligned_data):
    data = []
    for (ori_sen, tar_sen), vals in un_aligned_data.items():
        for text, pos, ent in vals:
            data.append((ori_sen, tar_sen, text, pos, ent))
    with open(os.path.join(current_dir, target_filename), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


if __name__ == "__main__":
    un_aligned = filter_unaligned(
        os.path.join(current_dir, parallel_text_file), os.path.join(current_dir, aligned_file_path), target_lang
    )
    convert_to_csv(un_aligned)
