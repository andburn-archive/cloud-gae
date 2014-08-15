import webapp2

from google.appengine.ext import db
from google.appengine.api import users

import app.globals


class AddEventIframe(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<iframe src="' + app.globals.CONFIG.apphost
                                + 'addevent" ' +
                                'style="border: 0" width="530" height="650" '
                                + 'frameborder="0" scrolling="no"></iframe>')
        # end : get
# end : AddEventIframe


class ViewEvent(webapp2.RequestHandler):

    def get(self):
        eventid = self.request.get('eventid')
        events = db.GqlQuery("SELECT * FROM EventDetails")
        for event in events:
            eid = event.key().id()
            if int(eid) == int(eventid):
                author = event.author
                eventname = event.eventname
                description = event.description
                date = event.date
                location = event.location
                coord1 = event.location_cord1
                coord2 = event.location_cord2

        # TODO: possible use before assignment here
        template_values = {
            'eid': eid,
            'author': author,
            'eventname': eventname,
            'description': description,
            'date': date,
            'location': location,
            'coord1': coord1,
            'coord2': coord2
        }
        template = app.globals.JINJA_ENVIRONMENT.get_template(
            'view_event_form.html')
        self.response.out.write(template.render(template_values))
        # end : get
# end : ViewEvent


class MyEvents(webapp2.RequestHandler):
    def get(self):
        created_events = db.GqlQuery(
            "SELECT * FROM EventDetails WHERE author = :1",
            users.get_current_user())

        attending_events = db.GqlQuery(
            "SELECT * FROM EventAtendees WHERE atendee = :1",
            users.get_current_user())

        template_values = {
            'created_events': created_events,
            'attending_events': attending_events
        }

        template = app.globals.JINJA_ENVIRONMENT.get_template('my_events.html')
        self.response.out.write(template.render(template_values))
        # end : get


# end : MyEvents


class ListEvents(webapp2.RequestHandler):
    def get(self):
        events = db.GqlQuery("SELECT * FROM EventDetails")

        template_values = {
            'events': events
        }

        template = app.globals.JINJA_ENVIRONMENT.get_template(
            'list_events.html')
        self.response.out.write(template.render(template_values))
        # end : get


# end : ListEvents


class SearchEvents(webapp2.RequestHandler):
    def get(self):
        # TODO: can we generalise this away from sport
        sport = self.request.get('sport')
        location = self.request.get('location')

        events = db.GqlQuery("SELECT * FROM EventDetails")
        search_results = []

        for event in events:
            descp_result = -1
            name_result = -1
            loc_result = -1
            if len(sport) > 0:
                descp_result = event.description.lower().find(sport.lower())
                name_result = event.eventname.lower().find(sport.lower())
            else:
                descp_result = -1
                name_result = -1

            if len(location) > 0:
                loc_result = event.location.lower().find(location.lower())
            else:
                loc_result = -1

            if descp_result != -1 or name_result != -1 or loc_result != -1:
                new_results = {
                    'name': event.eventname,
                    'date': event.date,
                    'location': event.location,
                    'key': event.key().id()
                }
                search_results.append(new_results)
        # end : for

        template_values = {
            'search_results': search_results,
            'results_found': False
        }

        if len(search_results) >= 0:
            template_values['results_found'] = True

        template = app.globals.JINJA_ENVIRONMENT.get_template(
            'search_events.html')
        self.response.out.write(template.render(template_values))
    # end : get
# end : SearchEvents