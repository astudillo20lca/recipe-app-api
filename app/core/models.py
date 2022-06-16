"""
database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """manager for users."""

    def create_user(self, email, password = None, **extra_field):
        """create, save and return a new user"""
        # same as create a new user
        if not email:
            raise ValueError('user must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_field)
        # encript the password
        user.set_password(password)
        # in case you need multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password,):
        """Create and return a super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user
        

class User(AbstractBaseUser,PermissionsMixin):
    """user in the system"""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    # assign the user manager
    objects = UserManager()
    # to use the email instead username
    USERNAME_FIELD = 'email'

