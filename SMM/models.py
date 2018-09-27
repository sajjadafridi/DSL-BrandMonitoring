from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
class Keyword(models.Model):
    User = models.ForeignKey(Profile,on_delete=models.CASCADE)
    alert_name = models.CharField(max_length=200,blank=False)
    optional_keywords = models.TextField(max_length=200,  null=True)
    required_keywords = models.TextField(max_length=200, null=True)
    excluded_keywords = models.TextField(max_length=200, null=True)
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
   TotalLikes= models.IntegerField(null=True)
   TotalPosts=models.IntegerField(null=True)
   FollowingCount=models.IntegerField(null=True)
   FollowerCount=models.IntegerField( null=True)
   PostReshareCount=models.IntegerField(null=True)

   class Meta:
       db_table = 'PostUser'

class Post(models.Model):
   PostUser=models.ForeignKey(PostUser, on_delete=models.CASCADE)
   Keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
   StatusID = models.CharField(max_length=45)
   Content = models.TextField()
   CreatedAt = models.DateTimeField()
   ResharerCount = models.IntegerField()
   Source = models.CharField(max_length=45)
   Sentiment=models.IntegerField(blank=True, null=True)

   class Meta:
       db_table = 'Post'
class Resharer(models.Model):
   PostUser = models.ForeignKey(PostUser, on_delete=models.CASCADE)
   Post=models.ForeignKey(Post,on_delete=models.CASCADE)
   class Meta:
       db_table = 'Resharer'
