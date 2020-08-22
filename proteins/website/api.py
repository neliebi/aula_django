from django.http import HttpResponse, JsonResponse
from website.models import *

def protein_api(request, accession):
	if UniprotKb.objects.filter(accession=accession).count() > 0:
		entry = UniprotKb.objects.get(accession=accession)
		pdbs = PDB.objects.filter(uniprot__accession=accession)
		p_type = 'json'

		if 'type' in request.GET:
			if request.GET['type'] == 'txt':
				p_type = 'txt'

		if p_type == 'txt':
			txt = entry.accession + "\n" + entry.sequence + "\n"
			txt += "Taxonomy: "  + str(entry.taxonomy) + "\n"
			txt += "Gene: " + str(entry.gene) + "\n"
			
			txt += "Gene Ontology: " + str(list(map(str,entry.gos.all()))) + "\n"
			txt += "Families: " + str(list(map(str,entry.pfam.all()))) + "\n"
			
			txt += "Structures: " + str(list(map(str,pdbs)))

			return HttpResponse(txt, content_type="text/plain")
		else:
			json = {
				'accession': entry.accession,
				'taxonomy': str(entry.taxonomy),
				'gene': str(entry.gene),
				'gos': list(map(str,entry.gos.all())),
				'families': list(map(str,entry.pfam.all())),
				'structures': list(map(str,pdbs))
			}

			return JsonResponse(json)
	else:
		return HttpResponse("Protein not found!")

def protein_list_api(request):
	p_from = 0
	p_to = UniprotKb.objects.all().count()
	p_type = 'json'

	if 'from' in request.GET:
		if int(request.GET['from']) > 0 and int(request.GET['from']) <= p_to:
			p_from = request.GET['from']
	if 'to' in request.GET:
		if int(request.GET['to']) > p_from and int(request.GET['from']) <= p_to:
			p_to = request.GET['to']
	if 'type' in request.GET:
			if request.GET['type'] == 'tsv':
				p_type = 'tsv'
			elif request.GET['type'] == 'fasta':
				p_type = 'fasta'

	proteins = UniprotKb.objects.all()[p_from:p_to]

	if p_type == 'tsv':
		txt = "accession\tsequence\ttaxonomy\tgene\tgos\tfamilies\tpdbs" + "\n"
		for entry in proteins:
			pdbs = PDB.objects.filter(uniprot__accession=entry.accession)
			txt += entry.accession + "\t" + entry.sequence + "\t"
			txt += str(entry.taxonomy) + "\t"
			txt += str(entry.gene) + "\t"
			txt += str(list(map(str,entry.gos.all()))) + "\t"
			txt += str(list(map(str,entry.pfam.all()))) + "\t"
			txt += str(list(map(str,pdbs))) + "\n"

		return HttpResponse(txt, content_type="text/tab-separated-values")
	elif p_type == 'fasta':
		txt = ''
		for entry in proteins:
			sequence = entry.sequence.replace(" ","")
			
			txt += ">" + entry.accession + "\n"
			for i in range(0,len(sequence),70):
				txt += sequence[i:i+70] + "\n"
		return HttpResponse(txt, content_type="text/plain")
	else:
		json = {'proteins': []}
		for entry in proteins:
			pdbs = PDB.objects.filter(uniprot__accession=entry.accession)
			entry = {
				'accession': entry.accession,
				'taxonomy': str(entry.taxonomy),
				'gene': str(entry.gene),
				'gos': list(map(str,entry.gos.all())),
				'families': list(map(str,entry.pfam.all())),
				'structures': list(map(str,pdbs))
			}
			json['proteins'].append(entry)
		return JsonResponse(json)