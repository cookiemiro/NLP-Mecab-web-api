#! /usr/bin/python3 
# -*- coding: utf-8 -*-

def get_transcript(words):
	transcript = ''
	for i in range(len(words)):
		transcript += words[i]['word'] + ' '
	return transcript
