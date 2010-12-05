'''
Created on Nov 8, 2010

@author: jburkhart
'''
from settings import API
from rb.models import Artist,UserProfile
import subprocess
import datetime
try:
	import json
except ImportError:
	import simplejson as json
import time
import urllib2

def get_for_user(username):
	start = time.time()
	user = UserProfile.objects.get(lfmusername=username)
	response = get_resp(username=username)
	info = response['artists']['@attr']
	handleresp(user,response)
	procs = []
	for page in range(2,int(info.get('totalPages'))+1):
		procs.append(subprocess.Popen(["curl", "%s"%get_url(username,page=page)], shell=False, stdout=subprocess.PIPE))
		time.sleep(0.3)
	done = False
#	return procs
	while not done:
		done = check_done(procs)
		time.sleep(0.5)
		print 'WAITIN'
	for proc in procs:
		resp = proc.communicate()[0]
		if resp:
			p = json.loads(proc.communicate()[0])
			handleresp(user,p)
	user.processed = datetime.datetime.now()
	user.save()
	print 'THIS TOOK THIS LONG TO EXECUTE:',time.time()-start
	
def handleresp(user,resp):
	artists = resp['artists']['artist']
	for artist in artists:
		make_artist(user,artist)

def get_url(username,page=1):
	return 'http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key=%s&user=%s&format=json&page=%s'%(API,username,page)

def get_resp(username,page=1):
	print 'PAGENUMBER',page
	reply = urllib2.urlopen(get_url(username,page))
	return json.loads(reply.read())

def make_artist(user,artist):
	print artist.get('name')
	try:
		a = Artist.objects.get(name=artist.get('name'))
	except:
		a = Artist(name=artist.get('name'))
		a.save()
	user.artists.add(a)
	
def check_done(procs):
	return not None in [proc.poll() for proc in procs]
