#!/usr/bin/env python

import ConfigParser

import webapp2

import app.models
import app.helpers

# get configuratoin information
config = app.helpers.Configuration('app.config')

##----- Request Handlers -----##

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world! ' + config.appid)
# end : MainHandler


class CheckIt(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
# end : CheckIt

##----- WSGIApplication Route Handler -----##

application = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
