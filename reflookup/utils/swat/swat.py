from reflookup.utils.parsers import parser
from reflookup.resources.lookup_functions.citation_extract import get_scopus_ref
from reflookup.resources.lookup_functions.citation_extract import getRefID, getReferenceInfo
import json
#Paso 1: leer tsv
dump = open('./src/dump_pdq_chechis.tsv')

line = dump.readline()
n = 0
while line:
    # por cada linea, resolver referencias con los servicios de la API
    [episteID, doi, pmid] = line.split('\t') # episteID, doi, pmid
    res_parser = parser.parse(doi)
    res_scopus = get_scopus_ref(doi)
    res_pubmed = []
    try:
        res_pubmed = getReferenceInfo(getRefID(pmid))
    except:
        pass
    if n == 1:
        print(str(res_parser) + "\n")
        print(str(res_scopus) + "\n")
        print(str(res_pubmed) + "\n")
    #imprimir a archivo nuevo llamado input_grafo.txt
    j = {
        "title": res_parser["title"] or res_scopus.get("title"),
        "authors": res_parser["authors"] or res_scopus.get("authors"),
        "abstract": res_parser["abstract"] or res_scopus.get("abstract"),
        "ids": {
            "doi": doi,
            "pmid": pmid,
            "episteId": episteID
        },
        "keywords": res_parser["keywords"] or res_scopus.get("keywords"),
        "publication_info": {
            "issue": res_parser["publication_info"]["issue"] or res_scopus.get("publication_info")["issue"],
            "journal": res_parser["publication_info"]["journal"] or res_scopus.get("publication_info")["journal"],
            "year": res_parser["publication_info"]["year"] or res_scopus.get("publication_info")["year"],
            "volume": res_parser["publication_info"]["volume"] or res_scopus.get("publication_info")["volume"],
            "pages": res_parser["publication_info"]["pages"] or res_scopus.get("publication_info")["pages"]
        } if res_scopus.get("publication_info") else res_parser["publication_info"],
        "citation": res_parser["citation"] or res_scopus.get("citation"),
        "references": res_parser["references"] + res_scopus.get("references", []) + res_pubmed
    }
    line = dump.readline()
    n +=1
    if n == 2:
        print(json.dumps(j))
        break




