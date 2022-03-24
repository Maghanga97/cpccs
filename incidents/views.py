from .models import Incidents,  Departments, Users, IncidentStatus, Feedback, AuthLevel, Logs
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.core.paginator import Paginator
import io
from reportlab.pdfgen import canvas
from .security import authenticated, SESSION_KEY, hash_phrase, hash_password
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from .utils import not_null
import datetime
from pathlib import Path
import os
from django.db.models import Q
from weasyprint import HTML, CSS
import secrets
from django.shortcuts import render


def incidents_view(request):
    new_log_event = Logs(event="The incident page has been visited", event_type='page view', page='incidents')
    new_log_event.save()
    departments =  Departments.objects.all()
    incidents_context = {'departments': departments}
    return render(request, 'home.html', incidents_context)


def view_logs(request):
    logs = Logs.objects.all()
    return render(request, 'cpccs/super-admin/logs.html')


def add_department(request, dept_session_key=None):
    if dept_session_key == SESSION_KEY:
        return render(request, 'cpccs/super-admin/department-registration.html', {})
    else:
        return HttpResponse("You need authorization from a registered user")

def add_group(request, session_key=None):
    if session_key == SESSION_KEY:
        return render(request, 'cpccs/super-admin/add-roles.html', {})
    else:
        return HttpResponse("You need authorization from a registered user")
    

def registration_view(request,user, clicked_from, reg_session_key=None):
    if reg_session_key == SESSION_KEY:
        departments = Departments.objects.all()
        levels = AuthLevel.objects.all()
        get_user = Users.objects.get(id=int(user))
        if clicked_from == 'main-dashboard':
            return render(request, 'cpccs/super-admin/register.html', {'departments': departments, 'session': SESSION_KEY, 'levels':levels, 'user':get_user, 'link_tag': clicked_from})
        else:
            return render(request, 'cpccs/department-admin/register.html', {'departments': departments, 'session': SESSION_KEY, 'levels':levels, 'user': get_user, 'link_tag': clicked_from})
    else:
        return HttpResponse("You need authorization from a registered user")    

def login(request):
    try:
        if request.method== 'POST':
            requesting_user = request.POST.get('username').lower()
            requesting_user_password= request.POST.get('password')
            user_authentication= authenticated(requesting_user, requesting_user_password)
            try:
                if user_authentication == True:
                    user = Users.objects.get(user_name=requesting_user)
                    request.session[requesting_user] = requesting_user
                    if user.level.name == 'super admin' :
                        event_log = f"{user.user_name} logged into the main system dashboard"
                        new_log_event = Logs(performed_by=user, event=event_log)
                        new_log_event.save()
                        return HttpResponseRedirect(f'/main-dashboard/{requesting_user}/{SESSION_KEY}/')
                    else:
                        event_log = f"{user.user_name} logged into the {user.department.department_name} department dashboard"
                        new_log_event = Logs(performed_by=user, event=event_log)
                        new_log_event.save()
                        return HttpResponseRedirect(f'/admin-dashboard/{requesting_user}/{SESSION_KEY}/')                                            
                else:
                    messages.error(request, user_authentication)
                    return HttpResponseRedirect('/') 
            except Exception as login_error:
                messages.error(request, login_error)
                return HttpResponseRedirect('/')
    except Exception as first_login_error:
                messages.error(request, first_login_error)
                return HttpResponseRedirect('/')
    return render(request, 'cpccs/login.html', {})


def admin_view(request, user, session):
    if session == SESSION_KEY:
        get_user= Users.objects.get(user_name=user)
        get_department_id =get_user.department.id
        get_department =  Departments.objects.get(id=get_department_id)
        filtered_incident_data = Incidents.objects.filter(department=get_department)
        display_incidents = filtered_incident_data[:10]
        get_user_admin_status = get_user.is_admin
        pending= IncidentStatus.objects.get(status_name='pending')
        assigned= IncidentStatus.objects.get(status_name='assigned')
        completed= IncidentStatus.objects.get(status_name='completed')
        total_filtered_incidents = filtered_incident_data.count()
        pending_incidents = filtered_incident_data.filter(status=pending).count()
        number_of_incidents_completed = filtered_incident_data.filter(status=completed).count()
        number_of_incidents_assigned = filtered_incident_data.filter(status=assigned).count()
        incidents_assigned = filtered_incident_data.filter(status=assigned)
        incidents_pending = filtered_incident_data.filter(status=pending)
        completed_incidents = filtered_incident_data.filter(status=completed)
        incidents_assigned_to_user = filtered_incident_data.filter(status=assigned, assigned_to=get_user)
        display_incidents_assigned_to_user = incidents_assigned_to_user[:10]
        incidents_completed_by_user = filtered_incident_data.filter(status=completed, assigned_to=get_user)
        number_of_incidents_completed_by_user = filtered_incident_data.filter(status=completed, assigned_to=get_user).count()
        number_of_incidents_assigned_to_user= filtered_incident_data.filter(status=assigned, assigned_to=get_user).count()
        users =Users.objects.filter(department_id=get_department)
        number_of_users= users.count()
        admin_context={'user': get_user,
                        "link_tag": "admin-dashboard",
                        'user_details': get_user_admin_status,
                        'user_list': users,
                        'session' : SESSION_KEY, 
                        'pending': pending_incidents,
                        'completed': number_of_incidents_completed,
                        'incidents': display_incidents,
                        'assigned' : number_of_incidents_assigned,
                        'assigned_to_admin': incidents_assigned_to_user,
                        'incidents_count': total_filtered_incidents}
        user_context= {'user': get_user, 'assigned': number_of_incidents_assigned_to_user, 'link_tag': 'admin-dashboard', 
                        'session': SESSION_KEY,
                        'completed': number_of_incidents_completed_by_user, 
                        'incidents': incidents_assigned_to_user, 
                        'display_incidents': display_incidents_assigned_to_user }
                                                            
        if get_user_admin_status == True:
            event_log = f"{get_user.user_name} had access to the {get_user.department.department_name} department dashboard"
            new_log_event = Logs(performed_by=get_user, event=event_log)
            new_log_event.save()
            return render(request,'cpccs/department-admin/department-admin.html',admin_context) 
        else:
            event_log = f"{get_user.user_name} had access to the {get_user.department.department_name} department dashboard"
            new_log_event = Logs(performed_by=get_user, event=event_log)
            new_log_event.save()
            return render(request,'cpccs/officer/department.html',user_context)
    else:
        return HttpResponse("Login required")
  
def main_admin_panel(request, user, session):
    if session == SESSION_KEY:
        department = request.GET.get('department')
        search = request.GET.get('search')
        view_incidents = Incidents.objects.all()
        display_incidents = Incidents.objects.all()[:10]
        users = Users.objects.all()
        if not_null(department):
            view_incidents= view_incidents.filter(department_id=int(department))
            display_incidents = Incidents.objects.filter(department_id= int(department))[:10]
            users= users.filter(department_id=int(department))
        # if not_null(search):
        #     view_incidents = view_incidents.get(ref_no=search)
        #     department = view_incidents.department.id
        #     users = users.filter(department_id= department)
        assigned= IncidentStatus.objects.get(status_name='assigned')
        completed = IncidentStatus.objects.get(status_name= 'completed')
        pending = IncidentStatus.objects.get(status_name= 'pending')
        completed_incidents= view_incidents.filter(status=completed)
        assigned_incidents = view_incidents.filter(status=assigned)
        pending_incidents = view_incidents.filter(status=pending)
        completed_count = completed_incidents.count()
        pending_count = pending_incidents.count()
        user = Users.objects.get(user_name= user)
        assigned_count= assigned_incidents.count()
        count_incidents = view_incidents.count()
        departments =  Departments.objects.all()
        number_of_departments = departments.count()
        number_of_users= users.count()
        event_log = f"{user.user_name} had access to the main system dashboard"
        new_log_event = Logs(performed_by=user, event=event_log)
        new_log_event.save()
        return render(request, 'cpccs/super-admin/main.html',{'incidents': display_incidents,
                                                                    'count_incidents': count_incidents,
                                                                    'dep_count': number_of_departments,
                                                                    'departments': departments,
                                                                    'completed_count': completed_count,
                                                                    'pending_count': pending_count,
                                                                    'assigned_count' : assigned_count,
                                                                    'users': users,
                                                                    'user': user,
                                                                    'session': SESSION_KEY,
                                                                    'number_of_users': number_of_users})
    else:
        messages.error(request, 'Unauthorised access')
        return HttpResponseRedirect('/')


def details(request, clicked_from, user, incident):
    get_incident= incident
    get_user = user
    incident= Incidents.objects.get(id=int(get_incident))
    user = Users.objects.get(id=int(get_user))    
    department= incident.department.id
    get_users= Users.objects.filter(department_id=department)
    feedback = Feedback.objects.filter(incident=incident)
    if clicked_from == 'main-dashboard':
        event_log = f"{user.user_name} viewed incident with ref: {incident.ref_no}"
        new_log_event = Logs(performed_by=user, event=event_log)
        new_log_event.save()        
        return render(request, 'cpccs/super-admin/details.html', {'details': incident,'user': user, 'session': SESSION_KEY, 'feedback': feedback, 'users': get_users, 'status': incident.status.status_name, 'link_tag': clicked_from})
    else:    
        event_log = f"{user.user_name} viewed incident with ref: {incident.ref_no}"
        new_log_event = Logs(performed_by=user, event=event_log)
        new_log_event.save()        
        return render(request, 'cpccs/department-admin/details.html', {'details': incident,'user': user, 'session': SESSION_KEY, 'feedback': feedback, 'users': get_users, 'status': incident.status.status_name, 'link_tag': clicked_from})

def incidents_list(request, clicked_from, get_user, incident_status):
    status = IncidentStatus.objects.get(status_name = incident_status)
    incidents = Incidents.objects.filter(status = status)
    user = Users.objects.get(id=int(get_user))    
    return render(request, 'cpccs/super-admin/main-incidents.html', {'incidents': incidents,'user': user, 'session': SESSION_KEY, 'link_tag': clicked_from})

def incidents_types(request, clicked_from, get_user, incident_type):
    incidents = Incidents.objects.filter(incident_type = incident_type)
    user = Users.objects.get(id=int(get_user))    
    return render(request, 'cpccs/super-admin/main-incidents.html', {'incidents': incidents,'user': user, 'session': SESSION_KEY, 'link_tag': clicked_from})


def department_incidents_types(request, clicked_from, get_user, incident_type):
    user = Users.objects.get(id=int(get_user))
    department =  Departments.objects.get(id = int(user.department.id))    
    incidents = Incidents.objects.filter(incident_type = incident_type, department=department)
    return render(request, 'cpccs/department-admin/incidents.html', {'incidents': incidents,'user': user, 'session': SESSION_KEY, 'link_tag': clicked_from})


def department_incidents(request, clicked_from, get_user, incident_status):
    user = Users.objects.get(id=int(get_user))
    department =  Departments.objects.get(id = int(user.department.id))    
    status = IncidentStatus.objects.get(status_name = incident_status)
    incidents = Incidents.objects.filter(status = status, department=department)
    return render(request, 'cpccs/department-admin/incidents.html', {'incidents': incidents,'user': user, 'session': SESSION_KEY, 'link_tag': clicked_from})


def edit_user_view(request, admin, user_id, clicked_from):
    user = Users.objects.get(id=user_id)
    return render(request, 'cpccs/department-admin/edit-user.html', {'user': user, 'admin_user' : admin, 'link_tag': clicked_from})

def manage_users(request,link_tag, department, user_id):
    user = Users.objects.get(id=int(user_id))
    if department == "All":
        users = Users.objects.all()
        return render(request, 'cpccs/super-admin/all-users.html', {'users': users, 'user' : user, 'session': SESSION_KEY, 'link_tag': link_tag})
    else:
        users_department =  Departments.objects.get(id=int(department))
        users = Users.objects.filter(department=users_department)
        return render(request, 'cpccs/department-admin/manage-users.html', {'user' : user, 'users': users, 'session': SESSION_KEY, 'link_tag': link_tag})

def search_results(request):
        search_input = request.GET.get('search')
        clicked_from = request.GET.get('clicked-from')
        assigned_user = request.GET.get('user-assigned')
        user = request.GET.get('user-id')
        user = Users.objects.get(id=int(user))
        gender_of_complainant = request.GET.get('gender')
        reported_on = request.GET.get('reported-on')
        incident_type= request.GET.get('incident-type')
        processing_status = request.GET.get('status')
        subcounty = request.GET.get('subcounty')
        wards = request.GET.get('wards')
        results = []
        search_tag = []
        if not_null(search_input):
            search_input = search_input
        else:
            search_input = None
        if not_null(assigned_user):
            assigned_user = assigned_user
        else:
            assigned_user = None
        if not_null(reported_on):
            reported_on = datetime.datetime.strptime(reported_on, '%Y-%m-%d')
        else:
            reported_on=None
        if not_null(processing_status):
            status = IncidentStatus.objects.get(status_name=processing_status.lower())
        else:
            status=None
        if not_null(incident_type):
            incident_type = incident_type
        else:
            incident_type=None
        if not_null(subcounty):
            subcounty = subcounty
        else:
            subcounty=None
        if not_null(wards):
            wards = wards
        else:
            wards=None
        if clicked_from == 'main-dashboard':
            if assigned_user:
                search_result = Incidents.objects.filter(assigned_to__user_name=assigned_user)
                if search_input or reported_on or status or incident_type or subcounty:
                    search_result = search_result.filter(Q(ref_no=search_input) |  Q(name_of_complainant=search_input) | Q(incident_type=incident_type) | Q(wards=wards) | Q(phone_no=search_input) | Q(incident_occurrence_date=reported_on) | Q(status=status))
            else:
                search_result = Incidents.objects.filter(Q(ref_no=search_input) |  Q(name_of_complainant=search_input) | Q(incident_type=incident_type) | Q(wards=wards) | Q(phone_no=search_input) | Q(incident_occurrence_date=reported_on) | Q(status=status))
            return render(request, 'cpccs/super-admin/search-results.html', {'results': search_result, 'user' : user, 'link_tag': clicked_from, 'session': SESSION_KEY})
        else:
            department =  Departments.objects.get(id=user.department.id)
            department_incidents = Incidents.objects.filter(department=department)
            users = Users.objects.filter(department=department)
            if assigned_user:
                search_result = department_incidents.filter(assigned_to__user_name=assigned_user)
                if search_input or reported_on or status or incident_type or subcounty:
                    search_result = search_result.filter(Q(ref_no=search_input) |  Q(name_of_complainant=search_input) | Q(incident_type=incident_type) | Q(wards=wards) | Q(phone_no=search_input) | Q(incident_occurrence_date=reported_on) | Q(status=status))
            else:    
                search_result = department_incidents.filter(Q(incident_occurrence_date=reported_on) | Q(status=status) | Q(incident_type=incident_type) | Q(gender=search_input) | Q(ref_no=search_input) | Q(phone_no=search_input) | Q(name_of_complainant=search_input) | Q(wards=wards) | Q(subcounty=subcounty))
            return render(request, 'cpccs/department-admin/search-results.html', {'results': search_result, 'user_list': users, 'user' : user, 'link_tag': clicked_from, 'session': SESSION_KEY})


def incident_pdf(request, reference):
    html_template = get_template('cpccs/incident-report.html')
    incident = Incidents.objects.get(id=int(reference))
    context = {'incident': incident}
    html_template = html_template.render(context)
    pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()      
    server_response = HttpResponse(pdf_file, content_type='application/pdf')
    server_response['Content-Disposition'] = ' inline; attachment; filename="report.pdf"'
    return server_response


def overall_report(request):
    html_template = get_template('cpccs/general-report.html')
    incidents = Incidents.objects.all()
    context = {'incidents': incidents}
    html_template = html_template.render(context)
    pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()      
    server_response = HttpResponse(pdf_file, content_type='application/pdf')
    server_response['Content-Disposition'] = ' inline; attachment; filename="report.pdf"'
    return se