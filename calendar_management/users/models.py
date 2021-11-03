from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timeszone
from slugify import slugify

class User(AbstractBaseUser):
    class Role(models.IntegerChoices):
        MEMBER = 0
        LEADER = 5
    
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=120, unique=True)
    #avatars
    lastname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True)
    email = models.CharField(blank=True)
    role = models.IntegerField(choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=timeszone.now)
    updated_at = models.DateField(auto_now=True)

    @staticmethod
    def make_username(firstname, middlename, lastname):
        firstname = slugify(firstname)
        middlename_letters = [slugify(letter)[0] for letter in middlename.split()]
        lastname_letter = slugify(lastname)[0]
        base_username = firstname + str(lastname_letter) + str(''.join(middlename_letters))
        
        if not User.check_username_exist(base_username):
            return base_username
        
        number = 1
        while True:
            username = base_username + str(number)
            if not User.check_username_exist(username):
                return username
            number += 1

    def get_name(self):
        return self.lastname + ' ' + self.firstname

    def get_full_name(self):
        return self.lastname + ' ' + self.middlename + ' ' + self.firstnam

    def get_role(self):
        if self.role == self.Role.LEADER:
            return 'Leader'
        else:
            return 'Member'
    