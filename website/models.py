from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    age = models.IntegerField()

class UserImages(models.Model):

    user = models.ForeignKey(User,on_delete = models.CASCADE)
    input_image = models.ImageField(upload_to=str(user))
    output_image_featureMap = models.ImageField(default = "")
    output_image_featureMap2 = models.ImageField(default = "")
    output_image_gradcam = models.ImageField(default = "")
    output_image_gradcam2 = models.ImageField(default = "")