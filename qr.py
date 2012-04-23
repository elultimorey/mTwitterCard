'''
Created on 19/04/2012

@author: jose
'''
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self, name):
        if len(name) > 0:
            temp = os.path.join(os.path.dirname(__file__), 'templates/qr.html')
            outstr = template.render(temp, {'http_host':os.environ['HTTP_HOST'], 'screen_name':name})
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(outstr)
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write('400 - Bad Request')
            self.response.set_status(400)
def main():
    application = webapp.WSGIApplication([('/qr/(.*)', MainHandler)],                                      
                                     debug=True)
    run_wsgi_app(application)
if __name__ is '__main__':
    main()