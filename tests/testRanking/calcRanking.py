__author__ = 'fmosso'

import math
import base64
import csv
import ast
import json
import binascii

AVGLENGTH = 220

weight1= {'title' :0.65, 'authors' : 0.2 , 'year': 0.15}
weight2= {'title' :0.5, 'authors' : 0.0 , 'year': 0.5}
weight3= {'title' :0.1, 'authors' : 0.0 , 'year': 0.9}
weight4= {'title' :0.9, 'authors' : 0.05 , 'year': 0.05}

weights = [weight1,weight2,weight3,weight4]
csv.field_size_limit(500 * 1024 * 1024)

def setWeight(t=0.0,a=0.0,y=0.0):
    return {'title' :t, 'authors' : a , 'year': y}

def weightLength(len):
    if len >= AVGLENGTH:
        len=AVGLENGTH
    if len < 1:
        len = 1
    return  math.log10(len) / math.log10(AVGLENGTH)

def calcRating(ratings, weight,length):
    lenWeight = weightLength(length)
    return (ratings['title']*weight['title'] + ratings['authors']*weight['authors'] + ratings['year']*weight['year'])*lenWeight


def calRankings(listOfRankings):
    with open('data140k.tsv') as tsvin, open('rankingResults140k.tsv', 'wt') as csvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        csvout = csv.writer(csvout)
        first_row = ["Original"]
        def wtoStr(weight):
            return 't:'+str(weight['title'])+ ' a:'+str(weight['authors'])+' y:'+str(weight['year'])
        for weight in listOfRankings:
            first_row.append(wtoStr(weight))
        csvout.writerow(first_row)
        print(first_row)
        for row in tsvin:
            numberOfCollum = len(row)
            if numberOfCollum == 0:
                continue
            citlength = len(row[0])
            standartJSON = row[numberOfCollum-1]
            try:
                ratings = json.loads(base64.urlsafe_b64decode(standartJSON).decode("utf-8"))['result'][0]

            except (UnicodeDecodeError,binascii.Error,json.decoder.JSONDecodeError):
                ratings = {}
            rankings = [ratings.get('rating',{}).get('total',0)]
            for weight in listOfRankings:
                rankings.append(calcRating(ratings.get('rating',{'year': 0, 'title': 0, 'total': 0, 'authors': 0}),weight,citlength))
            csvout.writerow(rankings)

calRankings(weights)