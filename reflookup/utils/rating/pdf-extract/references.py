from subprocess import check_output
import xml.etree.ElementTree as ET
import json

def pdf_extract_references(pdf):
    try:
        command = 'pdf-extract extract --references %s' % pdf
        output = check_output(command, shell=True)
        xml = ET.fromstring(output)
        xml_references = xml.findall('reference')
        references = [x.text for x in xml_references]
        return json.dumps(references)
    except:
        return ''
