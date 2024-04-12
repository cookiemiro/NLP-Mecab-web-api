#! /usr/bin/python3 
# -*- coding: utf-8 -*-

import os
import csv

def load_non_keyword() :
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resources/nonKeywordList.csv')
	with open(path, encoding='utf-8') as fp:
		keywords = [w[0] for w in csv.reader(fp)]
	return keywords

