from django.db import models

# Create your models here.
class Taxonomy(models.Model):
	ncbi_id = models.PositiveIntegerField(unique=True, null=False, blank=False)
	organism_name = models.CharField(max_length=100)

	def __str__(self):
		return "%s (%d)" % (self.organism_name, self.ncbi_id)


class Gene(models.Model):
	name = models.CharField(unique=True,max_length=20, null=False, blank=False)

	def __str__(self):
		return self.name


class GeneOntology(models.Model):
	TYPE_CHOICES = [(0,"Cellular location"),(1,"Biological process"),(2,"Molecular function")]

	go_id = models.CharField(unique=True,max_length=10,null=False,blank=False)
	name = models.CharField(max_length=50)
	description = models.TextField(null=True,blank=True)
	go_type = models.IntegerField(choices=TYPE_CHOICES,default=1)

	def __str__(self):
		return "%s [%s]" % (self.name, self.go_id)


class Pfam(models.Model):
	pfam_id = models.CharField(unique=True,max_length=7, null=False, blank=False)
	name = models.CharField(max_length=50)

	def __str__(self):
		return "%s (%s)" % (self.name, self.pfam_id)


class UniprotKb(models.Model):
	accession = models.CharField(unique=True,max_length=12, null=False, blank=False)
	sequence = models.TextField(max_length=99999, null=False, blank=False)
	length = models.PositiveIntegerField(null=True,blank=True)
	
	taxonomy = models.ForeignKey(Taxonomy,on_delete=models.CASCADE)
	gene = models.ForeignKey(Gene,on_delete=models.CASCADE)
	gos = models.ManyToManyField(GeneOntology)
	pfam = models.ManyToManyField(Pfam)

	def __str__(self):
		return self.accession

	def save(self, *args, **kwargs):
		self.length = len(self.sequence)
		super().save(*args, **kwargs)


class PDB(models.Model):
	METHOD_CHOICES = [(0,"NMR"),(1,"X-ray Crystallography"), (2,"Electron Cryo-microscopy")]

	accession = models.CharField(unique=True,max_length=4, null=False, blank=False)
	resolution = models.FloatField()
	method = models.IntegerField(choices=METHOD_CHOICES,default=1)
	
	uniprot = models.ForeignKey(UniprotKb,on_delete=models.CASCADE)

	def __str__(self):
		return self.accession

