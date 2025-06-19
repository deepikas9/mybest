from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    # Note: besties will be accessed via the BestieRequest model
    # You can add a convenience property or method to get accepted besties if you want.

    def besties(self):
        """Return queryset of accepted besties (both sent and received)."""
        from django.db.models import Q

        sent_accepted = BestieRequest.objects.filter(from_user=self, status='accepted').values_list('to_user', flat=True)
        received_accepted = BestieRequest.objects.filter(to_user=self, status='accepted').values_list('from_user', flat=True)
        user_ids = set(sent_accepted).union(set(received_accepted))
        return CustomUser.objects.filter(id__in=user_ids)
    
    def is_online(self):
        if self.last_seen:
            return timezone.now() - self.last_seen < timezone.timedelta(minutes=1)
        return False

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
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']  # Messages in chronological order

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message[:20]}"
    

