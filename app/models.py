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

    @staticmethod
    def info():
        return "<h1>Hi its me</h1>"

# end : PersonalDetails