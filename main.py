#!/usr/bin/env python

import webapp2

import app.models


##----- Request Handlers -----##

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world!')
# end : MainHandler


class CheckIt(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(app.models.PersonalDetails.info())
# end : CheckIt

##----- WSGIApplication Route Handler -----##

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/checkit', CheckIt)
], debug=True)
