#!/usr/bin/env python

import os
import jinja2
import webapp2

from google.appengine.api import users

import app.globals
import app.models
import app.helpers
import app.handlers.user
import app.handlers.event


# get configuration information
app.globals.CONFIG = app.helpers.Configuration('app.config')

# setup jinja2 environment
app.globals.JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__),
                     app.globals.CONFIG.template_dir)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# TODO need to set actions in hash ? + reflection
#   ie within the various handlers, hardcoded routes e.g. UserManagement


##----- Request Handlers -----##

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write('Hello, ' + user.nickname() + ', <a href="' +
                                users.create_logout_url('/') + '">Sign Out</a>')
        else:
            self.redirect(users.create_login_url(self.request.uri))
    # end : get
# end : MainHandler


##----- WSGIApplication Route Handler -----##

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getlogin', app.handlers.user.GetLogin),
    ('/userlogin', app.handlers.user.UserLogin),
    ('/checklogin', app.handlers.user.CheckLogin),
    ('/usermanagement', app.handlers.user.UserManagement),
    ('/sign', app.handlers.user.SetRegistrationDetails),
    ('/register', app.handlers.user.GetRegistrationDetails),
    ('/viewevent', app.handlers.event.ViewEvent),
    ('/myevents', app.handlers.event.MyEvents),
    ('/listevents', app.handlers.event.ListEvents),
    ('/searchevents', app.handlers.event.SearchEvents),
    ('/addevent', app.handlers.calendar.CalendarContacts)
], debug=True)
