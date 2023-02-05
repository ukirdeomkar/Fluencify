from django.db import models

# Create your models here.
from django.db import models

class Audio(models.Model):
    file = models.FileField(upload_to='audio/')