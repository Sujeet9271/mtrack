from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=20, null=True)
    work = models.CharField(max_length=50, null=True)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile, created = Profile.objects.get_or_create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def __str__(self):
        return str(self.user)