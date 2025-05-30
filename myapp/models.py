from django.db import models
from django.contrib.auth.models import AbstractUser
'''
class CustomUser(AbstractUser):
        full_name = models.CharField(max_length=100, blank=True)
        date_of_birth = models.DateField(null=True, blank=True)
        email = models.EmailField(unique=True)
        photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
        besties = models.ManyToManyField('self', symmetrical=False, related_name='bestie_of', blank=True)
        


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


class BestieRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_bestie_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_bestie_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # prevent duplicate requests

    def __str__(self):
        return f"{self.from_user} ➝ {self.to_user} ({self.status})"
'''

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # Note: besties will be accessed via the BestieRequest model
    # You can add a convenience property or method to get accepted besties if you want.

    def besties(self):
        """Return queryset of accepted besties (both sent and received)."""
        from django.db.models import Q

        sent_accepted = BestieRequest.objects.filter(from_user=self, status='accepted').values_list('to_user', flat=True)
        received_accepted = BestieRequest.objects.filter(to_user=self, status='accepted').values_list('from_user', flat=True)
        user_ids = set(sent_accepted).union(set(received_accepted))
        return CustomUser.objects.filter(id__in=user_ids)

    def __str__(self):
        return self.username


class BestieRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    ]

    from_user = models.ForeignKey(CustomUser, related_name='sent_bestie_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_bestie_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # Prevent duplicate requests
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} ➝ {self.to_user.username} ({self.status})"
