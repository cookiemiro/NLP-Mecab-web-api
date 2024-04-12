#! /usr/bin/python3 
# -*- coding: utf-8 -*-

#
#	Written by Sangyoun Paik, ActionPower
#
#	- Extract keywords either from file or string 
#	- Usage 
#		$ python3 get_keyword_tfidf.py [input_type] [input_doc] [noun_counts_statistics]
#

import math
import nltk
import numpy
import os
import pickle
import sys

from collections import Counter
from konlpy.tag import Mecab
mecab = Mecab("c:\mecab\mecab-ko-dic")

candidate_num = 30
target_keywords_num = 10
ALL_NOUNS = True

def get_candidates(target_doc, num_candidate, input_type, language):
    if(input_type == 'file'):
        f = open(target_doc, "r")
        target_string = f.read()
    elif(input_type == 'string'):
        target_string = target_doc

    if(language == 'kor'):
        if(ALL_NOUNS):
            words = mecab.nouns(target_string)
        else:
            all_pos = mecab.pos(target_string)
            nng_nnp_list = [elem for elem in all_pos if (elem[1] == 'NNG' or elem[1] == 'NNP')] # 일반명사, 고유명사
    
            words = []
            for i in range(len(nng_nnp_list)):
                words.append(nng_nnp_list[i][0])
    
    elif(language == 'kor-va'):
        all_pos = mecab.pos(target_string)
        word_list = [elem for elem in all_pos if ('VA' in elem[1])] # 형용사
        words = []
        for i in range(len(word_list)):
            words.append(word_list[i][0])

    elif(language == 'eng'):
        is_noun = is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = nltk.pos_tag(nltk.word_tokenize(target_string.lower()))
        words = [word for (word, pos) in tokenized if is_noun(pos)]

    else:
        words = []

    count = Counter(words)
    return count.most_common(num_candidate)

def get_TF_IDFs(counts, candidates, N):
	TF_IDF = []
	for n,c in candidates:
		num_containing_docs = 0.001
		for x in range(N):
			for y,z in counts[x].most_common(100):
				if(n==y):
					num_containing_docs = num_containing_docs + 1
					break;
		freq = c
		TF_IDF.append(freq * math.log(N/num_containing_docs))

	return TF_IDF

def get_index_n_keywords(TF_IDFs, n_keywords):
	arr=numpy.array(TF_IDFs)
	return (-arr).argsort()[:n_keywords]

def get_keywords(target_doc, noun_counts_file, num_candidate, n_keywords, input_type, language):
	keywords = []

	with open (noun_counts_file, 'rb') as fp:
	    saved_counts = pickle.load(fp)
	N = len(saved_counts)

	candidates = get_candidates(target_doc, num_candidate, input_type, language)

	TF_IDFs = get_TF_IDFs(saved_counts, candidates, N)

	idx = get_index_n_keywords(TF_IDFs, n_keywords)
	
	for i in range(len(idx)):
		#print(candidates[idx[i]])
		keywords.append(candidates[idx[i]])

	keywords.sort(key=lambda elem: elem[1], reverse=True)
	
	return keywords

def main(argv):
	input_type = argv[0]
	input_doc = argv[1]
	noun_counts_statistics = argv[2]
	language = argv[3]
	return get_keywords(input_doc, noun_counts_statistics, candidate_num, target_keywords_num, input_type, language)

if __name__ == '__main__':
	main(sys.argv[1:])
