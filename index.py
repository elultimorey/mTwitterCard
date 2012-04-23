# -*- encoding: utf-8 -*-
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import tweepy

class MainHandler(webapp.RequestHandler):
	formdata = '''<form method="post" action="/">
Introduce un nombre de usuario: <input type="text" name="resp"/><br />
<input type="submit"/>
</form>'''
	def get(self):
		temp = os.path.join(os.path.dirname(__file__),
					'templates/index.html')
		outstr = template.render(temp, 0)
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(outstr)
	def post(self):
		try:
			if tweepy.api.rate_limit_status()['remaining_hits'] > 0:
				user = tweepy.api.get_user(self.request.get('resp'))
				temp = os.path.join(os.path.dirname(__file__), 'templates/card.html')
				outstr = template.render(temp, {'profile_image_url':user.profile_image_url.replace('_normal', '_reasonably_small'),'screen_name': user.screen_name, 'name': user.name, 'description': user.description, 'location': user.location, 'url': user.url, 'statuses_count': user.statuses_count, 'followings_count': user.friends_count, 'followers_count': user.followers_count})
				self.response.headers['Content-Type'] = 'text/html'
				self.response.out.write(outstr)
			else:
				temp = os.path.join(os.path.dirname(__file__), 'templates/card_limit.html')
				outstr = template.render(temp, 0)
				self.response.headers['Content-Type'] = 'text/html'
				self.response.out.write(outstr)
		except:
			msg = 'jaja you are death'
		
def main():
	application = webapp.WSGIApplication(
										 [('/.*', MainHandler)],
										 debug=True)
	run_wsgi_app(application)
if __name__ is '__main__':
	main()
