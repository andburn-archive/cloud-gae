import time
import webapp2
import cgi
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template

import atom
import gdata.service

import app.globals
import app.models


class CalendarContacts(webapp2.RequestHandler):

    # Initialize some global variables we will use
    def __init__(self):
        super(CalendarContacts, self).__init__()
        # Stores the page's current user
        self.current_user = None
        # Stores the token_scope information
        self.token_scope = None
        # Stores the Google Data Client
        self.client = None
        # The one time use token value from the URL after the AuthSub redirect.
        self.token = None
        # Init local time - default date for new events
        localtime = time.localtime()
        self.todays_date = "%s-%s-%s" % (localtime[0], localtime[1], localtime[2])
    # end : init

    def post(self):
        event_status = 'not_created'
        event_link = None

        # Get the current user
        self.current_user = users.GetCurrentUser()

        # Manage our Authentication for the user
        self.ManageAuth()
        self.LookupToken()

        form = cgi.FieldStorage()

        attendee_list = []
        if form.has_key('event_attendees') and form['event_attendees'] is not None:
            if isinstance(form['event_attendees'], list):
                for attendee in form['event_attendees']:
                    attendee_list.append(attendee.value)
            else:
                attendee_list.append(form['event_attendees'].value)

        event = self.InsertEvent(form['event_title'].value,
                                 form['location'].value,
                                 form['event_description'].value,
                                 form['datepicker'].value,
                                 attendee_list)
        if event is not None:
            alt_link = event.GetAlternateLink().href
            self_link = event.GetSelfLink().href
            xml = self.FormatXML("%s" % event.ToString())
            event_status = 'created'

        ed = app.models.EventDetails()
        if users.get_current_user():
            ed.author = users.get_current_user()
        ed.eventname = form['event_title'].value
        ed.description = form['event_description'].value
        ed.date = form['datepicker'].value
        ed.location = form['location'].value
        ed.location_cord1 = form['lat'].value
        ed.location_cord2 = form['lng'].value
        ed.put()

        template_values = {
            'event_status': event_status,
            'alt_link': alt_link,
            'self_link': self_link,
            'xml': xml,
            'event_title': form['event_title'],
            'event_description': form['event_description'],
            'attendee_list': attendee_list,
            'app_name': app.globals.CONFIG.name,
            'css_link': app.globals.CSS_LINK
        }

        self.redirect('/ViewCal')
        template_file = 'process_event.html'
        path = os.path.join(os.path.dirname(__file__), 'main_templates',
                            template_file)
        self.response.out.write(template.render(path, template_values))
    # end : post

    def get(self):
        # Get the current user
        self.current_user = users.GetCurrentUser()

        if not self.current_user:
            template_values = {
                'login_url': users.CreateLoginURL(self.request.uri),
                'app_name': app.globals.CONFIG.name,
                'css_link': app.globals.CSS_LINK,
                'app_info': app.globals.APP_INFO
            }
            template_file = 'login.html'
        else:
            self.token = self.request.get('token')

            # Manage our Authentication for the user
            self.ManageAuth()
            self.LookupToken()

            if self.client.GetAuthSubToken() is not None:
                self.response.out.write('<div id="main">')
                self.feed_url = 'http://www.google.com/calendar/feeds/' \
                                'default/private/full'
                contacts = self.GetContacts()
                template_values = {
                    'current_user': self.current_user,
                    'logout_url': users.CreateLogoutURL(self.request.uri),
                    'contacts': contacts,
                    'app_name': app.globals.CONFIG.name,
                    'css_link': app.globals.CSS_LINK,
                    'todays_date': self.todays_date,
                    'sample_event_title': app.globals.SAMPLE_EVENT_TITLE,
                    'sample_event_description':
                        app.globals.SAMPLE_EVENT_DESCRIPTION
                }
                template_file = 'CreateEventForm.html'
            else:
                template_values = {
                    'authsub_url': self.client.GenerateAuthSubURL(
                        'http://%s/' % app.globals.CONFIG.apphost,
                        '%s %s' % ('http://www.google.com/m8/feeds/',
                                   'http://www.google.com/calendar/feeds'),
                        secure=False, session=True),
                    'app_name': app.globals.CONFIG.Name,
                    'css_link': app.globals.CSS_LINK
                }
                template_file = 'authorize_access.html'

        path = os.path.join(os.path.dirname(__file__), 'main_templates',
                            template_file)
        self.response.out.write(template.render(path, template_values))
    # end : get

    def ManageAuth(self):
        self.client = gdata.service.GDataService()
        gdata.alt.appengine.run_on_appengine(self.client)
        if self.token:
            # Upgrade to a session token and store the session token.
            self.UpgradeAndStoreToken()
    # end : ManageAuth

    def LookupToken(self):
        if self.current_user:
            stored_tokens = app.models.StoredToken.gql('WHERE user_email = :1',
                                            self.current_user.email())
            for token in stored_tokens:
                self.client.SetAuthSubToken(token.session_token)
                return
    # end : LookupToken

    def UpgradeAndStoreToken(self):
        self.client.SetAuthSubToken(self.token)
        self.client.UpgradeToSessionToken()
        if self.current_user:
            # Create a new token object for the data store which associates the
            # session token with the requested URL and the current user.
            new_token = app.models.StoredToken(user_email=self.current_user.email(),
                                    session_token=self.client.GetAuthSubToken())

            new_token.put()
            self.redirect('http://%s/' % app.globals.CONFIG.apphost)
    # end : UpgradeAndStoreToken

    def GetContacts(self):
        self.contacts_client = gdata.contacts.service.ContactsService()
        gdata.alt.appengine.run_on_appengine(self.contacts_client)
        self.contacts_client.SetAuthSubToken(self.client.GetAuthSubToken())
        contacts_feed = self.contacts_client.GetContactsFeed()
        contacts_dict = {}
        for contact in contacts_feed.entry:
            for email in contact.email:
                if email.primary and email.primary == 'true':
                    email.address
                    if contact.title.text is not None:
                        contacts_dict['%s - %s' %
                                      (contact.title.text, email.address)] = email.address
                    else:
                        contacts_dict[email.address] = email.address
        return contacts_dict
    # end : GetContacts

    def InsertEvent(self, title, location, description=None, start_time=None, attendees=[]):
        self.calendar_client = gdata.calendar.service.CalendarService()
        gdata.alt.appengine.run_on_appengine(self.calendar_client)
        self.calendar_client.SetAuthSubToken(self.client.GetAuthSubToken())

        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text=description)
        event.where.append(gdata.calendar.Where(value_string=location))
        event.when.append(gdata.calendar.When(start_time=start_time))

        for attendee in attendees:
            who = gdata.calendar.Who()
            who.email = attendee
            event.who.append(who)

        new_event = self.calendar_client.InsertEvent(event,
                                                     '/calendar/feeds/default/private/full')

        return new_event
    # end : InsertEvent

    def FormatXML(self, xmlstring):
        """Helper method to format XML into browser-friendly output."""
        output = xmlstring.replace('<', '&lt;')
        output = output.replace('>', '&gt;')
        output = output.replace('&gt;&lt;', '&gt;<br />&lt;')
        return output
    # end : FormatXML