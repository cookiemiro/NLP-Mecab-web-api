from collections import Counter 
import pickle
from keyword_extraction import get_pos_list

in_corpus = 'english.corpus'
out_counts = 'eng.adjective.counts'
tag = 'eng-adjective' # noun/va/adjective/adjective_and_noun
num_list_to_count = 50000

def read_corpus(corpus):
    text_list = []
    with open(corpus, 'r') as fr:
        lines = fr.readlines()
        for l in lines:
            text_list.append(l.strip())
    return text_list

def get_count_list(text_list, tag):
    count_list = []
    words_list = []
    for i in range(len(text_list)):
        text = text_list[i]
        if not text:
            continue
        words = get_pos_list(text, tag)
        print(f'[{i}/{len(text_list)}] {text} {words}')
        words_list.append(words)
    
    words_list.sort(key=len, reverse=True)
    words_list = words_list[:num_list_to_count]

    for i in range(len(words_list)):
        count_list.append(Counter(words_list[i]))

    return count_list

text_list = read_corpus(in_corpus)
count_list = get_count_list(text_list, tag)

with open(out_counts,'wb') as fw:
    pickle.dump(count_list, fw)
