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
    


# 🌟 TRENDING FEATURE MODELS

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s post at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes

    
    def save(self, *args, **kwargs):
        # Before saving a new like, update the post's like count
        if not self.pk:  # If the like is new (not being updated)
            self.post.like_count += 1
            self.post.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrease the like count when a like is removed
        self.post.like_count -= 1
        self.post.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} liked post {self.post.id}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on Post {self.post.id}"
    

# models.py

from django.db import models
from django.conf import settings

class EmojiReaction(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)  # e.g., 😍, 😳
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'emoji')  # prevents duplicate reactions by same user



    

