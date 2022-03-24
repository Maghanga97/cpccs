import datetime
from .models import Incidents, Departments, Users, IncidentStatus, Feedback, AuthLevel, Logs
import django

def data(request):
	incidents = Incidents.objects.all()
	departments = Departments.objects.all()
	users = Users.objects.all()
	feedback = Feedback.objects.all()
	user_group = AuthLevel.objects.all()
	logs = Logs.objects.all()
	data = {
		'incidents': incidents,
		'departments': departments,
		'users': users,
		'feedback': feedback,
		'levels': user_group,
		'logs': logs, 
		'current_date': django.utils.timezone.now()
	}
	return data

