from email.policy import default
from django.db import models
import jsonfield
# Create your models here.
class User_data(models.Model):
    username = models.CharField(max_length=100)
    groups = jsonfield.JSONField(default={"groups":[]})
    current_shares = jsonfield.JSONField(default={"shares":[]}) 
    def __str__(self):
        return self.username

class Group_Log(models.Model):
    def nameFile(instance,filename):
        return '/'.join(['images',filename])
    group_name = models.CharField(max_length=100)
    group_members = jsonfield.JSONField(default={"group_members":[]})
    group_data = jsonfield.JSONField(default={"group_data":[]})
    members_required = models.IntegerField(default=2)
    combined_shares = jsonfield.JSONField(default={"combined_shares":[]})
    image_url = models.CharField(max_length=300,default='')
    nonce = models.CharField(max_length=300,default='')
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)
    def __str__(self):
        return self.group_name


# class requests(models.Model):
#     id = models.CharField(max_length=100)
#     Approved = models.BooleanField(default=False)
#     Approvedby = models.CharField(max_length=100)
#     From = models.IntegerField(default=0)
#     OutNow = models.BooleanField(default=False)
#     OutTime = models.IntegerField(default=0)
#     ReqLocation = models.CharField(max_length=100)
#     ReqPurpose = models.CharField(max_length=100)
#     To = models.IntegerField(default=0)
#     email = models.CharField(max_length=200)
#     house = models.CharField(max_length=100)
#     isDaily = models.BooleanField(default=False)
#     name = models.CharField(max_length=100)
#     uid = models.CharField(max_length=100) 
#     def __str__(self):
#         return self.id