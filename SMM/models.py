from __future__ import unicode_literals

from django.db.models.signals import post_delete
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.conf import settings


def image_directory_path(instance, filename):
    return (u'picture/{0}'.format(filename))


COMPANY_SIZE = [
    ('five', '5-10 employees'),
    ('ten', '10-25 employees'),
    ('twentyfive', '25-50 employees'),
    ('fifty', '50-100 employees'),
    ('morethan', '>100 employees'),
]

class Profile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500, blank=True)
    email = models.EmailField(max_length=30, blank=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    country = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    company_name = models.CharField(max_length=200, blank=False, null=True)
    company_size = models.CharField(max_length=256, choices=COMPANY_SIZE)
    profile_image = models.ImageField(
        upload_to='profile_image', blank=True, null=True, default='default_profile_image.png')

    class Meta:
        db_table = 'Profile'
    # profile_image = models.ImageField(
    # upload_to='profile_image', default='profile_image/default_profile_image.png'storage=image_storage, null=True, blank=True)
    # profile_image = models.ImageField(
    #     image_directory_path, storage=image_storage, blank=True, null=True)


class Keyword(models.Model):
    User = models.ForeignKey(Profile, on_delete=models.CASCADE)
    alert_name = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = 'Keyword'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class PostUser(models.Model):
    UserID = models.CharField(max_length=60)
    DisplayName = models.CharField(max_length=45)
    DisplayPicture = models.CharField(max_length=1024)

    class Meta:
        db_table = 'PostUser'


class Post(models.Model):
    PostUser = models.ForeignKey(PostUser, on_delete=models.CASCADE)
    Keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    StatusID = models.CharField(max_length=45)
    Content = models.TextField()
    CreatedAt = models.DateTimeField()
    Sentiment = models.IntegerField(blank=True, null=True)

    def set_statusID(self, id):
        self.statusID = id

    def get_statusID(self):
        return self.statusID

    class Meta:
        db_table = 'Post'
