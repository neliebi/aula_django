import re
import requests

SOLR_URL = "http://localhost:8983/solr/proteins2"

def clearSolr():
	try:
		url = SOLR_URL + "/update?commit=true"
		headers = {'Content-type': 'text/xml'}
		data = '<delete><query>*:*</query></delete>'
		response = requests.post(url, headers=headers, data=data)
	except requests.exceptions.HTTPError as e:
		logging.error(e)

def addEntry(dataset):
	try:
		url = SOLR_URL + "/update?commit=true"
		headers = {'Content-type': 'text/xml'}
		data = "<add><doc>"
		for field,values in dataset.items():
			for value in values:
				value = str(value)
				if len(value.strip()) > 0:
					data += "<field name='" + field + "'>" + value + "</field>"
		data += "</doc></add>"

		response = requests.post(url, headers=headers, data=data)

		if response.status_code != 200:
			print(response.text)
			print(data)
	except requests.exceptions.HTTPError as e:
		print(e)

clearSolr()
with open('test.tab','r') as file:
	for line in file:
		row = line.split('\t')
		document = {}

		document['id'] = [row[0]]
		document['entry'] = [row[1]]

		document['protein_name'] = [row[2].split('(')[0]]
		document['protein_name'] += re.findall(r'\(([^()]+)\)',row[2])

		document['organism_name'] = [row[3].split('(')[0]]
		document['organism_name'] += re.findall(r'\(([^()]+)\)',row[3])

		document['gene_name'] = row[4].split()

		document['pfam'] = row[5].split(';')[:-1]
		document['pdb'] = row[6].split(';')[:-1]

		#Facet fields
		document['protein_name_ft'] = document['protein_name']
		document['organism_name_ft'] = document['organism_name']
		document['gene_name_ft'] = document['gene_name']
		document['pfam_ft'] = document['pfam']

		addEntry(document)