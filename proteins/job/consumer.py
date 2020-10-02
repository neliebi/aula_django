
import os
import sys
import django

#Configuração para acessar nosso projeto por um script stand-alone
sys.path.append('/Users/neli/Dropbox/Aulas/django/teste/proteins/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proteins.settings")
django.setup()

import time
import stomp
from proteins.settings import ACTIVEMQ_USER, ACTIVEMQ_PASW, ACTIVEMQ_HOST, ACTIVEMQ_PORT, ACTIVEMQ_DEST
from job.models import *


def execute(job,data):
	#Processamento ficticio do dado
	#Etapa 1
	print("Filtrando...")
	job.status = 1
	job.save()
	time.sleep(10)

	#Etapa 2
	print("Treinando...")
	job.status = 2
	job.save()
	time.sleep(10)

	#Etapa 3
	print("Classificando...")
	job.status = 3
	job.save()
	time.sleep(10)

	print("Done...")
	job.status = 10
	job.save()

class MyListener(object): 
	
	def __init__(self, conn): 
		self.conn = conn
		self.job = None
	
	def on_error(self, headers, message): 
		print('received an error %s' % message) 

	def on_message(self, headers, message): 
		try:
			temp = message.split("\n")
			job_id = temp[0]
			data = temp[1:]
			
			self.job = Queue.objects.get(job_id=job_id)

			execute(self.job,data)
		except Exception as e:
			self.job.status = -1
			self.job.save()
			print(e)
		
conn = stomp.Connection(host_and_ports = [(ACTIVEMQ_HOST, ACTIVEMQ_PORT)]) 
conn.set_listener('', MyListener(conn)) 
conn.start() 
conn.connect(login=ACTIVEMQ_USER,passcode=ACTIVEMQ_PASW) 
conn.subscribe(id='stomp_listener', destination=ACTIVEMQ_DEST, ack='auto') 

print("Waiting for messages...") 
while 1: 
	time.sleep(1)

