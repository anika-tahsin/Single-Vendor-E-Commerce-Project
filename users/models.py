from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class customerUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    address = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=30)
    country = models.CharField(null=True, blank=True, max_length=30)
    
    mobile = models.CharField(null=True, blank=True, max_length=11)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="users/profile")
