from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.exceptions import ValidationError

# Validator for number
def maxnum(value):
    if len(str(value)) != 11:
        raise ValidationError('Number must be 11 digits')

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superusers must have is_superuser=True.')
        if not extra_fields.get('is_staff'):
            raise ValueError('Superusers must have is_staff=True.')
        if not extra_fields.get('is_active'):
            raise ValueError('Superusers must have is_active=True.')

        user = self.create_user(email, password)
        user.is_superuser = extra_fields['is_superuser']
        user.is_staff = extra_fields['is_staff']
        user.is_active = extra_fields['is_active']
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=50, blank=True)
    number = models.CharField(max_length=11, blank=True, validators=[maxnum])
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return f'{self.name}, {self.email}'
