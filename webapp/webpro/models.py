from django.db import models

# Create your models here.
class Admin(models.Model):
    a_username = models.CharField(max_length=64)
    a_password = models.CharField(max_length=64)


class User(models.Model):
    u_username = models.CharField(max_length=64)
    u_password = models.CharField(max_length=64)
    u_phone = models.CharField(max_length=32)
    u_email = models.CharField(max_length=64)
    u_token = models.CharField(max_length=64)


class Jobinfo(models.Model):

    jobname = models.CharField(max_length=64)
    company_name = models.CharField(max_length=64)
    position = models.CharField(max_length=64)
    eduLevel = models.CharField(max_length=16)
    city_name = models.CharField(max_length=32)
    salary = models.CharField(max_length=32)
    update_time= models.CharField(max_length=32)
    workingExp = models.CharField(max_length=16)
    web_name = models.CharField(max_length=32)
    hash_id = models.CharField(max_length=128)
    job_require = models.CharField(max_length=2048)
    # class Meta:
    #     db_table = 'Jobinfo'

class CollecTable(models.Model):
    user_id = models.ForeignKey(User)
    jobinfo_id = models.ForeignKey(Jobinfo)

