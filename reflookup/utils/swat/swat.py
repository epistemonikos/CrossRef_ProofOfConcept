from reflookup.utils.parsers import parser
from reflookup.resources.lookup_functions.citation_extract import get_scopus_ref
from reflookup.resources.lookup_functions.citation_extract import getRefID, getReferenceInfo
import json
#Paso 1: leer tsv
dump = open('./src/dump_pdq_chechis.tsv')
output = open('./result/input_grafo.txt', 'w')
errors = open('./result/unresolved_grafo.txt', 'w')

line = dump.readline()
n = 0


def get_param(param, res_parser, res_scopus, res_pubmed):
    res = None
    if param == "references":
        try:
            res = res_parser[param] + res_scopus.get(param, []) + res_pubmed
        except:
            res = None
    elif isinstance(param, dict):
        try:
            res_parser["publication_info"][param["publication_info"]] + res_scopus.get("publication_info")[param["publication_info"]]
        except:
            res = None

    else:
        try:
            res = res_parser[param] or res_scopus.get(param)
        except:
            res = None
    return res


while line:
    n += 1
    # if n < 100:
    #     line = dump.readline()
    #     continue
    # por cada linea, resolver referencias con los servicios de la API
    try:
        [episteID, doi, pmid] = line.strip().split('\t') # episteID, doi, pmid
    except:
        line = dump.readline()
        errors.write(line + '\n')
        continue
    res_parser = {}
    try:
        res_parser = parser.parse(doi)
    except:
        pass
    res_scopus = {}
    try:
        res_scopus = get_scopus_ref(doi)
    except:
        pass
    res_pubmed = []
    try:
        res_pubmed = getReferenceInfo(getRefID(pmid))
    except:
        pass
    #imprimir a archivo nuevo llamado
    #  input_grafo.txt
    j = {
        "title": get_param("title",res_parser ,res_scopus, res_pubmed),
        "authors": get_param("authors", res_parser, res_scopus, res_pubmed),
        "abstract": get_param("abstract", res_parser, res_scopus, res_pubmed),
        "ids": {
            "doi": doi,
            "pmid": pmid,
            "episteId": episteID
        },
        "keywords": get_param("keywords", res_parser, res_scopus, res_pubmed),
        "publication_info": {
            "issue": get_param({"publication_info": "issue"}, res_parser, res_scopus, res_pubmed),
            "journal": get_param({"publication_info": "journal"}, res_parser, res_scopus, res_pubmed),
            "year": get_param({"publication_info": "year"}, res_parser, res_scopus, res_pubmed),
            "volume": get_param({"publication_info": "volume"}, res_parser, res_scopus, res_pubmed),
            "pages": get_param({"publication_info": "pages"}, res_parser, res_scopus, res_pubmed),
        },
        "citation": get_param("citation", res_parser, res_scopus, res_pubmed),
        "references": get_param("references", res_parser, res_scopus, res_pubmed)
    }
    if n%10 == 0:
        print("Cantidad de RS resueltas: "+str(n)+"\n")
    output.write(json.dumps(j)+'\n')
    line = dump.readline()
if output:
    output.close()






