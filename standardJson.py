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

def crossRefToStandard(crossrefJson):
    standard = {}
    standard['title'] = tryAccesslist (tryAccessdict(crossrefJson,'title'),0)
    standard['abstract'] = ""
    standard['language'] = ""
    standard['ids'] = {}
    standard['ids']['doi'] = tryAccessdict(crossrefJson,'DOI')
    standard['ids']['embase'] = ""
    standard['ids']['pubmed'] = ""
    standard['publication_type'] = {}
    standard['publication_type']['pagination'] = tryAccessdict(crossrefJson,'page')
    standard['publication_type']['cited_medium'] = ""
    standard['publication_type']['title'] = tryAccessdict(crossrefJson,'publisher')
    standard['publication_type']['type'] = tryAccessdict(crossrefJson,'type')
    standard['publication_type']['ISSN'] = tryAccesslist(tryAccessdict(crossrefJson,'ISSN'),0)
    standard['publication_type']['volume'] = tryAccessdict(crossrefJson,'volume')
    standard['publication_type']['year'] = str (tryAccesslist(tryAccesslist(tryAccessdict(tryAccessdict(crossrefJson,'issued'),'date-parts'),0),0))
    standard['publication_type']['issue'] = tryAccessdict(crossrefJson,'issue')
    standard['authors'] = []
    for author in tryAccessdict(crossrefJson,'author'):
        standard['authors'].append(tryAccessdict(author,'family')  +" " +tryAccessdict(author,'given'))
    return json.dumps(standard)



