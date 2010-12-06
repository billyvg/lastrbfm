from django.db import models
from django.contrib.auth.models import User

class AbstractContent(models.Model):
	objects = models.Manager()
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	class Meta:
		abstract = True
		app_label = 'rb'
		
class UserProfile(AbstractContent):
	user = models.ForeignKey(User,unique=True,null=True,blank=True)
	lfmusername=models.CharField(max_length=25)
	artists = models.ManyToManyField('Artist',blank=True)
	processed = models.DateTimeField(null=True,blank=True)
	pages_loaded = models.CharField(max_length=120,null=True,blank=True)
	
class Track(AbstractContent):
	name = models.CharField(max_length=100)
	artist = models.ForeignKey('Artist',related_name='tracks')
#	cover = models.BooleanField(null=True)
	
	
class Artist(AbstractContent):
	name = models.CharField(max_length=100)