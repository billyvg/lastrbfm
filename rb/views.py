# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rb.models import UserProfile,Track
from rb.get_lfm_data import get_for_user
from django.conf import settings
try:
	import json
except ImportError:
	import simplejson as json
from django.template.context import RequestContext
from django.template.loader import get_template

def home(request):
	return render_to_response('index.html')
	t = get_template('index.html')
	html=t#.render()
	return HttpResponse(html)
	
def user_page(request):
	try:
		username = request.GET.get('lfmusername')
		(profile,created) = UserProfile.objects.get_or_create(lfmusername=username)
		if not profile.processed:
			get_for_user(username)
		
		progess_str = '%s of %s pages of results processed... Reload the page in a few minutes for more results.'\
			%(profile.pages_loaded.count('1'),len(profile.pages_loaded))
		
		artists = list(profile.artists.all())
		tracks = Track.objects.filter(artist__in=artists).select_related('artist').order_by('artist__name')
		tracks_out = []
		[tracks_out.append({'artist':track.artist.name,'title':track.name}) for track in tracks]
		
		data_out = {'tracks':tracks_out,
				'username':username,
				'progress':progess_str}
	except Exception, e:
		f=open(settings.LOG_DIRECTORY+"viewlog","a")
		f.write(e+'\n')
		f.close()
	return HttpResponse(json.dumps(data_out),mimetype='application/javascript')
#	artists = [track.artist.name for track in tracks]
#	for 
