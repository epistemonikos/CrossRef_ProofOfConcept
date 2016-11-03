#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint
import os
import csv

counter_file = open('count', 'r')
count = counter_file.read() or 0
counter_file.close()

with open('data.tsv', 'w') as output_citas:
  with open('input.tsv') as input_citas:
    
      ##input_citas.skip_lines(count)


      for _ in range(count):
        next(input_citas)
        
      for line in input_citas:
        
        line.replace ("\n", " ")
        sline = line.split('\t')
       
        if len(sline) > 1:
          cita = sline[0] or '-'
          episte_doi = sline[1] or '-'
          episte_pubmedId = sline[2] or '-'
          episte_clasification = sline[3] or '-'
          episte_id = sline[4] or '-'

          if sline[5] == "\n":
            episte_ref_id = '-'
          else:
            episte_ref_id = sline[5] or '-'
          
          try:
            x = requests.get('http://52.3.221.80/api/v1/crsearch', params={
              'ref' : cita
              },
              headers= {
              'Accept-Encoding': 'base64'
              })
            crossref_json = x.text
            cr_line = u"{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cita, episte_doi, episte_pubmedId, episte_clasification, episte_id, episte_ref_id.replace("\n","_"), crossref_json)

          except:
            cr_line = "LINEERROR"

          try:
            y = requests.get('http://52.3.221.80/api/v1/mdsearch', params={
              'ref' : cita
              },
              headers= {
              'Accept-Encoding': 'base64'
              })
            mendeley_json = y.text
            md_line = u"{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(cita, episte_doi, episte_pubmedId, episte_clasification, episte_id, episte_ref_id.replace("\n","_"), mendeley_json)

          except:
            md_line = "LINEERROR"

          output_citas.write(cr_line)
          output_citas.write(md_line)

        count += 1
        counter_file = open('count', 'w')
        counter_file.write(count)
        counter_file.close()
        if count%20 == 0:
          print("Estoy vivo. Llevo: {0}".format(count))