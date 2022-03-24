from django.contrib import admin
from django.urls import path
from django.views.static import serve
# from django.conf.urls import url
from django.conf import settings
from incidents import views, db_insert

urlpatterns = [
    path('', views.incidents_view),
    path('insert_data/', db_insert.insert_function),
    path('register/<user>/<clicked_from>/<reg_session_key>/', views.registration_view),
    path('add/<dept_session_key>/', views.add_department),
    path('add-group/<session_key>/', views.add_group),
    path('register_backend/', db_insert.registration_back_end),
    path('admin-dashboard/<str:user>/<str:session>/', views.admin_view),
    path('add_backend/', db_insert.add_department_back_end),
    path('more-details/<user>/<incident>/<clicked_from>/', views.details, name='incident_details'),
    path('assign/', db_insert.assign_user_incident),
    path('incident/<reference>/', views.incident_pdf),
    path('report/', views.overall_report),
    path('view_user/<clicked_from>/<admin>/<user_id>/', views.edit_user_view),    
    path('edit/', db_insert.change_user),
    path('login/', views.login),
    path('main-dashboard/<user>/<session>/', views.main_admin_panel),
    path('manage-users/<link_tag>/<department>/<user_id>/', views.manage_users),
    path('incidents-list/<clicked_from>/<get_user>/<incident_status>/', views.incidents_list),
    path('department-incidents/<clicked_from>/<get_user>/<incident_status>/', views.department_incidents),
    path('incident-type/<get_user>/<incident_type>/<clicked_from>/', views.incidents_types),
    path('logs/', views.view_logs),
    path('department-incident-type/<get_user>/<incident_type>/<clicked_from>/', views.department_incidents_types),
    path('search-results/', views.search_results),
    # url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 

    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
