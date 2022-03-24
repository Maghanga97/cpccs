from django.shortcuts import render
from .models import Incidents, Departments, Users, IncidentStatus
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User


# def fetch_department_count():
# 		with connection.cursor() as cursor:
# 			cursor.execute("select count( distinct department) from pages_incidences")
# 			mydepartment=cursor.fetchall()
# 		return mydepartment

class FetchData:

	def __init__(self):
		self.user_fetch = Users.objects.all()
		self.department_fetch = Departments.objects.all()
		self.status_fetch = IncidentStatus.objects.all()
		self.incident_data = Incidents.objects.all()

	def create_list(self, string_input):
		data_list = string_input.split(',')
		return data_list

	def get_user_data(self, username):
		data_fetch= self.user_fetch.get(user_name=username)
		data_fetch= str(data_fetch)
		return self.create_list(data_fetch)

	def fetch_password(self,username):
		data_list= self.get_user_data(username)
		return data_list[2]

	def fetch_user(self, username):
		data_list= self.get_user_data(username)
		return data_list[0]

	def fetch_department_id_for_user(self, username):
		data_list= self.get_user_data(username)
		return int(data_list[1])

	def fetch_salt_value(self, username):
		data_list= self.get_user_data(username)
		return data_list[3]

	def fetch_admin_status(self, username):
		data_list= self.get_user_data(username)
		return data_list[4]

	def get_department(self, department):
		department_data= str(self.department_fetch.get(department_name=department))
		return self.create_list(department_data)

	def fetch_department_name(self, department):
	 	department_name= self.get_department(department)
	 	return department_name[1]

	def fetch_department_id(self, department):
		new_dept_id= self.get_department(department)
		return int(new_dept_id[0])

	def get_incident_status(self, name):
		get_status= str(self.status_fetch.get(status_name=name))
		return self.create_list(get_status)

	def fetch_status_id(self, name):
	 	status_id= self.get_incident_status(name)
	 	return int(status_id[0])

	def fetch_status_name(self, name):
	 	status_name= self.get_incident_status(name)
	 	return status_name[1]









def fetch_incident(reference):
	incident_fetch= Incidents.objects.get(ref_no=reference)
	data_fetch= str(incident_fetch)
	data_list= data_fetch.split(',')
	return data_list

def fetch_incident_with_id(incident_id):
	incident_fetch= Incidents.objects.get(id=incident_id)
	data_fetch= str(incident_fetch)
	data_list= data_fetch.split(',')
	return data_list

def fetch_incident_department(reference):
	incident_department=fetch_incident(reference)
	return int(incident_department[1])

def fetch_incident_department_with_id(id):
	incident_department=fetch_incident_with_id(id)
	return int(incident_department[1])

def fetch_incident_type_count():
	with connection.cursor() as cursor:
		cursor.execute("select count( distinct incident_type) from incidents_Incidents")
		myincident_type_count = cursor.fetchall()
	return myincident_type_count


def fetch_userdata(username):
	user_fetch = Users.objects.get(user_name=username)
	data_fetch= str(user_fetch)
	data_list = data_fetch.split(',')
	return data_list

def fetch_password(username):
	data_list= fetch_userdata(username)
	return data_list[2]

def fetch_user(username):
	data_list= fetch_userdata(username)
	return data_list[0]

def fetch_department_id_for_user(username):
	data_list= fetch_userdata(username)
	return int(data_list[1])

def fetch_salt_value(username):
	data_list= fetch_userdata(username)
	return data_list[3]

def fetch_admin_status(username):
	data_list= fetch_userdata(username)
	return data_list[4]


def fetch_salt():
    with connection.cursor() as cursor:
        cursor.execute("select salt_value from pages_users")
        mysalt= cursor.fetchone()
    return mysalt


def fetch_department_data(department):
	department_fetch = Departments.objects.get(department_name=department)
	data_fetch= str(department_fetch)
	data_list = data_fetch.split(',')
	return data_list

def fetch_status_data(name):
	status_fetch = IncidentStatus.objects.get(status_name=name)
	data_fetch= str(status_fetch)
	data_list = data_fetch.split(',')
	return data_list


def fetch_department_name(department):
 	department_name= fetch_department_data(department)
 	return department_name[1]

def fetch_department_id(department):
	new_dept_id= fetch_department_data(department)
	return int(new_dept_id[0])

def fetch_status_id(name):
 	status_id= fetch_status_data(name)
 	return int(status_id[0])

def fetch_status_name(name):
 	status_name= fetch_status_data(name)
 	return status_name[1]

 

