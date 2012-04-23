# -*- encoding: utf-8 -*-
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import tweepy
import re

consumer_key = ""
consumer_secret = ""

key = ""
secret = ""


class MainHandler(webapp.RequestHandler):
	def get(self, name):
		if len(name) <= 0:
			temp = os.path.join(os.path.dirname(__file__),
						'templates/index.html')
			outstr = template.render(temp, 0)
			self.response.headers['Content-Type'] = 'text/html'
			self.response.out.write(outstr)
		elif len(name) > 20:
			error(self,414)
		elif re.search("resp=", self.request.url, flags=0) is not None:
			self.redirect("/"+name)
		else:
			response_card(self, name)

def response_card(self, name):
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(key, secret)
		
		api = tweepy.API(auth)
		if api.rate_limit_status()['remaining_hits'] > 0:
			user = api.get_user(name)
			temp = os.path.join(os.path.dirname(__file__), 'templates/card.html')
			if user.url is None:
				user_url = ''
			else:
				user_url = user.url
			outstr = template.render(temp, {'profile_image_url':user.profile_image_url.replace('_normal', '_reasonably_small'),'screen_name': user.screen_name, 'name': user.name, 'description': user.description, 'location': user.location, 'url': user_url, 'statuses_count': user.statuses_count, 'followings_count': user.friends_count, 'followers_count': user.followers_count})
			self.response.headers['Content-Type'] = 'text/html'
			self.response.out.write(outstr)
		else:
			error(self,420)
	except tweepy.TweepError, e:
		error(self,400,e)
	except e:
		error(self,200,e)
		
def error(self,code,e=None):
	self.response.headers['Content-Type'] = 'text/html'
	if code == 414:
		self.response.out.write('414 - Request-URI Too Long')
	elif code == 420:
		self.response.out.write('420 - REST API Rate Limiting. Please try again later.')
	else:
		self.response.out.write(str(code) + ' - ' + str(e))
	self.response.set_status(code)
	
				
def main():
	application = webapp.WSGIApplication([('/(.*)', MainHandler)],                                      
                                     debug=True)
	run_wsgi_app(application)
if __name__ is '__main__':
	main()
