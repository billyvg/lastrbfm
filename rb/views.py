# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def home(request):
	render_to_response('template.html')
	
@login_required
def user_page(request):
	user = request.user
	profile = UserProfile.objects.get(user=request.user)
	if profile.processed:
		display_for_user(request,user)
	else:
		process_user(user)
	
def display_for_user(request,user):
	