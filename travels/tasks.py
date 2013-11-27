import sys
import pprint
import calendar
import time
import urllib2
import traceback

from hashlib import sha1
import hmac
import binascii
import os

from django.conf import settings

from celery import Celery

import requests

from travels.celery import app
import travels.social_networks as socials
from travels import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

@app.task
def post_to_facebook(user_facebook_id, access_token, cast_url, thumbnail_url, cast_title):
	# pass instead user_id and cast_id. The rest can be retrieved based on a User instance and a Cast instance
	# with the help of a SocialNetworks object.
	project_settings = models.Settings.objects.all()[0]

	message = 'I want to see positive change in my community, which is why I have just uploaded a report to Voices of Youth Maps. Share this report and help me spread the word. '
	
	description = project_settings.project_description

	caption = project_settings.project_title

	payload = {'access_token': access_token, 'link': cast_url, 'message' : message, 'picture' : thumbnail_url, 'name' : cast_title, 'description' : description, 'caption' : caption }

	r = requests.post('https://graph.facebook.com/' + user_facebook_id + '/feed', data=payload)
    
@app.task
def post_to_twitter(user_id, cast_guid, cast_url, access_token, oauth_token_secret):
	try:
		cast_url = "http://staging.unicef-gis.org/#!cast/42/"

		msg = "I have just uploaded a report to Voices of Youth Maps Share this report and help me spread the word: {0}".format(cast_url)
		status = percent_encode(msg)

		payload = { 'status' : msg  }

		oauth_consumer_key = settings.SOCIAL_AUTH_TWITTER_KEY
		oauth_nonce = "{0}-{1}".format(user_id, cast_guid)
		oauth_signature_method = 'HMAC-SHA1'
		oauth_timestamp = str(calendar.timegm(time.gmtime()))
		oauth_token = access_token
		oauth_version = '1.0'
		request_url = 'https://api.twitter.com/1.1/statuses/update.json'

		oauth_signature = create_signature(status, oauth_consumer_key, oauth_nonce, oauth_signature_method, oauth_timestamp, oauth_token, oauth_version, request_url, oauth_token_secret)

		print oauth_signature

		headers = { 'Authorization' : authorization_headers(oauth_consumer_key, oauth_nonce, oauth_signature, oauth_signature_method, oauth_timestamp, oauth_token, oauth_version) }

		print str(headers)

		r = requests.post(request_url, data=payload, headers=headers)

		print str(r.text)
	except Exception:
		print >> sys.stderr, sys.exc_info()[0]
		print >> traceback.print_exc()
 
def authorization_headers(oauth_consumer_key, oauth_nonce, oauth_signature, oauth_signature_method, oauth_timestamp, oauth_token, oauth_version):
	return "OAuth oauth_consumer_key=\"{0}\", oauth_nonce=\"{1}\", oauth_signature=\"{2}\", oauth_signature_method=\"{3}\", oauth_timestamp=\"{4}\", oauth_token=\"{5}\", oauth_version=\"{6}\"".format(oauth_consumer_key, oauth_nonce, oauth_signature, oauth_signature_method, oauth_timestamp, oauth_token, oauth_version)

def create_signature(status, oauth_consumer_key, oauth_nonce, oauth_signature_method, oauth_timestamp, oauth_token, oauth_version, request_url, oauth_token_secret):
	#As per: https://dev.twitter.com/docs/auth/creating-signature

	consumer_secret = settings.SOCIAL_AUTH_TWITTER_SECRET

	param_string = "oauth_consumer_key={0}&oauth_nonce={1}&oauth_signature_method={2}&oauth_timestamp={3}&oauth_token={4}&oauth_version={5}&status={6}".format(percent_encode(oauth_consumer_key), percent_encode(oauth_nonce), percent_encode(oauth_signature_method), percent_encode(oauth_timestamp), percent_encode(oauth_token), percent_encode(oauth_version), status)

	signature_base_string = "POST&{0}&{1}".format(percent_encode(request_url), percent_encode(param_string))

	signing_key = "{0}&{1}".format(percent_encode(consumer_secret), percent_encode(oauth_token_secret))

	hashed = hmac.new(signing_key, signature_base_string, sha1)

	# For some reason, the b2a_base64 method appends a '\n' char at the end of the binary sequence, so we strip it 
	# because it would lead to an invalid OAuth signature
	sign = percent_encode(binascii.b2a_base64(hashed.digest()).rstrip())

	return sign

def percent_encode(str_to_encode):
	return urllib2.quote(str_to_encode, "")
	
	