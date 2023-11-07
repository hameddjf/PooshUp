from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    # create normal user
    def create_user(self , first_name , last_name , username , email , password=None ):
        if not email:
            raise ValueError("user not have email")
        if not username:
            raise ValueError("user not have username")

        user = self.model(
            email = self.normalize_email(email),
            # make a normal email = small letter
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # create superuser
    def create_superuser(self , first_name , last_name , email , username , password=None ):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name ,
            last_name = last_name , 
            username =username , 
            password = password , 
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=50 , unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100 , unique=True , blank=False)
    password = models.CharField(max_length=200 , blank=False)
    confirm_password = models.CharField(max_length=200 , blank=False)
    phone_number = models.CharField(max_length=50 , unique=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' , 'first_name' , 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self , permission , obj=None):
        # if self.is_active and self.is_staff
        return self.is_admin
        # get all permissions

    def has_module_perms(self , add_label):
        return True