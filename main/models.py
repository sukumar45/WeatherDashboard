from django.db import models
from datetime import datetime

# Create your models here.
class Visualization_demo(models.Model):
    title = models.CharField(max_length=200)
    published = models.DateTimeField("date published", default=datetime.now())
    content = models.TextField()
    

    def __str__(self):
        return self.title