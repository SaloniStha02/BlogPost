from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from .manager import UserManager

class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()
    def soft_delete(self):
        self.is_deleted=True
        self.save()
    
    def restore(self):
        self.is_deleted=False
        self.save()

    class Meta:
        abstract = True


class NewUser(AbstractBaseUser,PermissionsMixin,SoftDelete):
    username = models.CharField(max_length=20,null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null= True)
    last_name = models.CharField(max_length=30,null=True)
    phone_no=models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=30)
    age= models.IntegerField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
    objects = UserManager()

    def __str__(self):
        return self.email

