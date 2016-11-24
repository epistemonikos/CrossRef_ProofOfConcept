#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint
import os
"""
This files its similar to auto_test.py, but it print on the standar output the results of testing.
"""
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

reference = input()
while reference != 'q':
    print("searching...")
    x = requests.get('http://0.0.0.0:5001/api/v1/crsearch', params={
        'ref' : reference
    })
    json = x.json()
    rating = json.get('rating',0)
    autor = json.get('author')
    title = json.get('title')
    year = str(json['created']['date-parts'][0][0])
    pretty_reference(reference)
    Color.puts("DOI: %s" % x.json().get('ids', {}).get('doi', '-'), Color.PINK)
    Color.puts("Rating: %.2f%%" % (rating['total']*100), Color.YELLOW)
    print("RatingTitle: %.2f%%" % (rating['title']*100))
    print("RatingAuthors: %.2f%%" % (rating['authors']*100))
    print("RatingYear: %.2f%%" % (rating['year']*100))
    print("autor: %s" % autor)
    print("year: %s" % year)
    print("title: %s\n" % title)
    reference = input()
