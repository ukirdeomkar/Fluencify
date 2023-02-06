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

class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user2')
    room_id = models.CharField(max_length=10)
    common_interest = models.TextField()
    matching_percentage = models.IntegerField()
