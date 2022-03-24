from django.shortcuts import render
from .models import Incidents, Departments, Users, IncidentStatus, Feedback, AuthLevel, Logs
from django.db import connection
from django.http import HttpResponseRedirect
from .generate_reference_number import generate_first_reference_number, generate_new_reference_number
import datetime
from .security import SESSION_KEY, hash_password, hash_phrase
from django.contrib import messages
from .utils import not_null, sendsms


def fetch_inserted_ref_no():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ref_no FROM incidents_incidents order by id desc")
        row = cursor.fetchone()
    return row


def insert_function(request):
    try:
        if request.method == 'POST':
            new_name = request.POST.get('name_of')
            new_mail = request.POST.get('email_of')
            new_phone = request.POST.get('phone_of')
            new_gender = request.POST.get('gender_details')
            new_incident_type = request.POST.get('incident_type')
            new_location = request.POST.get('location')
            new_subcounty = request.POST.get('subcounty')
            new_ward = request.POST.get('wards')
            new_incident = request.POST.get('description')
            dept_selected = request.POST.get('department')
            occurred_on = request.POST.get('occurrence-date')
            reported_on= datetime.datetime.now()
            due_on = reported_on + datetime.timedelta(days=3)
            if not_null(occurred_on):
                occurred_on = datetime.datetime.strptime(occurred_on, '%Y-%m-%d')
                date_of_incident = occurred_on
            else:
                date_of_incident=datetime.datetime.now()    
            status_load= IncidentStatus.objects.get(status_name='pending')
            department_insert= Departments.objects.get(department_name=dept_selected)
            inserted_ref_no = fetch_inserted_ref_no()
            dept_strip = dept_selected[: 3]
            try:
                generated_ref_no = generate_new_reference_number(inserted_ref_no, dept_strip)
            except Exception as er:
                generated_ref_no = generate_first_reference_number(dept_strip)

            db_inserter = Incidents(ref_no=generated_ref_no,
                                        name_of_complainant=new_name,
                                        incident_type=new_incident_type,
                                        location=new_location,
                                        department=department_insert,
                                        description=new_incident,
                                        gender =new_gender,
                                        subcounty=new_subcounty,
                                        email_of_complainant=new_mail,
                                        phone_no=new_phone,
                                        incident_occurrence_date=date_of_incident,
                                        wards=new_ward,
                                        due_on=due_on,
                                        status= status_load)
            db_inserter.save()
            if not_null(new_name):
                new_name = new_name
            else:
                new_name = 'Anonymous'
            event_log = f'An new incident has been submitted by {new_name}'
            new_log_event = Logs(event=event_log)
            new_log_event.save()
            msg = f"You have successfully submitted your incident, your reference number is {generated_ref_no}"
            #sendsms(new_phone, msg)
            messages.success(request, msg)
            return HttpResponseRedirect('/')
    except Exception as insert_error:
        messages.error(request, insert_error)
        return HttpResponseRedirect('/')


def add_department_back_end(request):
    try:
        if request.method =='POST':
            new_department = request.POST.get('department')
            new_role = request.POST.get('role')
            if not_null(new_department):
                insert_department = Departments(department_name=new_department.upper())
                insert_department.save()
                return HttpResponseRedirect(f'/add/{SESSION_KEY}')
            if not_null(new_role):
                insert_role = AuthLevel(name=new_role.lower())
                insert_role.save()
                return HttpResponseRedirect(f'/add-roles/{SESSION_KEY}')
    except Exception as department_error:
        messages.error(request, department_error)
        return HttpResponseRedirect(f'/add/{SESSION_KEY}')
    

def registration_back_end(request):
    if request.method == 'POST':
        new_user_name = request.POST.get('user_name')
        new_user_mail = request.POST.get('user_mail')
        user = request.POST.get('user')
        user = Users.objects.get(id=int(user))
        clicked_from = request.POST.get('clicked-from')
        new_user_department = request.POST.get('department')
        user_department= Departments.objects.get(department_name=new_user_department)
        new_user_pass = request.POST.get('user_pass')
        user_status= request.POST.get('group')
        user_group = AuthLevel.objects.get(name=user_status)
        if user_status=='department officer':
            user_status=False
        else:
            user_status=True
        generate_pass = hash_password(new_user_name, new_user_pass)
        register_user= Users(user_name=new_user_name,
                                   user_mail=new_user_mail,
                                   salt_value= hash_phrase(new_user_name),
                                   department= user_department,
                                   level = user_group,
                                   user_pass=generate_pass,
                                   is_admin=user_status)
        register_user.save()
        event_log = f"User {new_user_name} with {user_group.name} role has been added by {user.user_name}"
        new_log_event= Logs(event=event_log)
        new_log_event.save()
        return HttpResponseRedirect(f'/register/{user.id}/{clicked_from}/{SESSION_KEY}/')


def change_user(request):
        if request.method == 'POST':
            new_user_name = request.POST.get('user_name')
            admin_user = request.POST.get('admin')
            new_user_mail = request.POST.get('user_mail')
            new_user_department = request.POST.get('department')
            user_status= request.POST.get('admin_status')
            delete_user= request.POST.get('delete_user')
            change_user= Users.objects.filter(user_name= new_user_name)
            if delete_user == 'delete':
                change_user.delete()
            else:        
                if user_status=='admin':
                    user_status=True
                else:
                    user_status=False
                change_user.is_admin = user_status
                change_user.save()
            return HttpResponseRedirect('/admin-dashboard/{}/{}/'.format(admin_user, SESSION_KEY))


def assign_user_incident(request):
    try:
        if request.method == 'POST':
            incident_id= request.POST.get('incident_id')
            username= request.POST.get('user_assigned')
            get_user = request.POST.get('user')
            change_to_completed= request.POST.get('status')
            send_to_user= request.POST.get('external')
            user_feedback = request.POST.get('feedback')
            link_clicked = request.POST.get('link-from')
            user = Users.objects.get(id=int(get_user))
            new_assignment= Incidents.objects.get(id=int(incident_id))
            events = []
            try:
                if not_null(user_feedback):
                    feedback = Feedback(user=user, reply= user_feedback)
                    feedback.save()
                    feedback.incident.add(new_assignment)
                    in_progress = IncidentStatus.objects.get(status_name='in progress')
                    new_assignment.status = in_progress
                    new_assignment.save()
                    msg = "You have successfully submitted your feedback"
                    event_log = f"{user.user_name} submitted a feedback on incident, ref:{new_assignment.ref_no}"
                    events.append(event_log)
                if not_null(change_to_completed):
                    new_status = IncidentStatus.objects.get(status_name=change_to_completed)
                    new_assignment.status= new_status
                    new_assignment.save()
                    msg = "You changed the incident status to complete"
                    event_log = f"Incident with ref: {new_assignment.ref_no} was closed by {user.user_name}"
                    events.append(event_log)
                if not_null(username):
                    user_assigned= Users.objects.get(user_name= username)
                    new_status= IncidentStatus.objects.get(status_name='assigned')
                    new_assignment.assigned_to.add(user_assigned)
                    new_assignment.status = new_status
                    new_assignment.save()
                    msg = f"You have successfully assigned incident to {user_assigned.user_name}"
                    event_log = f"{user_assigned.user_name} was assigned incident with ref: {new_assignment.ref_no} by {user.user_name}"
                    events.append(event_log)                
                if not_null(send_to_user):
                    feedback = Feedback(user=user, reply= user_feedback)
                    feedback.save()
                    feedback.incident.add(new_assignment)
                    sendsms(new_assignment.phone_no, user_feedback )
                    event_log = f"{user.user_name} sent a feedback to the complainant"
                    events.append(event_log)
                    msg = "Your feedback has been sent"
                for event in events:
                    new_log_event= Logs(performed_by=user, event= event)
                    new_log_event.save()                    
                messages.success(request, msg)
                return HttpResponseRedirect(f'/{link_clicked}/{user.user_name}/{SESSION_KEY}')
            except Exception as no_action:    
                messages.error(request, "You did not perform any action")
                return HttpResponseRedirect(f'/{link_clicked}/{user.user_name}/{SESSION_KEY}')                                                      
    except Exception as insert_error:
        messages.error(request, insert_error +",Try again")
        return HttpResponseRedirect(f'/{link_clicked}/{user.user_name}/{SESSION_KEY}')

