from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator



class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=500, blank=True)
    email = models.EmailField(max_length=30,blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    country = models.CharField(max_length=20,blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    company_name = models.CharField(max_length=30, blank=True)
    company_size= models.CharField(max_length=30, blank=True)
    avatar = models.ImageField()

class Keyword(models.Model):
    User = models.ForeignKey(Profile,on_delete=models.CASCADE)
    alert_name = models.CharField(max_length=200,blank=False)
    optional_keywords = models.TextField(max_length=200,  null=True)
    required_keywords = models.TextField(max_length=200, null=True)
    excluded_keywords = models.TextField(max_length=200, null=True)
    source_googleplus = models.BooleanField(default=0)
    source_twitter = models.BooleanField(default=0)


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
   Location=models.CharField(max_length=100)

   class Meta:
       db_table = 'PostUser'

class Post(models.Model):
   PostUser=models.ForeignKey(PostUser, on_delete=models.CASCADE)
   Keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
   StatusID = models.CharField(max_length=45)
   Content = models.TextField()
   CreatedAt = models.DateTimeField()
   ResharerCount = models.IntegerField()
   Sentiment=models.IntegerField(blank=True, null=True)


   def set_statusID(self,id):
       self.statusID=id
   def get_statusID(self):
       return self.statusID

   class Meta:
       db_table = 'Post'
class Resharer(models.Model):
   PostUser = models.ForeignKey(PostUser, on_delete=models.CASCADE)
   Post=models.ForeignKey(Post,on_delete=models.CASCADE)
   class Meta:
       db_table = 'Resharer'
