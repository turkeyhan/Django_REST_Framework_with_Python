from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/images')
    description = models.TextField()
    price = models.IntegerField()
