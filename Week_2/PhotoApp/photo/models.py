from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(blank = True, max_length=50)
    author = models.CharField(blank = True, max_length=50)
    image = models.ImageField(blank = True, null = True, upload_to='static/images')
    description = models.TextField(blank = True)
    price = models.IntegerField(blank = True)
