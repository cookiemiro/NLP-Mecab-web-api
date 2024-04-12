#! /usr/bin/python3 
# -*- coding: utf-8 -*-

import json
import math
import numpy
import os
import pickle
import subprocess
import sys

from collections import Counter
from konlpy.tag import Mecab
mecab = Mecab()

from src.keywordExtraction.nonkeywordlist import nonKeywordList as nonkeywordlist
import nltk

DEFAULT_CANDIDATE_NUM = 30
DEFAULT_TARGET_KEYWORDS_NUM = 10
NUM_SAVED_COUNTS_FOR_PREDICTION = 500

MIN_COUNT = 0
MIN_LENGTH = 0
NOUN_COUNTS_KOREAN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/noun_counts')
# NOUN_COUNTS_KOREAN = [("올리브영", "올리브", "올리브 영")]
VA_COUNTS_KOREAN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/va_counts')
ADJECTIVE_COUNTS_KOREAN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/adjective.counts')
ADJECTIVE_AND_NOUN_COUNTS_KOREAN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/adjective_and_noun.counts')
NOUN_COUNTS_ENGLISH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/noun_counts_english')
ADJECTIVE_COUNTS_ENGLISH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/eng.adjective.counts')

NON_KEYWORD_LIST = nonkeywordlist.load_non_keyword()

def check_and_download_nltk_requisite():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

def get_pos_list(target_string, tag='noun'):
    def get_adjectives(all_pos):
        words = []
        for i in range(len(all_pos)):
            if i < len(all_pos)-1:
                if 'VA' in all_pos[i][1]:
                    if 'VA+' in all_pos[i][1]:
                        words.append(all_pos[i][0])
                    if ('EF' in all_pos[i+1][1]) or ('EC' in all_pos[i+1][1]) or ('ETM' in all_pos[i+1][1]):
                        words.append(all_pos[i][0] + all_pos[i+1][0])
        return words

    words = []
    if tag=='kor-noun':
        all_pos = mecab.pos(target_string)
        pos_list = [elem for elem in all_pos if (elem[1] == 'NNG' or elem[1] == 'NNP')] # 일반명사, 고유명사
        for i in range(len(pos_list)):
            words.append(pos_list[i][0])

    elif tag == 'kor-va': # 형용사인데 va 만
        all_pos = mecab.pos(target_string)
        pos_list = [elem for elem in all_pos if ('VA' in elem[1])] # 형용사
        for i in range(len(pos_list)):
            words.append(pos_list[i][0])

    elif tag == 'kor-adjective': 
        all_pos = mecab.pos(target_string)
        words = get_adjectives(all_pos)

    elif tag == 'kor-adjective-and-noun':
        all_pos = mecab.pos(target_string)
        noun_list = [elem for elem in all_pos if (elem[1] == 'NNG' or elem[1] == 'NNP')] # 일반명사, 고유명사
        for i in range(len(noun_list)):
            words.append(noun_list[i][0])
        adjectives = get_adjectives(all_pos)
        words += adjectives

    elif tag == 'eng-noun':
        is_noun = is_noun = lambda pos: pos[:2].startswith('NN')
        tokenized = nltk.pos_tag(nltk.word_tokenize(target_string))
        words = [word for (word, pos) in tokenized if is_noun(pos)]

    elif tag == 'eng-adjective':
        is_noun = is_noun = lambda pos: pos[:2].startswith('JJ')
        tokenized = nltk.pos_tag(nltk.word_tokenize(target_string))
        words = [word for (word, pos) in tokenized if is_noun(pos)]

    return words

def get_candidates(target_doc, num_candidate, input_type, language, verbose):
    if(input_type == 'file'):
        f = open(target_doc, "r")
        target_string = f.read()
    elif(input_type == 'string'):
        target_string = target_doc

    if(language == 'kor'):
        words = get_pos_list(target_string, tag='kor-noun')
    elif(language == 'kor-va'):
        words = get_pos_list(target_string, tag='kor-va')
    elif language == 'kor-adjective':
        words = get_pos_list(target_string, tag='kor-adjective')
    elif language == 'kor-adjective-and-noun':
        words = get_pos_list(target_string, tag='kor-adjective-and-noun')
    elif(language == 'eng'):
        words = get_pos_list(target_string, tag='eng-noun')
    elif(language == 'eng-adjective'):
        words = get_pos_list(target_string, tag='eng-adjective')
    else:
        words = []

    if verbose:
        print(f'all pos words: {words}')

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
# get_keywords(transcript, noun_counts_statistics, DEFAULT_CANDIDATE_NUM, DEFAULT_TARGET_KEYWORDS_NUM, 'string', language, verbose)

def get_keywords(target_doc, noun_counts_file, num_candidate, n_keywords, input_type, language, num_saved_counts_for_prediction, verbose):
    keywords = []

    with open (noun_counts_file, 'rb') as fp:
        saved_counts = pickle.load(fp)[:num_saved_counts_for_prediction]
    N = len(saved_counts)

    candidates = get_candidates(target_doc, num_candidate, input_type, language, verbose)
    if verbose:
        print(f'candidates: {candidates}')

    TF_IDFs = get_TF_IDFs(saved_counts, candidates, N)
    if verbose:
        print(f'TF_IDFs: {TF_IDFs}')

    idx = get_index_n_keywords(TF_IDFs, n_keywords)

    for i in range(len(idx)):
        #print(candidates[idx[i]])
        keywords.append(candidates[idx[i]])

    keywords.sort(key=lambda elem: elem[1], reverse=True)
    return keywords

### Daglo Interface
'''
	In: in_json (e.g. '/kaldi/egs/daglo/decoder_vlite5.0/decode_results/sample/sample.decode.timestamp.json')
	Out: tmp_json (e.g. '/kaldi/egs/daglo/decoder_vlite5.0/decode_results/sample/sample.decode.timestamp.ke_tmp.json')
'''
def generate_tmp(in_json):
    base_name = os.path.basename(os.path.abspath(in_json))
    dir_name = os.path.dirname(os.path.abspath(in_json))
    new_base_name = base_name.split('.json')[0] + '.ke_tmp.json'
    tmp_json = os.path.join(dir_name, new_base_name)
    subprocess.call('cp ' + in_json + ' ' + tmp_json, shell=True)
    return tmp_json

def remove_unlikely_keywords(keyword_counts, min_length):
    return [keyword_count for keyword_count in keyword_counts if keyword_count[1] > MIN_COUNT  and len(keyword_count[0].strip()) > min_length]

def remove_non_keywords(keyword_counts):
    return [keyword_count for keyword_count in keyword_counts if (keyword_count[0].strip() not in NON_KEYWORD_LIST)]

def run_keyword_extraction(in_json, language='kor', min_length=MIN_LENGTH, verbose=False):
    def get_transcript(words):
        transcript = ''
        for i in range(len(words)):
            transcript += words[i]['word'] + ' '
        return transcript
    
    if(language=='kor'):
        noun_counts_statistics = NOUN_COUNTS_KOREAN
    elif(language=='kor-va'):
        noun_counts_statistics = VA_COUNTS_KOREAN 
    elif(language=='kor-adjective'):
        noun_counts_statistics = ADJECTIVE_COUNTS_KOREAN 
    elif(language=='kor-adjective-and-noun'):
        noun_counts_statistics = ADJECTIVE_AND_NOUN_COUNTS_KOREAN 
    elif(language=='eng'):
        check_and_download_nltk_requisite()
        noun_counts_statistics = NOUN_COUNTS_ENGLISH
    elif(language=='eng-adjective'):
        check_and_download_nltk_requisite()
        noun_counts_statistics = ADJECTIVE_COUNTS_ENGLISH
    else:
        print(f'Keyword extraction failed. Wrong input argument {language}...')
        sys.exit(-1)

    out_json = generate_tmp(in_json)

    with open(out_json) as json_file:
        json_data = json.load(json_file)
        result = json_data['results'][0]['alternatives'][0]
        words = result['words']
		
        transcript = get_transcript(words)

        #raw_keyword_counts = get_keyword_tfidf.main(['string', transcript, noun_counts_statistics, language])
        raw_keyword_counts = get_keywords(transcript, noun_counts_statistics, DEFAULT_CANDIDATE_NUM, DEFAULT_TARGET_KEYWORDS_NUM, 'string', language, verbose)
		
        keyword_counts = remove_unlikely_keywords(raw_keyword_counts, min_length)
		
        keyword_counts = remove_non_keywords(keyword_counts)

        json_data['results'][0]['alternatives'][0].update({'keywords':keyword_counts})

        if(keyword_counts):
            for i in range(len(words)):
                curr_word = words[i]['word']
                for keyword_count in keyword_counts:
                    keyword = keyword_count[0] # [0]:keyword, [1]:count
                    if(keyword in curr_word):
                        json_data['results'][0]['alternatives'][0]['words'][i].update({'hasKeyword':True})
                        break
                    json_data['results'][0]['alternatives'][0]['words'][i].update({'hasKeyword':False})
        else:
            for i in range(len(words)):
                json_data['results'][0]['alternatives'][0]['words'][i].update({'hasKeyword':False})
		
        # overwrite result to in_json
        with open(in_json, 'w') as f_json:
            json.dump(json_data, f_json, ensure_ascii=False, indent='\t')

# String Input Interface
def run_keyword_extraction_string(in_string, candidate_num=DEFAULT_CANDIDATE_NUM, target_keywords_num=DEFAULT_TARGET_KEYWORDS_NUM, language='kor', min_length=MIN_LENGTH, num_saved_counts_for_prediction=NUM_SAVED_COUNTS_FOR_PREDICTION, verbose=False):
    if(language=='kor'):
        noun_counts_statistics = NOUN_COUNTS_KOREAN
    elif(language=='kor-va'):
        noun_counts_statistics = VA_COUNTS_KOREAN 
    elif(language=='kor-adjective'):
        noun_counts_statistics = ADJECTIVE_COUNTS_KOREAN 
    elif(language=='kor-adjective-and-noun'):
        noun_counts_statistics = ADJECTIVE_AND_NOUN_COUNTS_KOREAN 
    elif(language=='eng'):
        check_and_download_nltk_requisite()
        noun_counts_statistics = NOUN_COUNTS_ENGLISH
    elif(language=='eng-adjective'):
        check_and_download_nltk_requisite()
        noun_counts_statistics = ADJECTIVE_COUNTS_ENGLISH
    else:
        print('Keyword extraction failed. Wrong input argument {language}...')
        sys.exit(-1)
    
    raw_keyword_counts = get_keywords(in_string, noun_counts_statistics, candidate_num, target_keywords_num, 'string', language, num_saved_counts_for_prediction, verbose)
    keyword_counts = remove_unlikely_keywords(raw_keyword_counts, min_length)
    keyword_counts = remove_non_keywords(keyword_counts)
    return keyword_counts

def run_keyword_extraction_api(in_string, language='kor', max_num_keywords=10, num_saved_counts_for_prediction=NUM_SAVED_COUNTS_FOR_PREDICTION):
    return run_keyword_extraction_string(in_string, candidate_num=max_num_keywords*3, target_keywords_num=max_num_keywords, language=language, num_saved_counts_for_prediction=num_saved_counts_for_prediction)
