'''
Created on Nov 8, 2010

@author: jburkhart
'''
import urllib2
import simplejson as json
from rb.models import Track,Artist

def get_all():
	resp = urllib2.urlopen('http://www.rockband.com/services.php/music/all-songs.json')
	resp = json.loads(resp.read())
	handle_resp(resp)
	
def handle_resp(resp):
	for track_data in resp:
		(track,created) = Track.objects.get_or_create(name=track_data.get('name'),artist = Artist.objects.get_or_create(name=track_data.get('artist'))[0])
		track.save()
