from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm , CustomUserChangeForm
from .models import Class

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username','first_name','last_name','user_type','created','cart','approval_status','student_list','schedule_term']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Class)