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

line = rrsr.readline()
while line:
    sline = line.split('\t')
    if len(sline) > 1:
        episte_doi = sline[0]
        reference = ''.join(sline[1:])
        x = requests.get('http://0.0.0.0:5001/api/v1/crsearch', params={
            'ref' : reference
        })
        rating = x.json().get('rating',0)
        pretty_reference(reference)
        Color.puts("EpisteDOI: %s" % episte_doi, Color.BOLD)
        Color.puts("DOI: %s" % x.json().get('ids',{}).get('doi','-'), Color.PINK)
        Color.puts("Rating: %.2f%%\n\n" % (rating['total']*100), Color.YELLOW)
    line = rrsr.readline()
