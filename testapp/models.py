from django.db import models
# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

class endpointavgtime(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime: {}".format(self.endpoint)

class endpointavgtime1(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime1: {}".format(self.endpoint)

class endpointavgtime2(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime2: {}".format(self.endpoint)

class endpointavgtime3(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime3: {}".format(self.endpoint)

class endpointavgtime4(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime4: {}".format(self.endpoint)

class endpointavgtime5(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime5: {}".format(self.endpoint)

class List(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
         return "List: {}".format(self.name)
