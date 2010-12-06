'''
Created on Nov 8, 2010

@author: jburkhart
'''
from django.conf import settings
from rb.models import Artist,UserProfile
from django_beanstalkd import BeanstalkClient
import datetime
try:
	import json
except ImportError:
	import simplejson as json
import time
import urllib2
API = settings.API
def get_for_user(username):
	user = UserProfile.objects.get(lfmusername=username)
	client = BeanstalkClient()
	response = get_page(username=username)
	info = response['artists']['@attr']
	handle_resp(user,response)
	for page in range(2,int(info.get('totalPages'))+1):
		job_data = {'uname':username,'page':page}
		client.call('rb.processpage',json.dumps(job_data))
	user.processed = datetime.datetime.now()
	user.save()
	
def handle_resp(user,resp):
	artists = resp['artists']['artist']
	for artist in artists:
		make_artist(user,artist)
	pagecomplete = int(resp['artists']['@attr']['page'])
	if not user.pages_loaded:
		user.pages_loaded = '0'*int(resp['artists']['@attr']['totalPages'])
	user.pages_loaded = user.pages_loaded[:pagecomplete-1]+'1'+user.pages_loaded[pagecomplete:]
	user.save()
	
def get_url(username,page=1):
	return 'http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key=%s&user=%s&format=json&page=%s'%(API,username,page)

def get_page(username,page=1):
	print 'PAGENUMBER',page
	reply = urllib2.urlopen(get_url(username,page))
	return json.loads(reply.read())

def make_artist(user,artist):
	try:
		print artist.get('name')
	except:
		print 'error!'
	try:
		a = Artist.objects.get(name=artist.get('name'))
	except:
		a = Artist(name=artist.get('name'))
		a.save()
	user.artists.add(a)
