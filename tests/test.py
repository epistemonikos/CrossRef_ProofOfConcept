#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint
import os

class Color:
    PINK = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    puts = lambda x, color : print(color + x + Color.ENDC)

def pretty_reference(cita):
    print('\n'.join([cita[i:i+50] for i in range(0, len(cita), 50)]))

# gsort --random-sort results_systematic_review > random_results_systematic_review

rrsr = open('./src/random_results_systematic_review')

while input() != 'exit':
    sline = rrsr.readline().split('\t')
    while len(sline) < 2:
        sline = rrsr.readline().split('\t')
    episte_doi = sline[0]
    reference = ''.join(sline[1:])
    print("searching...")
    x = requests.get('http://0.0.0.0:5001/api/v1/crsearch', params={
        'ref' : reference
    })
    rating = x.json().get('rating',0)
    pretty_reference(reference)
    Color.puts("EpisteDOI: %s" % episte_doi, Color.BOLD)
    Color.puts("DOI: %s" % x.json().get('DOI','-'), Color.PINK)
    Color.puts("URL: %s" % x.json().get('URL','-'), Color.GREEN)
    Color.puts("Rating: %.2f%%" % (rating['total']*100), Color.YELLOW)
    print("RatingTitle: %.2f%%" % (rating['title']*100))
    print("RatingTuthors: %.2f%%" % (rating['authors']*100))
    print("RatingYear: %.2f%%\n" % (rating['year']*100))
