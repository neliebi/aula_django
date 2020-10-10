from django.shortcuts import render, redirect
import uuid
import stomp
from job.models import Queue
from proteins.settings import ACTIVEMQ_USER, ACTIVEMQ_PASW, ACTIVEMQ_HOST, ACTIVEMQ_PORT, ACTIVEMQ_DEST

# Create your views here.
def calculate(request):
	if request.method == 'POST' and request.FILES['myfile']:
		dpw = request.POST.get("select")
		#Read file
		file = request.FILES['myfile']
		data = file.read()

		#Generate Job ID
		job_id = uuid.uuid4().hex[:10].upper()
		data = job_id + "\n" + str(data)
		
		#Save job
		job = Queue(job_id=job_id)
		job.save()

		#Send message
		conn = stomp.Connection(host_and_ports = [(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
		conn.start()
		conn.connect(login=ACTIVEMQ_USER, passcode=ACTIVEMQ_PASW)
		conn.send(ACTIVEMQ_DEST, data, persistent='false')
		conn.disconnect()

		return redirect('/results/' + job_id)
	else:
		return render(request,'calculate.html', {})

def results(request, job_id):
	job = Queue.objects.get(job_id=job_id)
	position = Queue.objects.filter(status__gte=0).count()

	context = {'job': job, 'position': position}

	return render(request, 'results.html',context)