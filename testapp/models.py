from django.db import models
# Create your models here.
from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.
from django.db import models

class endpointavgtime(models.Model):
    endpoint=models.CharField(max_length=300)
    averageResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime: {}".format(self.endpoint)

class endpointavgtime1(models.Model):
    endpoint=models.CharField(max_length=300)
    averageResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime1: {}".format(self.endpoint)

class endpointavgtime2(models.Model):
    endpoint=models.CharField(max_length=300)
    averageResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime2: {}".format(self.endpoint)

class endpointavgtime3(models.Model):
    endpoint=models.CharField(max_length=300)
    averageResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime3: {}".format(self.endpoint)

class endpointavgtime4(models.Model):
    endpoint=models.CharField(max_length=300)
    averageResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime4: {}".format(self.endpoint)

class endpointavgtime5(models.Model):
    level=models.CharField(max_length=300)
    transactionCount=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime5: {}".format(self.level)

class endpointavgtime6(models.Model):
    endpoint=models.CharField(max_length=300)
    transactionCount=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime6: {}".format(self.endpoint)

class endpointavgtime7(models.Model):
    endpoint=models.CharField(max_length=300)
    transactionCount=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime7: {}".format(self.endpoint)


class auroraaggregate(models.Model):
    Agent=models.CharField(max_length=300)
    transcount=models.IntegerField(default=0)
    avgResponseTime=models.FloatField(default=0.0)
    medResponseTime=models.FloatField(default=0.0)
    maxResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "auroraaggregate: {}".format(self.Agent)

class auroraice(models.Model):
    Agent=models.CharField(max_length=300)
    transcount=models.IntegerField(default=0)
    avgResponseTime=models.FloatField(default=0.0)
    medResponseTime=models.FloatField(default=0.0)
    maxResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "auroraice: {}".format(self.Agent)

class auroratps(models.Model):
    Agent=models.CharField(max_length=300)
    transcount=models.IntegerField(default=0)
    avgResponseTime=models.FloatField(default=0.0)
    medResponseTime=models.FloatField(default=0.0)
    maxResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "auroratps: {}".format(self.Agent)

class auroraaris(models.Model):
    Agent=models.CharField(max_length=300)
    transcount=models.IntegerField(default=0)
    avgResponseTime=models.FloatField(default=0.0)
    medResponseTime=models.FloatField(default=0.0)
    maxResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "auroraaris: {}".format(self.Agent)

class auroradmp(models.Model):
    Agent=models.CharField(max_length=300)
    transcount=models.IntegerField(default=0)
    avgResponseTime=models.FloatField(default=0.0)
    medResponseTime=models.FloatField(default=0.0)
    maxResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "auroradmp: {}".format(self.Agent)

class auroramlife(models.Model):
    Agent=models.CharField(max_length=300)
    transcount=models.IntegerField(default=0)
    avgResponseTime=models.FloatField(default=0.0)
    medResponseTime=models.FloatField(default=0.0)
    maxResponseTime=models.FloatField(default=0.0)
    def __str__(self):
         return "auroramlife: {}".format(self.Agent)


class auroradistribution(models.Model):
    Agent=models.CharField(max_length=300)
    transcount = models.IntegerField(default=0)
    avgResponseTime = models.FloatField(default=0.0)
    medResponseTime = models.FloatField(default=0.0)
    maxResponseTime = models.FloatField(default=0.0)
    def __str__(self):
         return "hotel: {}".format(self.Agent)

class aurorasummary(models.Model):
    server=models.CharField(max_length=300)
    timeStamp = models.FloatField(default=0.0)
    def __str__(self):
         return "aurorasummary: {}".format(self.server)

class auroraerrorsummary(models.Model):
    errorType=models.CharField(max_length=300)
    s2aurora01p = models.FloatField(default=0.0)
    s2aurora03p = models.FloatField(default=0.0)
    s2aurora05p = models.FloatField(default=0.0)
    All = models.FloatField(default=0.0)
    def __str__(self):
         return "auroraerrorsummary: {}".format(self.server)

class auroramethodsummary(models.Model):
    errorType=models.CharField(max_length=300)
    s2aurora01p = models.FloatField(default=0.0)
    s2aurora03p = models.FloatField(default=0.0)
    s2aurora05p = models.FloatField(default=0.0)
    All = models.FloatField(default=0.0)
    def __str__(self):
         return "auroramethodsummary: {}".format(self.server)

class auroraerrormethodsummary(models.Model):
    errorType=models.CharField(max_length=300)
    method = models.CharField(max_length=300)
    s2aurora01p = models.FloatField(default=0.0)
    s2aurora03p = models.FloatField(default=0.0)
    s2aurora05p = models.FloatField(default=0.0)
    All = models.FloatField(default=0.0)
    def __str__(self):
         return "auroraerrormethodsummary: {}".format(self.server)

class testmodel(models.Model):
    Agent=models.CharField(max_length=300)
    def __str__(self):
         return "testmodel: {}".format(self.Agent)

class EnrollmentApplication(models.Model):
      reasons_for_childcare = MultiSelectField()


class VizInfoModel(models.Model):
    tog = MultiSelectField()

