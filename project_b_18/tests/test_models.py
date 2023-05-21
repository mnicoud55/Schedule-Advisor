from django.test import TestCase
from project_b_18.models import User, Class
from django.urls import reverse
from django.contrib.auth import get_user_model

import requests

class ModelTestClass(TestCase):
    def test_user(self):
        #CustomUser = get_user_model()
        self.user = User.objects.create(user_type = 'S', created = True)
        #self.user = CustomUser.objects.create(first_name="Evan", last_name="Zimmerman", email="ewz9kg@virginia.edu", username=uname, password=pword, user_type=utype, created=True)
        self.assertTrue(isinstance(self.user, User))

    def test_one_plus_one_equals_two(self):
        self.assertEqual(1 + 1, 2)
    
    def test_CustomUser(self):
        CustomUser = get_user_model()
        self.user = CustomUser.objects.create(first_name="Evan", last_name="Zimmerman", email="ewz9kg@virginia.edu", username="Evan", password="password", user_type='S', created=True)
        self.assertTrue(isinstance(self.user, User))

    def test_class(self):
        self.course = Class.objects.create()
        self.assertTrue(isinstance(self.course, Class))

    def test_class_param(self):
        r = requests.get('https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1222&class_nbr=15402')
        self.course = Class.objects.create(class_term="1222", class_nbr=15402, json_raw=r.json())
        self.assertTrue(isinstance(self.course, Class))
