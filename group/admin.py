from django.contrib import admin

from group.models import Group_Log, User_data

# Register your models here.
admin.site.register(User_data)
admin.site.register(Group_Log)