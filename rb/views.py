# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rb.models import UserProfile,Track
from rb.get_lfm_data import get_for_user
import simplejson as json
from django.template.context import RequestContext
from django.template.loader import get_template

def home(request):
	return render_to_response('index.html')
	t = get_template('index.html')
	html=t#.render()
	return HttpResponse(html)
	
def user_page(request):
	return user_page_ajax(request)
	
def user_page_ajax(request):
	username = request.GET.get('u')
	(profile,created) = UserProfile.objects.get_or_create(lfmusername=username)
	if not profile.processed:
		get_for_user(username)
	tracks=Track.objects.filter(artist__in=profile.artists.all())
	tracks_out = []
	[tracks_out.append({'artist':track.artist.name,'title':track.name}) for track in tracks]
	return HttpResponse(json.dumps(tracks_out),mimetype='application/javascript')