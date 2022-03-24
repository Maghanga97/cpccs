import requests
from requests.structures import CaseInsensitiveDict
import json
from .models import Incidents, Departments, Users, IncidentStatus, Feedback, AuthLevel, Logs



def not_null(param):
    return param != "" and param != None

def sendsms(phone, message):
    url = "https://api.mobitechtechnologies.com/sms/sendsms"
    headers = CaseInsensitiveDict()
    headers["h_api_key"] = "123b08dcc32921eaf7c87d15e4fda2c31f808fa5ab6709d8e7fc3878b34593a7"
    headers["Content-Type"] = "application/json"
    data = {"mobile" : phone,"response_type": "json","sender_name":"23107","service_id" : 0,"message" : message}
    json_data = json.dumps(data)
    resp = requests.post(url, headers=headers, data=json_data)
    return(resp.status_code)
def initialize():
    try:
        pending= IncidentStatus(status_name='pending')
        completed = IncidentStatus(status_name= 'completed')
        assigned = IncidentStatus(status_name = 'assigned')
        in_progress = IncidentStatus(status_name = 'in progress')
        in_progress.save()
        pending.save()
        completed.save()
        assigned.save()
        water =  Departments(department_name='WATER AND IRRIGATION')
        finance =  Departments(department_name='FINANCE AND PLANNING')
        education =  Departments(department_name='EDUCATION AND LIBRARIES')
        health =  Departments(department_name='HEALTH SERVICES')
        youth =  Departments(department_name='YOUTH,GENDER,SPORT AND SOCIAL SERVICES')
        agriculture =  Departments(department_name='AGRICULTURE,LIVESTOCK AND FISHERIES')
        works =  Departments(department_name='PUBLIC WORKS, HOUSING AND INFRASTRUCTURE')
        lands =  Departments(department_name='LANDS, ENVIRONMENT AND NATURAL RESOURCES')
        trade =  Departments(department_name='TRADE, TOURISM AND COOPERATIVE DEVELOPMENT')
        service=  Departments(department_name='PUBLIC SERVICE AND ADMINISTRATION')
        mining =  Departments(department_name='PORTFOLIO OF MINING, INDUSTRIALISATION, ICT AND SPECIAL PROGRAMMES')
        agriculture.save()
        education.save()
        finance.save()
        health.save()
        lands.save()
        mining.save()
        service.save()
        works.save()
        trade.save()
        water.save()
        youth.save()
        super_admin = AuthLevel(name='super admin')
        super_admin.save()
        register_user= Users(user_name='admin',
                                           salt_value= hash_phrase('admin'),
                                           level = super_admin,
                                           user_pass=hash_password('admin', '1234'),
                                           is_admin=True)
        register_user.save()
    except Exception as initial_error:
        pass



