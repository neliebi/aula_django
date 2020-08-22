
from django.shortcuts import render

from django.http import HttpResponse
from website.models import *

# Create your views here.
def hello(request):
	return HttpResponse("<h1>Hello World</h1>")


def proteins(request):
	proteins = UniprotKb.objects.all()

	html = "<h1>Proteínas</h1>"

	html += "<ul>"
	for protein in proteins:
		html += "<li><a href='../protein/%s'>%s</a></li>" % (protein.accession,protein.accession)
	html += "</ul>" 

	return HttpResponse(html)

def protein(request, accession):
	if UniprotKb.objects.filter(accession=accession).count() > 0:
		entry = UniprotKb.objects.get(accession=accession)

		html = "<h1>%s</h1>" % entry.accession
		html += "<p>%s</p>" % entry.sequence

		html += "<b>Taxonomy:</b> <a href='../../taxonomy/%s'>%s</a><br>" % (entry.taxonomy.ncbi_id, entry.taxonomy)
		html += "<b>Gene:</b> <a href='../../gene/%s'>%s</a><br>" % (entry.gene.name, entry.gene)
		
		html += "<h2>Gene Ontology:</h2>"
		html += "<ul>"
		for go in entry.gos.all():
			html += "<li><a href='../../go/%s'>%s</a></li>" % (go.go_id,go)
		html += "</ul>"

		html += "<h2>Families:</h2>"
		html += "<ul>"
		for pfam in entry.pfam.all():
			html += "<li><a href='../../pfam/%s'>%s</a></li>" % (pfam.pfam_id,pfam)
		html += "</ul>"

		html += "<h2>Structure:</h2>"
		pdbs = PDB.objects.filter(uniprot__accession=accession)
		html += "<ul>"
		for pdb in pdbs:
			html += "<li><a href='../../pdb/%s'>%s</a></li>" % (pdb.accession,pdb)
		html += "</ul>"

		return HttpResponse(html)
	else:
		return HttpResponse("<h1>Protein not found</h1>")

def taxonomy(request, ncbi_id):
	if Taxonomy.objects.filter(ncbi_id=ncbi_id).count() > 0:
		taxon = Taxonomy.objects.get(ncbi_id=ncbi_id)

		html = "<h1>%s</h1>" % taxon

		html += "<h2>Proteins</h2>"
		proteins = UniprotKb.objects.filter(taxonomy__ncbi_id=ncbi_id)

		html += "<ul>"
		for protein in proteins:
			html += "<li><a href='../../protein/%s'>%s</a></li>" % (protein.accession,protein.accession)
		html += "</ul"

		return HttpResponse(html)
	else:
		return HttpResponse("<h1>Taxon not found</h1>")

def gene(request, gene_name):
	if Gene.objects.filter(name=gene_name).count() > 0:
		gene = Gene.objects.get(name=gene_name)

		html = "<h1>%s</h1>" % gene

		html += "<h2>Proteins</h2>"
		proteins = UniprotKb.objects.filter(gene__name=gene_name)

		html += "<ul>"
		for protein in proteins:
			html += "<li><a href='../../protein/%s'>%s</a></li>" % (protein.accession,protein.accession)
		html += "</ul"

		return HttpResponse(html)
	else:
		return HttpResponse("<h1>Gene not found</h1>")

def go(request, go_id):
	if GeneOntology.objects.filter(go_id=go_id).count() > 0:
		go = GeneOntology.objects.get(go_id=go_id)

		html = "<h1>%s</h1>" % go
		html += "<b>Name:</b> %s<br>" % go.name
		html += "<b>Type:</b> %s<br>" % go.get_go_type_display()
		html += "<b>Description:</b> %s<br>" % go.description

		html += "<h2>Proteins</h2>"
		proteins = UniprotKb.objects.filter(gos__go_id=go_id)

		html += "<ul>"
		for protein in proteins:
			html += "<li><a href='../../protein/%s'>%s</a></li>" % (protein.accession,protein.accession)
		html += "</ul"

		return HttpResponse(html)
	else:
		return HttpResponse("<h1>GO not found</h1>")

def pfam(request, pfam_id):
	if Pfam.objects.filter(pfam_id=pfam_id).count() > 0:
		entry = Pfam.objects.get(pfam_id=pfam_id)

		html = "<h1>%s</h1>" % entry

		html += "<h2>Proteins</h2>"
		proteins = UniprotKb.objects.filter(pfam__pfam_id=pfam_id)

		html += "<ul>"
		for protein in proteins:
			html += "<li><a href='../../protein/%s'>%s</a></li>" % (protein.accession,protein.accession)
		html += "</ul"

		return HttpResponse(html)
	else:
		return HttpResponse("<h1>GO not found</h1>")

def pdb(request, accession):
	if PDB.objects.filter(accession=accession).count() > 0:
		entry = PDB.objects.get(accession=accession)

		html = "<h1>%s</h1>" % entry
		html += "<b>Protein:</b> <a href='../../protein/%s'>%s</a><br>" % (entry.uniprot.accession, entry.uniprot)
		html += "<b>Method:</b> %s<br>" % entry.get_method_display()
		html += "<b>Resolution:</b> %s<br>" % entry.resolution
		
		return HttpResponse(html)
	else:
		return HttpResponse("<h1>PDB not found</h1>")

def error400(request, exception):
	return HttpResponse("Error 400!", status=400)

def error403(request, exception):
	return HttpResponse("Error 403!", status=403)

def error404(request, exception):
	return HttpResponse("Error 404!", status=404)

def error500(request):
	return HttpResponse("Error 500!", status=500)


