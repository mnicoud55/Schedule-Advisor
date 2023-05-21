from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import requests

BASE_URL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email','first_name','last_name','username','password1','password2','user_type', 'created')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email','first_name','last_name','username','password','user_type', 'created')

class SISSearchForm(forms.Form):
    
    # get list of class codes from SIS
    r = requests.get(BASE_URL + '&term=1228&page=1')
    SUBJECTS = [('--', '--Select--')]
    for subject in r.json()['subjects']:
        entry = (subject['subject'], subject['descr'])
        SUBJECTS.append(entry)

    YEARS = [
        ('22', '2022'),
        ('23', '2023'),
    ]

    TERMS = [
        ('1', 'J-Term'),
        ('2', 'Spring Term'),
        ('6', 'Summer Term'),
        ('8', 'Fall Term'),
    ]

    DAYS = [
        ('Mo', 'Monday'),
        ('Tu', 'Tuesday'),
        ('We', 'Wednesday'),
        ('Th', 'Thursday'),
        ('Fr', 'Friday'),
    ]
    
    class_subject = forms.CharField(label='Subject', max_length=4, widget=forms.Select(choices=SUBJECTS))
    class_year = forms.CharField(label='Year', max_length=2, widget=forms.Select(choices=YEARS), required=True)
    class_term = forms.CharField(label='Term', max_length=1, widget=forms.Select(choices=TERMS), required=True)
    class_units = forms.IntegerField(label='Units', required=False, min_value=0, max_value=9)
    check_full = forms.BooleanField(label='Search Full Classes?', required=False)
    days = forms.MultipleChoiceField(label='Meeting Days', required=False, widget=forms.CheckboxSelectMultiple, choices=DAYS)
    start_time = forms.CharField(label='Earliest Start Time', required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.CharField(label='Latest End Time', required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
"""

SIS search time_range format:

....&time_range=HH.MM,HH.MM

obviously, first time is beginning of range and second is end of range. any classes that start and end within that range
(endpoints included) will be returned in the search

SIS searh days format:

....&days=DdDd

must be exact match to meeting days for class, i.e. for Mon-Wed-Fri class, you would query "MoWeFr"

"""