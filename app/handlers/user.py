import webapp2

from google.appengine.api import users

import app.globals
import app.models

import os;


class GetLogin(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<iframe src="' + app.globals.CONFIG.apphost + 'userlogin" ' +
                                'style="border: 0" width="530" height="650" '
                                + 'frameborder="0" scrolling="no"></iframe>')
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
            self.response.out.write('<h2>Click the links on the Menu Bar '
                                    + 'above to begin....</h2>')
        else:
            self.redirect(users.create_login_url(self.request.uri))
    # end : get
# end : GetLogin


class CheckLogin(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<iframe src="' + app.globals.CONFIG.apphost
                                + 'UserManagement" style="border: 0" '
                                + 'width="530" height="650" frameborder="0" '
                                + 'scrolling="no"></iframe>')
    # end : get
# end : CheckLogin


class UserManagement(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/register')
        else:
            self.redirect(users.create_login_url(self.request.uri))
    # end : get
# end : UserManagement


class GetRegistrationDetails(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = app.globals.JINJA_ENVIRONMENT.get_template('registration_form.html')
        self.response.out.write(template.render(template_values))
    # end : get
# end : GetRegistrationDetails


class SetRegistrationDetails(webapp2.RequestHandler):
    def post(self):
        pd = app.models.PersonalDetails()

        if users.get_current_user():
            pd.uname = users.get_current_user()

        pd.firstname = self.request.get('firstname')
        pd.surname = self.request.get('surname')
        pd.address1 = self.request.get('address1')
        pd.address2 = self.request.get('address2')
        pd.town = self.request.get('town')
        pd.county = self.request.get('county')
        pd.phone = self.request.get('phone')
        pd.desc = self.request.get('desc')
        pd.googlelink = self.request.get('callink')
        pd.put()
        self.response.out.write('<h2 align=center>Registration Complete!</h2>')
    # end : get
# end : SetRegistrationDetails
