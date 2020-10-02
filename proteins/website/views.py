from django.shortcuts import render

from django.http import HttpResponse
from website.models import *

def hello(request):
	proteins = UniprotKb.objects.all()

	context = {
		'proteins': proteins,
		'values': ["John", "Paul", "George", "Ringo"],
		'text': 'text'
	}
	
	return render(request,'base.html',context)

def test_filters(request):
	proteins = UniprotKb.objects.all()

	context = {
		'value': 5,
		'text': 'text',
		'phrase': "The Django Template Language",
		'html': '<b>bold</b>',
		'list': [1,2,3,4]
	}
	
	return render(request,'filters.html',context)

def proteins(request):
	proteins = UniprotKb.objects.all()
	context = {'proteins': proteins}

	return render(request,'proteins.html', context)

def clades(request):
	clades = Taxonomy.objects.all()
	context = {'clades': clades}

	return render(request,'clades.html', context)

def genes(request):
	genes = Gene.objects.all()
	context = {'genes': genes}

	return render(request,'genes.html', context)

def gos(request):
	gos = GeneOntology.objects.all()
	context = {'gos': gos}

	return render(request,'gos.html', context)

def families(request):
	families = Pfam.objects.all()
	context = {'families': families}

	return render(request,'families.html', context)

def structures(request):
	structures = PDB.objects.all()
	context = {'structures': structures}

	return render(request,'structures.html', context)

def protein(request, accession):

	if UniprotKb.objects.filter(accession=accession).count() > 0:
		entry = UniprotKb.objects.get(accession=accession)
		pdbs = PDB.objects.filter(uniprot__accession=accession)
		
		context = {
			'entry': entry,
			'pdbs': pdbs
		}

		return render(request,'protein.html', context)
	else:
		context = {
			'msg': 'Protein not found.'
		}
		return render(request,'notfound.html', context)

def taxonomy(request, ncbi_id):
	if Taxonomy.objects.filter(ncbi_id=ncbi_id).count() > 0:
		taxon = Taxonomy.objects.get(ncbi_id=ncbi_id)
		proteins = UniprotKb.objects.filter(taxonomy__ncbi_id=ncbi_id)
		context = {
			'taxon': taxon,
			'proteins': proteins
		}

		return render(request,'taxonomy.html', context)
	else:
		context = {'msg': 'Clade not found.'}
		return render(request,'notfound.html', context)

def gene(request, gene_name):
	if Gene.objects.filter(name=gene_name).count() > 0:
		gene = Gene.objects.get(name=gene_name)
		proteins = UniprotKb.objects.filter(gene__name=gene_name)

		context = {
			'gene': gene,
			'proteins': proteins
		}

		return render(request,'taxonomy.html', context)
	else:
		context = {'msg': 'Gene not found.'}
		return render(request,'notfound.html', context)

def go(request, go_id):
	if GeneOntology.objects.filter(go_id=go_id).count() > 0:
		go = GeneOntology.objects.get(go_id=go_id)
		proteins = UniprotKb.objects.filter(gos__go_id=go_id)

		context = {
			'go': go,
			'proteins': proteins
		}

		return render(request,'go.html', context)
	else:
		context = {'msg': 'GO not found.'}
		return render(request,'notfound.html', context)

def pfam(request, pfam_id):
	if Pfam.objects.filter(pfam_id=pfam_id).count() > 0:
		entry = Pfam.objects.get(pfam_id=pfam_id)
		proteins = UniprotKb.objects.filter(pfam__pfam_id=pfam_id)

		context = {
			'pfam': entry,
			'proteins': proteins
		}

		return render(request,'pfam.html', context)
	else:
		context = {'msg': 'Family not found.'}
		return render(request,'notfound.html', context)

def pdb(request, accession):
	if PDB.objects.filter(accession=accession).count() > 0:
		entry = PDB.objects.get(accession=accession)

		context = {
			'pdb': entry
		}

		return render(request,'pdb.html', context)
	else:
		context = {'msg': 'Structure not found.'}
		return render(request,'notfound.html', context)

def error400(request, exception):
	return render(request,'notfound.html', {'msg': 'Error 400!'})

def error403(request, exception):
	return render(request,'notfound.html', {'msg': 'Error 403!'})

def error404(request, exception):
	return render(request,'notfound.html', {'msg': 'Error 404!'})

def error500(request):
	return render(request,'notfound.html', {'msg': 'Error 500!'})


