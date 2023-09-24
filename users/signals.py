from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
# To create the profile picture

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# To save profile picture
@receiver(post_save, sender= User)
def save_profile(sender, instance, **kwargs):
 instance.profile.save()

# signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Profile  # Adjust this import based on your UserProfile model

# @receiver(post_save, sender=User)
# def create_default_profile_image(sender, instance, created, **kwargs):
#     """
#     Create a default profile image for a new user.
#     """
#     if created:
#         # Check if the user already has a profile image
#         if not instance.userprofile.profile_picture:
#             from django.core.files import File
#             from django.conf import settings
#             import os

#             # Set the path to your default profile image
#             default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')

#             # Create a File object from the default image path
#             default_image = File(open(default_image_path, 'rb'))

#             # Assign the default image to the user's profile picture field
#             instance.profile.profile_picture.save('default.png', default_image, save=True)
