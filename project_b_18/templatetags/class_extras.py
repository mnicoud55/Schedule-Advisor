from django import template
from django.contrib.auth import get_user_model
from project_b_18.models import Class

import requests

register = template.Library()
BASE_URL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'

@register.simple_tag
def update_class(strm, class_nbr):
	r = requests.get(BASE_URL + '&term=' + str(strm) + '&class_nbr=' + str(class_nbr))
	try:
		course = Class.objects.get(class_term=str(strm), class_nbr=class_nbr)
		course.json_raw = r.json()
	except Class.DoesNotExist:
		course = Class.objects.create(class_term=str(strm), class_nbr=class_nbr, json_raw=r.json())
	return course

"""
	 Mo Tu We Th Fr
 8AM 
 9AM 
10AM 
11AM
12PM
 1PM
 2PM
 3PM
 4PM
 5PM
 6PM
 7PM
 8PM
"""