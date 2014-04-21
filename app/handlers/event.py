import webapp2

from google.appengine.ext import db

import app.globals

class AddEventIframe(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<iframe src="' + app.globals.CONFIG.apphost + 'addevent" ' +
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
        template = app.globals.JINJA_ENVIRONMENT.get_template('view_event_form.html')
        self.response.out.write(template.render(template_values))
    # end : get
# end : ViewEvent


# class MyEvents(webapp2.RequestHandler):
#     def get(self):
#         self.response.out.write('<h2>Created Events</h2>')
#         ev = db.GqlQuery("SELECT * FROM EventDetails WHERE author = :1", users.get_current_user())
#         self.response.out.write('<table border=0 class=\"eventtext\" width=100%>')
#         self.response.out.write('<tr class=\"tblheader\"><th>Name</th><th>Event</th><th>Date</th><th>Location</th><th></th></tr>')
#         for event in ev:
#             self.response.out.write('<tr>')
#             self.response.out.write('<td>%s</td>' % event.author)
#             self.response.out.write('<td>%s</td>' % event.eventname)
#             self.response.out.write('<td>%s</td>' % event.date)
#             self.response.out.write('<td>%s</td>' % event.location)
#             self.response.out.write('<td><a href=# onclick=\"CLoad(\'Event Viewer\',\'/viewevent?eventid=%s\')\">View</a></td>' % event.key().id())
#             self.response.out.write('</tr>')
#         self.response.out.write('</table>')
#
#         self.response.out.write('<hr>')
#         self.response.out.write('<h2>Attending Events</h2>')
#         events = db.GqlQuery("SELECT * FROM EventAtendees WHERE atendee = :1", users.get_current_user())
#         self.response.out.write('<table border=0 class=\"eventtext\" width=100%>')
#         self.response.out.write('<tr class=\"tblheader\"><th>Name</th><th>Event</th><th>Date</th><th>Location</th><th></th></tr>')
#         for event in events:
#             self.response.out.write('<tr>')
#             self.response.out.write('<td>%s</td>' % event.atendee)
#             self.response.out.write('<td>%s</td>' % event.eventname)
#             self.response.out.write('<td>%s</td>' % event.date)
#             self.response.out.write('<td>%s</td>' % event.location)
#             self.response.out.write('<td><a href=# onclick=\"CLoad(\'Event Viewer\',\'/viewevent?eventid=%s\')\">View</a></td>' % event.eventid)
#             self.response.out.write('</tr>')
#         self.response.out.write('</table>')
#     # end : get
# # end : MyEvents
#
#
# class ListEvents(webapp.RequestHandler):
#     def get(self):
#         events = db.GqlQuery("SELECT * FROM EventDetails")
#         self.response.out.write('<table border=0 class=\"eventtext\" width=100%>')
#         self.response.out.write('<tr class=\"tblheader\"><th>Event</th><th>Date</th><th>Location</th><th></th></tr>')
#         for event in events:
#             self.response.out.write('<tr>')
#             #self.response.out.write('<td>%s</td>' % event.key().id())
#             #self.response.out.write('<td>%s</td>' % event.author)
#             self.response.out.write('<td>%s</td>' % event.eventname)
#             #self.response.out.write('<td>%s</td>' % event.description)
#             self.response.out.write('<td>%s</td>' % event.date)
#             self.response.out.write('<td>%s</td>' % event.location)
#             #self.response.out.write('<td>%s</td>' % event.location_cord1)
#             #self.response.out.write('<td>%s</td>' % event.location_cord2)
#             #self.response.out.write('<td><a href=\"viewevent?eventid=%s\">View</a></td>' % event.key().id())
#             self.response.out.write('<td><a href=# onclick=\"CLoad(\'Event Viewer\',\'/viewevent?eventid=%s\')\">View</a></td>' % event.key().id())
#             self.response.out.write('</tr>')
#         self.response.out.write('</table>')
#     # end : get
# # end : ListEvents
#
#
# class SearchEvents(webapp2.RequestHandler):
#     def get(self):
#         sport = self.request.get('sport')
#         location = self.request.get('location')
#         events = db.GqlQuery("SELECT * FROM EventDetails")
#         self.response.out.write('<table border=0 class=\"eventtext\" width=100%>')
#         self.response.out.write('<tr class=\"tblheader\"><th>Event</th><th>Date</th><th>Location</th><th></th></tr>')
#         counter=0
#         for event in events:
#             res = -1
#             res1 = -1
#             res2 = -1
#             if len(sport) > 0:
#                 res = event.description.lower().find(sport.lower())
#                 res1 = event.eventname.lower().find(sport.lower())
#             else:
#                 res = -1
#                 res1 = -1
#
#             if len(location) > 0:
#                 res2 = event.location.lower().find(location.lower())
#             else:
#                 res2 = -1
#
#             if res != -1 or res1 != -1 or res2 != -1:
#                 counter=1
#                 self.response.out.write('<tr>')
#                 #self.response.out.write('<td>%s</td>' % event.key().id())
#                 #self.response.out.write('<td>%s</td>' % event.author)
#                 self.response.out.write('<td>%s</td>' % event.eventname)
#                 #self.response.out.write('<td>%s</td>' % event.description)
#                 self.response.out.write('<td>%s</td>' % event.date)
#                 self.response.out.write('<td>%s</td>' % event.location)
#                 #self.response.out.write('<td>%s</td>' % event.location_cord1)
#                 #self.response.out.write('<td>%s</td>' % event.location_cord2)
#                 #self.response.out.write('<td><a href=\"viewevent?eventid=%s\">View</a></td>' % event.key().id())
#                 self.response.out.write('<td><a href=# onclick=\"CLoad(\'Event Viewer\',\'/viewevent?eventid=%s\')\">View</a></td>' % event.key().id())
#                 self.response.out.write('</tr>')
#         self.response.out.write('</table>')
#         if counter == 0:
#             self.response.out.write('<h2 class=\"eventtext\">No Results!!</h2>')
#     # end : get
# # end : SearchEvents