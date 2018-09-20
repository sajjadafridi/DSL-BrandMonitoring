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
    Userid = models.ForeignKey(Profile,on_delete=models.CASCADE)
    alert_name = models.CharField(max_length=200,blank=False)
    optional_keywords = models.TextField(max_length=200, blank=False)
    required_keywords = models.TextField(max_length=200, blank=False)
    excluded_keywords = models.TextField(max_length=200, blank=False)
    class Meta:
        order_with_respect_to = 'Userid'
        db_table = 'Keyword'
        # constraints = [
        #     models.CheckConstraint(models.Q(age__gte=18), 'age_gte_18'),
        # ]
# class Brand(ModelForm):
#     class Meta:
#         model = AlertMention
#         exclude = ['excluded_keywords','optional_keywords','required_keywords']
#
# class Anything(ModelForm):
#     model = AlertMention
#     fields = '__all__'



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class PostUser(models.Model):
   UserID = models.CharField(max_length=60)
   DisplayName = models.CharField(max_length=45)
   DisplayPicture = models.CharField(max_length=1024)
   TotalLikes= models.IntegerField()
   TotalPosts=models.IntegerField()
   FollowingCount=models.IntegerField()
   FollowerCount=models.IntegerField()
   PostReshareCount=models.IntegerField()

   class Meta:
       db_table = 'PostUser'

class Post(models.Model):
   PostUserID=models.ForeignKey(PostUser, on_delete=models.CASCADE)
   KeywordID = models.ForeignKey(Keyword, on_delete=models.CASCADE)
   StatusID = models.CharField(max_length=45)
   Content = models.TextField()
   CreatedAt = models.DateTimeField()
   ResharerCount = models.IntegerField()
   Source = models.CharField(max_length=45)
   Sentiment=models.IntegerField()

   class Meta:
       db_table = 'Post'


class Resharer(models.Model):
   PostUserID = models.ForeignKey(PostUser, on_delete=models.CASCADE)
   PostID=models.ForeignKey(Post,on_delete=models.CASCADE)
   class Meta:
       db_table = 'Resharer'