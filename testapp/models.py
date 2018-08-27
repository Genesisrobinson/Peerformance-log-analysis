from django.db import models
# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

class endpointavgtime(models.Model):
    endpoint=models.CharField(max_length=300)
    time=models.FloatField(default=0.0)
    def __str__(self):
         return "endpointavgtime: {}".endpoint(self.name)
