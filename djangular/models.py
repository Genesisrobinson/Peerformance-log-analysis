from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

class List(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
         return "List: {}".format(self.name)


class card(models.Model):
    title = models.CharField(max_length=100)
    description=models.TextField(blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
         return "card: {}".format(self.title)


