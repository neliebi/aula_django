from django.db import models

# Create your models here.
class Queue(models.Model):
	job_id = models.CharField(unique=True, max_length=20, null=False, blank=False)
	status = models.IntegerField(default=0)
