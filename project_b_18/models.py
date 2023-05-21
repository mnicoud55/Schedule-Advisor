from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

class User(AbstractUser):
    USER_CHOICES = [
        ('S', 'Student'),
        ('A', 'Advisor'),
    ]
    APPROVAL_CHOICES = [
        ('U', 'Unsent'),
        ('N', 'NoResponse'),
        ('R', 'Rejected'),
        ('A', 'Approved'),
    ]
    user_type = models.CharField(max_length=1, choices=USER_CHOICES, default='S')
    created = models.BooleanField(default=False)
    approval_status = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='U') 
    students = models.ManyToManyField('self', symmetrical=False)
    schedule_term = models.CharField(max_length=4, default='1238')

    @property
    def is_instansiated(self):
        return self.created
    pass

    @property
    def cart(self):
        return self.class_set.all().values_list('class_nbr', flat=True)
    
    @property
    def cart_json(self):
        return self.class_set.all().values_list('json_raw', flat=True)
    
    @property
    def student_list(self):
        return self.students.all()

def class_default():
    return {
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
                        "bldg_has_coordinates":True,
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

class Class(models.Model):
    user = models.ManyToManyField(User)
    class_term = models.CharField(max_length=4, default="1228")
    class_nbr = models.IntegerField(default=16351)
    json_raw = models.JSONField(default=class_default)