from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login, authenticate

from .forms import CustomUserCreationForm, SISSearchForm
from .models import Class

import requests

CustomUser = get_user_model()
BASE_URL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'

def signup_page(request):
    return render(request, 'signup.html')

def signup(request):
    fname = request.POST.get("first_name", None)
    lname = request.POST.get("last_name", None)
    mail = request.POST.get("email", None)
    uname = request.POST.get("username", None)
    pword = request.POST.get("password", None)
    utype = request.POST.get("type", None)

    try:
        user = CustomUser.objects.get(email=mail)
        user.first_name = fname
        user.last_name = lname
        user.email = mail
        user.username = uname
        user.password = pword
        user.user_type = utype
        user.created = True
        user.save()
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create(first_name=fname, last_name=lname, email=mail, username=uname, password=pword, user_type=utype, created=True)
        user.save()

    login(request, user)

    return redirect('index')

def login_page(request):
    return render(request, 'login.html')

def log_in(request):
    uname = request.POST.get("usernameText", None)
    pword = request.POST.get("userPassword", None)
    try:
        user = CustomUser.objects.get(username=uname,password=pword)
    except CustomUser.DoesNotExist:
        return render(request, 'login.html')

    login(request, user)
    return redirect('index')

def search_page(request):
    form = SISSearchForm(request.POST)
    if form.is_valid():
        
        data = form.cleaned_data
        year = data['class_year']
        term = data['class_term']
        subj = data['class_subject']
        units = data['class_units']
        check_full = data['check_full']
        days = data['days']
        start_time = data['start_time']
        end_time = data['end_time']

        sis_url = BASE_URL + '&term=1' + year + term
        if subj != '--':
            sis_url += '&subject=' + subj
        if type(units) is int:
            sis_url += '&units=' + str(units)
        if not check_full:
            sis_url += '&enrl_stat=O'
        if len(days) > 0:
            sis_url += '&days='
            for d in days:
                sis_url += d
        if start_time and end_time:
            sis_url += '&time_range='
            sis_url += start_time.replace(':', '.') + ','
            sis_url += end_time.replace(':', '.')
        elif start_time:
            sis_url += '&time_range='
            sis_url += start_time.replace(':', '.') + ',23.59'
        elif end_time:
            sis_url += '&time_range='
            sis_url += '00.01,'
            sis_url += end_time.replace(':', '.')
        
        r = requests.get(sis_url + '&page=1')
        return render(request, 'search.html', {'form': form, 'results': r.json()})

    else:
        form = SISSearchForm()
        return render(request, 'search.html', {'form': form, 'results': {}})

def edit_schedule(request, strm, class_nbr):
    try:
        course = Class.objects.get(class_term=str(strm), class_nbr=class_nbr)
    except Class.DoesNotExist:
        r = requests.get(BASE_URL + '&term=' + str(strm) + '&class_nbr=' + str(class_nbr))
        course = Class.objects.create(class_term=str(strm), class_nbr=class_nbr, json_raw=r.json())
        course.save()

    # remove if course in user's schedule
    if request.user in course.user.all():
        course.user.remove(request.user)
        html = "<html><a class='btn btn-primary btn-lg btn-block' hx-post='/edit/" + str(strm) + "/" + str(class_nbr) + "/' hx-trigger='click' hx-swap='outerHTML'>Add to Schedule</a></html>"
    # add if course not in user's schedule
    else:
        course.user.add(request.user)
        html = "<html><a class='btn btn-danger btn-lg btn-block' hx-post='/edit/" + str(strm) + "/" + str(class_nbr) + "/' hx-trigger='click' hx-swap='outerHTML'>Remove from Schedule</a></html>"

    usr = request.user
    usr.approval_status = 'U'
    usr.save()
    return HttpResponse(html)

def schedule_page(request):
    student = request.user
    if student.approval_status == 'U':
        student.schedule_term = request.POST.get('term_select', default='1238')
        student.save()
    user_list = CustomUser.objects.all()
    return render(request, 'schedule.html', {'user_list': user_list, 'selected_term': student.schedule_term})

def view_schedule_page(request, uname):
    student = CustomUser.objects.get(username=uname)
    return render(request, 'view_schedule.html', {'student': student})

def send_schedule(request):
    try:
        advisor = CustomUser.objects.get(username=request.POST.get('advisors', False))
        student = request.user
        advisor.students.add(student)
        student.approval_status = 'N'
        student.save()
        advisor.save()
        return schedule_page(request)
    except:
        return schedule_page(request)
    

def respond_to_schedule(request, uname):
    if request.POST.get('approve', False) == 'approve':
        student = CustomUser.objects.get(username=uname)
        advisor = request.user
        student.approval_status = 'A'
        advisor.students.remove(student)
        student.save()
        advisor.save()
    elif request.POST.get('reject', False) == 'reject':
        student = CustomUser.objects.get(username=uname)
        advisor = request.user
        print(advisor.username)
        student.approval_status = 'R'
        advisor.students.remove(student)
        student.save()
        advisor.save()

    return redirect('advisor_schedules')

"""
{
    "index":1,
    "crse_id":"006852",
    "crse_offer_nbr":1,
    "strm":"1228",
    "session_code":"SRT",
    "session_descr":"Short Add",
    "class_section":"001",
    "location":"MAIN",
    "location_descr":"On Grounds",
    "start_dt":"08/23/2022",
    "end_dt":"12/06/2022",
    "class_stat":"A",
    "campus":"MAIN",
    "campus_descr":"Main Campus",
    "class_nbr":16351,
    "acad_career":"UGRD",
    "acad_career_descr":"Undergraduate",
    "component":"LEC",
    "subject":"CS",
    "subject_descr":"Computer Science",
    "catalog_nbr":"1010",
    "class_type":"E",
    "schedule_print":"Y",
    "acad_group":"ENGR",
    "instruction_mode":"P",
    "instruction_mode_descr":"In Person",
    "acad_org":"CS",
    "wait_tot":0,
    "wait_cap":199,
    "class_capacity":75,
    "enrollment_total":72,
    "enrollment_available":3,
    "descr":"Introduction to Information Technology",
    "rqmnt_designtn":"",
    "units":"3",
    "combined_section":"N",
    "enrl_stat":"O",
    "enrl_stat_descr":"Open",
    "topic":"",
    "instructors":[
        {
            "name":"Derrick Stone",
            "email":"djs6d@virginia.edu"
        }
    ],
    "section_type":"Lecture",
    "meetings":[
        {
            "days":"MoWe",
            "start_time":"17.00.00.000000-05:00",
            "end_time":"18.15.00.000000-05:00",
            "start_dt":"08/23/2022",
            "end_dt":"12/06/2022",
            "bldg_cd":"OLS",
            "bldg_has_coordinates":true,
            "facility_descr":"Olsson Hall 009",
            "room":"009",
            "facility_id":"OLS 009",
            "instructor":"Derrick Stone"
        }
    ],
    "crse_attr":"NCLC",
    "crse_attr_value":"NCLC-NOCOST",
    "reserve_caps":[]
}
What we wanna display:
*********************************************************
* {subject}{catalog_nbr} - {descr}        {units} units *
* {enrl_stat_descr} {enrollment_total}/{class_capacity} *
*                   {wait_tot}/{wait_cap}               *
*
*
*
*
*********************************************************
"""