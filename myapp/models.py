from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
        full_name = models.CharField(max_length=100, blank=True)
        date_of_birth = models.DateField(null=True, blank=True)
        email = models.EmailField(unique=True)
        # Optional: Make email the unique identifier for login
        #USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['full_name']

        def __str__(self):
            return self.username
        
        class Meta:
            ordering = ['username']
            verbose_name = 'User'
            verbose_name_plural = 'Users'

    # Add any additional fields or methods you need for your user model
        
    # GENDER_CHOICES = [
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    # ]
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)