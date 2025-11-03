from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import string,random


# Create your models here.


class Service(models.Model):
    name=models.CharField(max_length=100,unique=True,blank=True,null=True)
    location=models.CharField(max_length=100,unique=True,blank=True,null=True)
    total_members=models.PositiveIntegerField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    




class UserManager(BaseUserManager):

    def generate_random_password(self, length=10):
        """Generate a secure random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return "kelvin"

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")

        role = extra_fields.get("role", "PASTOR") 

        if role != "ADMIN" and not password:
            password = self.generate_random_password()

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        if role != "ADMIN":
            print(f"Generated password for {username}: {password}")

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        if password is None:
            raise ValueError("Superusers must have a password")

        return self.create_user(username, email, password, **extra_fields)


class CustomerUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        Pastor = "PASTOR", "Pastor"
        Helper = "HELPER", "Helper"
    first_name=models.CharField(max_length=150,null=True,blank=True)
    last_name=models.CharField(max_length=150,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    username=models.CharField(max_length=150,null=True,blank=True,unique=True)

    service=models.ForeignKey(Service,on_delete=models.SET_NULL,null=True,blank=True)
    role = models.CharField(max_length=10,choices=Role.choices,default=Role.Pastor)
    phone_number=models.CharField(max_length=100,unique=True,blank=True,null=True)
    profile_picture=models.ImageField(upload_to="profile_pictures",null=True,blank=True)
    password_changed=models.BooleanField(default=False)
    last_login=models.DateTimeField(auto_now=True,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

    objects=UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name',"last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def __str__(self):
        return self.full_name


