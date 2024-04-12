#! /usr/bin/python3 
# -*- coding: utf-8 -*-

import os
import sys
import json
import subprocess

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import get_keyword_tfidf
from transcriptutils import get_transcript
from nonkeywordlist import nonKeywordList as nonkeywordlist

NON_KEYWORD_LIST = nonkeywordlist.load_non_keyword()
MIN_COUNT = 1
MIN_LENGTH = 1
NOUN_COUNTS_KOREAN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/noun_counts')
VA_COUNTS_KOREAN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/va_counts')
NOUN_COUNTS_ENGLISH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/noun_counts_english')

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

# Daglo Interface
def runKeywordExtraction(in_json, language='kor', min_length=MIN_LENGTH):
    if(language=='kor'):
        noun_counts_statistics = NOUN_COUNTS_KOREAN
    elif(language=='eng'):
        noun_counts_statistics = NOUN_COUNTS_ENGLISH
    else:
        print('Keyword extraction failed. Wrong input argument {language}...')
        sys.exit(-1)

    out_json = generate_tmp(in_json)

    with open(out_json) as json_file:
        json_data = json.load(json_file)
        result = json_data['results'][0]['alternatives'][0]
        words = result['words']
		
        transcript = get_transcript(words)

        raw_keyword_counts = get_keyword_tfidf.main(['string', transcript, noun_counts_statistics, language])
		
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
def runKeywordExtractionString(in_string, candidate_num, target_keywords_num, language='kor', min_length=MIN_LENGTH):
    if(language=='kor'):
        noun_counts_statistics = NOUN_COUNTS_KOREAN
    elif(language=='kor-va'):
        noun_counts_statistics = VA_COUNTS_KOREAN 
    elif(language=='eng'):
        noun_counts_statistics = NOUN_COUNTS_ENGLISH
    else:
        print('Keyword extraction failed. Wrong input argument {language}...')
        sys.exit(-1)
    raw_keyword_counts = get_keyword_tfidf.get_keywords(in_string, noun_counts_statistics, candidate_num, target_keywords_num, 'string', language)
    keyword_counts = remove_unlikely_keywords(raw_keyword_counts, min_length)
    keyword_counts = remove_non_keywords(keyword_counts)
    return keyword_counts
