from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class interestModel(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    interest = models.TextField()


class addtionalInfoModel(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    interest = models.TextField()
    age = models.IntegerField()
    fluency = models.IntegerField(null=True)