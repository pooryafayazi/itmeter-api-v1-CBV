from django.db import models
from django.utils.translation import gettext_lazy as _ # This is used to translate the string to the user's language
from django.db.models.signals import post_save
from django.dispatch import receiver
from .users import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(blank=True , null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
    
    
@receiver(post_save, sender=User)
def save_profile(sender, instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk)

