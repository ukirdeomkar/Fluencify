from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user2')
    room_id = models.CharField(max_length=10)
    common_interest = models.TextField()
    matching_percentage = models.DecimalField(max_digits=5,decimal_places=2)


class Paragraph(models.Model):
    paratext = models.TextField()