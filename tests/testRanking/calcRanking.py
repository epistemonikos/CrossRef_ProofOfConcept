__author__ = 'fmosso'

import math
import base64
import csv
import ast
import json
AVGLENGTH = 220

weight1= {'title' :0.65, 'authors' : 0.2 , 'year': 0.15}
weight2= {'title' :0.50, 'authors' : 0.5 , 'year': 0.0}
weight3= {'title' :0.50, 'authors' : 0.0 , 'year': 0.5}
weight4= {'title' :0.9, 'authors' : 0.05 , 'year': 0.05}

weights = [weight1,weight2,weight3,weight4]

def weightLength(len):
    if len >= 220:
        len=220
    if len < 1:
        len = 1
    return  math.log10(len) / math.log10(AVGLENGTH)

def calcRating(ratings, weight,length):
    lenweight = weightLength(length)
    return (ratings['title']*weight['title'] + ratings['authors']*weight['authors'] + ratings['year']*weight['year'])*lenweight

with open('data.tsv') as tsvin, open('rankingResults.tsv', 'wt') as csvout:
    tsvin = csv.reader(tsvin, delimiter='\t')
    csvout = csv.writer(csvout)
    csvout.writerow(["Original","w1(t:0.65 a:0.2 y:0.15)", "w2(t:0.5 a:0.5 y:0.0)", "w3(t:0.5 a:0.0 y:0.5)","w4(t:0.9 a:0.05 y:0.05)"])
    for row in tsvin:
        numberOfCollum = len(row)
        citlength = len(row[0])
        ratings = ast.literal_eval(row[numberOfCollum-1])
        #ratings = json.loads(base64.urlsafe_b64decode(row[numberOfCollum-1]).decode("utf-8"))
        rankings = [ratings.get('rating',{}).get('total',0)]
        for weight in weights:
            rankings.append(calcRating(ratings.get('rating',{'year': 0, 'title': 0, 'total': 0, 'authors': 0}),weight,citlength))
        csvout.writerow(rankings)


