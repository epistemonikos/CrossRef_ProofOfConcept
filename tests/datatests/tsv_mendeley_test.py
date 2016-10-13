#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint
import os

with open('result/output_correctos.tsv', 'w') as output_correctos:
    with open('result/output_incorrectos.tsv', 'w') as output_incorrectos:
        with open('./src/random_results_systematic_review') as rrsr:
            count = 0
            for line in rrsr:
                count += 1
                try:
                    if count%20 == 0:
                        print("Estoy vivo. Llevo: {0}".format(count))
                    sline = line.split('\t')
                    if len(sline) > 1:
                        episte_doi = sline[0] or '-'
                        reference = ''.join(sline[1:]) or '-'
                        x = requests.get('http://localhost:5001/api/v1/mdsearch', params={
                            'ref' : reference
                        })
                        rating = x.json().get('rating', {}).get('total', 0)
                        mendeley_doi = x.json().get('ids', {}).get('doi', '-')
                        if mendeley_doi and "doi.org" in mendeley_doi:
                            index = mendeley_doi.index(".org/") + 5
                            mendeley_doi = mendeley_doi[index:]

                        new_line = u"{}\t{}\t{}\t{:.2f}\t{:s}\n".format('Mendeley', mendeley_doi, episte_doi,
                                                                                 rating, reference)
                        if mendeley_doi == episte_doi:
                            print("Correcto: " + new_line)
                            output_correctos.write(new_line)
                        else:
                            print("Incorrecto: " + new_line)
                            output_incorrectos.write(new_line)
                except:
                    pass

