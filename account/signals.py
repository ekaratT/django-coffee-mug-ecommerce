from .models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def userprofile_post_save(sender, instance, created, **kwarge):
    user = instance
    if created:
        UserProfile.objects.create(user=user)
    else:
        # Modify existing user.
        # IF the user get deleted then profile will also be deleted automatically, no need signal.
        profile = UserProfile.objects.get(user=user)
        profile.save()