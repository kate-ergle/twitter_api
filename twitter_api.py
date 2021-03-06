from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "3xH7hbgRNHjpfU7W3Y8OV4BEn"
CONSUMER_SECRET = "qlgrrfOZkVBuivYMDd6t71YjaIdcP5FW0EJCf3oQdZVnMJIaIx"

OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


def setup_oauth():
    #"""Authorize your app via identifier."""
	# Request token
	oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
	r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
	credentials = parse_qs(r.content)

	resource_owner_key = credentials.get('oauth_token')[0]
	resource_owner_secret = credentials.get('oauth_token_secret')[0]

	# Authorize
	authorize_url = AUTHORIZE_URL + resource_owner_key
	print 'Please go here and authorize: ' + authorize_url

	verifier = raw_input('Please input the verifier: ')
	oauth = OAuth1(CONSUMER_KEY,
					   client_secret=CONSUMER_SECRET,
					   resource_owner_key=resource_owner_key,
					   resource_owner_secret=resource_owner_secret,
					   verifier=verifier)


	# Finally, Obtain the Access Token
	r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
	credentials = parse_qs(r.content)
	token = credentials.get('oauth_token')[0]
	secret = credentials.get('oauth_token_secret')[0]

	return token, secret



def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth



if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        #print "OAUTH_TOKEN: " + token
        #print "OAUTH_TOKEN_SECRET: " + secret
        OAUTH_TOKEN_SECRET = secret
        OAUTH_TOKEN = token
        oauth = get_oauth()
        #r = requests.get(url="https://api.twitter.com/1.1/statuses/mentions_timeline.json", auth=oauth)
        r = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json", auth=oauth)
        #print len(r.json())
        api_json = r.json()
        for i in range(len(r.json())):
            api_json_curr = api_json[i]
            #print (api_json.keys())
            print (api_json_curr['created_at'] + ": " + api_json_curr['user']['screen_name'] + ": " + api_json_curr['text'])
    else:
        oauth = get_oauth()
        r = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json", auth=oauth)
        print r.json()
