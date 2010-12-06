'''
Created on Dec 5, 2010

@author: jburkhart
'''
from django_beanstalkd import beanstalk_job
from rb.get_lfm_data import handle_resp,get_page
from rb.models import UserProfile
import urllib2
try:
	import json
except ImportError:
	import simplejson as json
	
@beanstalk_job
def processpage(in_str):
	'''in_str will be a json serialized object of the following format
	{
		'uname':string,
		'page':int
	}
	'''
	data = json.loads(in_str)
	uname = data.get('uname')
	page = data.get('page')
	print 'processing %s'%page
	resp = get_page(uname,page=page)
	user = UserProfile.objects.get(lfmusername=uname)
	handle_resp(user,resp)
	
	

