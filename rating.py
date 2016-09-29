#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from stop_words import get_stop_words

reference = u"Gomes, E., Bastos, T., Probst, M., Ribeiro, J.C., Silva, G., Corredeira, R., 2014. Effects of a group physical activity program on physical fitness and quality of life in individuals with schizophrenia. Mental Health and Physical Activity 7, 155–162."
# reference = u"Scheewe, et al., 2008. Physical activity and cardiovascular fitness in patients with schizophrenia. The Fourth European Congress of PsychomotricityAn. Int. J. Theory Res. Prac. 4 (1). Amsterdam, Body, Move Dance Psychother, The Netherlands, pp. 67–71 2008"

def cita_without_stop_words(raw_cita):
    stop_words = get_stop_words('en')
    return ''.join([c for c in raw_cita if c not in stop_words])

def year_rate(year, raw_cita):
    cita = cita_without_stop_words(raw_cita)
    rates = [{
        'char' : '/',
        'val' : 1
    },{
        'char' : '-',
        'val' : 1
    },{
        'char' : ' ',
        'val' : 0.75
    },{
        'char' : '',
        'val' : 0.25
    }]
    for rate in rates:
        en_year = rate['char']+str(year)
        latin_year = str(year)+rate['char']
        if en_year in cita:
            return rate['val'] if ((en_year+' ') in cita) or ((en_year+'.') in cita) else 0.5*rate['val']
        if latin_year in cita:
            return rate['val'] if (' '+latin_year) in cita else 0.5*rate['val']
    return 0

def title_rate(raw_title, raw_cita):
    if raw_title in raw_cita:
        return 1
    cita = cita_without_stop_words(raw_cita)
    title = cita_without_stop_words(raw_title)
    title_in_cita = [c for c in title if c in cita]
    rating = len(title_in_cita)/len(title) if len(title) > 0 else 0
    # TODO: puntaje proporcional a la distancia entre las palabras con match
    return rating


def authors_rate(authors_given, authors_family, raw_cita):
    authors = [{
        'full_name' : "%s %s" % (authors_family[i], authors_given[i]),
        'abrev_name' : "%s %s." % (authors_family[i], authors_given[i][0]),
        'abrev_name_2' : "%s, %s." % (authors_family[i], authors_given[i][0]),
        'given_name' : "%s" % (authors_given[i]),
        'familyname' : "%s" % (authors_family[i])
    } for i in range(len(authors_given))]
    raw_rating = 0
    for author in authors:
        raw_rating += author_rate(author, raw_cita)
    rating = raw_rating/len(authors) if len(authors) > 0 else 0
    return rating

def author_rate(author, raw_cita):
    rates = [{
        'style' : 'full_name',
        'val' : 1
    },{
        'style' : 'abrev_name',
        'val' : 0.9
    },{
        'style' : 'abrev_name_2',
        'val' : 0.9
    },{
        'style' : 'given_name',
        'val' : 0.5
    },{
        'style' : 'familyname',
        'val' : 0.5
    }]
    cita = raw_cita.encode('ascii','ignore')
    for rate in rates:
        auth = author[rate['style']].encode('ascii','ignore')
        if auth in cita:
            # print "%s : %s" % (auth, rate['val'])
            return rate['val']
        # else:
        #     print "%s not in %s" % (auth, auth in cita)
    # print "%s : %s" % (author, 0)
    return 0

def pretty_cita(line):
    return '\n'.join([line[i:i+50] for i in range(0, len(line), 50)])

def crossref(citation):
    json = requests.get('http://api.crossref.org/works', params={
        'query': citation.strip()
    }).json()['message']['items'][0]

    authors_given = [aut['given'] for aut in json['author']]
    authors_family = [aut['family'] for aut in json['author']]
    year = json['published-print']['date-parts'][0][0]
    title = json['title'][0]

    return {
        'authors_given' : authors_given,
        'authors_family' : authors_family,
        'year' : year,
        'title' : title
    }

def rating(json, raw_cita):
    a_rate = authors_rate(json['authors_given'], json['authors_family'], raw_cita)
    print "authors: %s" % a_rate
    y_rate = year_rate(json['year'], raw_cita)
    print "year: %s" % y_rate
    t_rate = title_rate(json['title'], raw_cita)
    print "t_rate: %s" % t_rate
    final_rate = a_rate*0.2 + y_rate*0.1 + t_rate*0.7
    print "final_rate: %s" % final_rate
    return final_rate

def app(cita):
    print pretty_cita(cita)
    print ''
    json = crossref(cita)
    print json
    print ''
    rating(json, cita)

# app(reference)
