from django.db import models
from django.contrib.auth.models import User

class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}"

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
def save(self, *args, **kwargs):
    self.name = self.name.strip().lower()
    self.description = self.description.strip().lower()
    super().save(*args, **kwargs)