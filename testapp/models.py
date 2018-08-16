from django.db import models
# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

class folder(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
         return "folder: {}".format(self.name)
