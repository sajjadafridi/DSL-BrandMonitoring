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


class Keyword(models.Model):
    Text=models.CharField(max_length=45)
    Optional=models.CharField(default=None, blank=True, null=True,max_length=45)
    Required=models.CharField(default=None, blank=True, null=True,max_length=45)
    Excluded=models.CharField(default=None, blank=True, null=True,max_length=45)
    Userid = models.ForeignKey(Profile,on_delete=models.CASCADE)
    class Meta:
        order_with_respect_to = 'Userid'
        db_table = 'Keyword'


class PostUser(models.Model):
    UserID = models.CharField(max_length=60)
    DisplayName = models.CharField(max_length=45)
    DisplayImage = models.CharField(max_length=1024)
    TotalLikes= models.IntegerField(default=None, blank=True, null=True)
    TotalPosts=models.IntegerField(default=None, blank=True, null=True)
    FollowingCount=models.IntegerField(default=None, blank=True, null=True)
    FollowerCount=models.IntegerField(default=None, blank=True, null=True)
    PostReshareCount=models.IntegerField(default=None, blank=True, null=True)

class Post(models.Model):
    PostUser=models.ForeignKey(PostUser, on_delete=models.CASCADE)
    Keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    StatusID = models.CharField(max_length=45)
    Content = models.TextField()
    CreatedAt = models.DateTimeField()
    ResharerCount = models.IntegerField()
    Source = models.CharField(max_length=45)


class Resharer(models.Model):
    PostUser = models.ForeignKey(PostUser, on_delete=models.CASCADE)
    Post=models.ForeignKey(Post,on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
