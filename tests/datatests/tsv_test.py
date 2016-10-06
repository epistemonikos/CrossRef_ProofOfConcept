#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint
import os

rrsr = open('./src/random_results_systematic_review')

line = rrsr.readline()
while line:
    sline = line.split('\t')
    if len(sline) > 1:
        episte_doi = sline[0] or '-'
        reference = ''.join(sline[1:]) or '-'
        x = requests.get('http://0.0.0.0:5001/api/v1/crsearch', params={
            'ref' : reference
        })
        rating = x.json().get('rating', {}).get('total', 0)
        crossRef_doi = x.json().get('ids', {}).get('doi', '-')
        print("%.2f\t%s\t%s\t%s" % (rating, crossRef_doi, episte_doi, reference))
    line = rrsr.readline()
