from django.db import models

# Create your models here.

class ProductModel(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=2550)
    

class ImageModel(models.Model):
    image = models.ImageField(upload_to="objects_detections/", blank=True, null=True)

