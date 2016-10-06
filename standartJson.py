__author__ = 'fmosso'
import json
#with open('crossrefjson2.json') as data_file:
#    data = json.load(data_file)

#try-catchs if there not
def tryAccessdict(dict,arg):
    try:
        return dict[arg]
    except IndexError:
        return ""

def tryAccesslist(list,index):
    try:
        return list[index]
    except KeyError:
        return ""

def crossRefToStandart(crossrefJson):
    standart = {}
    standart['title'] = tryAccesslist (tryAccessdict(crossrefJson,'title'),0)
    standart['abstract'] = ""
    standart['language'] = ""
    standart['ids'] = {}
    standart['ids']['doi'] = tryAccessdict(crossrefJson,'DOI')
    standart['ids']['embase'] = ""
    standart['ids']['pubmed'] = ""
    standart['publication_type'] = {}
    standart['publication_type']['pagination'] = tryAccessdict(crossrefJson,'page')
    standart['publication_type']['cited_medium'] = ""
    standart['publication_type']['title'] = tryAccessdict(crossrefJson,'publisher')
    standart['publication_type']['type'] = tryAccessdict(crossrefJson,'type')
    standart['publication_type']['ISSN'] = tryAccesslist(tryAccessdict(crossrefJson,'ISSN'),0)
    standart['publication_type']['volume'] = tryAccessdict(crossrefJson,'volume')
    standart['publication_type']['year'] = str (tryAccesslist(tryAccesslist(tryAccessdict(tryAccessdict(crossrefJson,'issued'),'date-parts'),0),0))
    standart['publication_type']['issue'] = tryAccessdict(crossrefJson,'issue')
    standart['authors'] = []
    for author in tryAccessdict(crossrefJson,'author'):
        standart['authors'].append(tryAccessdict(author,'family')  +" " +tryAccessdict(author,'given'))
    return json.dumps(standart)



