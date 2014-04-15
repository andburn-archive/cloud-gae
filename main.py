#!/usr/bin/env python

import ConfigParser

import webapp2

from google.appengine.api import users

import app.models
import app.helpers

# get configuratoin information
config = app.helpers.Configuration('app.config')
# TODO need to set actions in hash ? + reflection


##----- Request Handlers -----##

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Hello, ' + user.nickname() + ', '
                + '<a href="' + users.create_logout_url('/') + '">Sign Out</a>')
        else:
            self.redirect(users.create_login_url(self.request.uri))
    # end : get
# end : MainHandler

class GetLogin(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<iframe src=\"" +
                config.apphost + "userlogin\"" +
                " style=\"border: 0\" width=\"530\" heig" +
                "ht=\"650\" frameborder=\"0\" scrolling=\"no\"></iframe>")
    # end : get
# end : GetLogin


# NOTE handles user login and subsequent output
class UserLogin(webapp2.RequestHandler):
    def get(self):
        # self.response.out.write('User Login Page')
        user = users.get_current_user()
        if user:
            self.response.out.write('<h2>Hello, ' + user.nickname() + '</h2>')
            self.response.out.write('<h2>Login has been successful!!</h2>')
            self.response.out.write('<h2>Click the links on the Menu Bar above to begin....</h2>')
        else:
            self.redirect(users.create_login_url(self.request.uri))
    # end : get
# end : GetLogin

##----- WSGIApplication Route Handler -----##

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getlogin', GetLogin),
    ('/userlogin', UserLogin),
], debug=True)
