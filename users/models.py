from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomerUserManager


# Create your models here.
class customerUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    address = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=30)
    country = models.CharField(null=True, blank=True, max_length=30)
    
    mobile = models.CharField(null=True, blank=True, max_length=11)

    profile_picture = models.ImageField(null=True, blank=True, upload_to="users/user_profile")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = None

    objects = CustomerUserManager()


    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}".strip()


    
