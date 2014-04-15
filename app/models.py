from google.appengine.ext import db


class PersonalDetails(db.Model):
    uname = db.UserProperty()
    firstname = db.StringProperty(multiline=True)
    surname = db.StringProperty(multiline=True)
    address1 = db.StringProperty(multiline=True)
    address2 = db.StringProperty(multiline=True)
    town = db.StringProperty(multiline=True)
    county = db.StringProperty(multiline=True)
    phone = db.StringProperty(multiline=True)
    desc = db.StringProperty(multiline=True)
    googlelink = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
# end : PersonalDetails


class StoredToken(db.Model):
    user_email = db.StringProperty(required=True)
    session_token = db.StringProperty(required=True)
# end : StoredToken


class EventDetails(db.Model):
    author = db.UserProperty()
    eventname = db.StringProperty(multiline=True)
    description = db.StringProperty(multiline=True)
    date = db.StringProperty(multiline=True)
    location = db.StringProperty(multiline=True)
    location_cord1 = db.StringProperty(multiline=True)
    location_cord2 = db.StringProperty(multiline=True)
# end : EventDetails


class EventAtendees(db.Model):
    atendee = db.UserProperty()
    eventid = db.StringProperty(multiline=True)
    eventname = db.StringProperty(multiline=True)
    date = db.StringProperty(multiline=True)
    location = db.StringProperty(multiline=True)
# end : EventAtendees


class Comments(db.Model):
    author = db.UserProperty()
    eventid = db.StringProperty(multiline=True)
    comment = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    # end : Comments