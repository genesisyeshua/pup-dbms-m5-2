import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
    year = ndb.StringProperty(indexed=True)
    title1 = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty(indexed=True)
    thesis_author = ndb.KeyProperty(kind='useraccount',indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class useraccount(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    phone_num = ndb.IntegerProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):

        loggedUser = users.get_current_user()
        if loggedUser:
            user_key = ndb.Key('useraccount', loggedUser.user_id())
            user = user_key.get()
            # user = user_key.get().first_name

            if user:
                logout_url = users.create_logout_url('/login')
                template = JINJA_ENVIRONMENT.get_template('main.html')
                # link_text = 'Logout'
                template_values = {
                    'logout_url':logout_url
                    # 'user':user
                }
                self.response.write(template.render(template_values))
                
            else:
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render())
                # self.redirect('/register')
        else:
            login_url = users.create_login_url('/home')
            template = JINJA_ENVIRONMENT.get_template('login.html')
            template_values = {
                'login_url':login_url
                # 'reg_url':'/register'
            }
            self.response.write(template.render(template_values))

class loginPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url('/home')
        template = JINJA_ENVIRONMENT.get_template('login.html')
        template_values = {
                'login_url':login_url
            }
        self.response.write(template.render(template_values))

class RegisterPage(webapp2.RequestHandler):
    def get(self):
        
        loggedUser = users.get_current_user()
        if loggedUser:
            user_key = ndb.Key('useraccount', loggedUser.user_id())
            user = user_key.get()
            if user:
                self.redirect('/home')
            else:
                template = JINJA_ENVIRONMENT.get_template('register.html')
                # template_values = {
                #     'email':loggedUser.email()
                # }
                self.response.write(template.render())
        else:
            self.redirect(users.create_login_url('/register'))

    def post(self):
        user = useraccount(id=users.get_current_user().user_id())
        user.phone_num = int(self.request.get('phone_num'))
        user.email = self.request.get('email')
        user.first_name = self.request.get('first_name')
        user.last_name = self.request.get('last_name')
        user.put()
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result':'OK',
            'data':{
                'first_name':user.first_name,
                'last_name':user.last_name,
                'phone_num':user.phone_num,
                'id':users.get_current_user().user_id()
            }
        }
        self.response.out.write(json.dumps(response))
        self.redirect('/home')

class thesisAPI(webapp2.RequestHandler):
    def get(self):  
        allthesis = Thesis.query().order(-Thesis.year)
        thesis_list = []

        for t in allthesis:
            user = useraccount.query(useraccount.key == t.thesis_author)
            e = []
            for u in user:
                e.append({
                    'first_name':u.first_name,
                    'last_name':u.last_name
                })

            thesis_list.append({
                'year': t.year,
                'title1': t.title1,
                'abstract': t.abstract,
                'adviser': t.adviser,
                'section': t.section,
                'thesis_author': e
                })

        response = {
            'result': 'OK',
            'data': thesis_list
        }                           
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):

        thesis = Thesis()
        user = useraccount()
        loggedUser = users.get_current_user()
        user_key = ndb.Key('useraccount', loggedUser.user_id())
        # if users.get_current_user():
        #     thesis.section = users.get_current_user().email()

        thesis.year = self.request.get('year')
        thesis.title1 = self.request.get('title1')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.thesis_author = user_key
        thesis.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result': 'OK',
        'data': {
            'year': thesis.year,
            'title1': thesis.title1,
            'abstract': thesis.abstract,
            'adviser': thesis.adviser,
            'section': thesis.section,
            'thesis_author': user_key.get().first_name + ' ' + user_key.get().last_name
            }
        }
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/home', MainPageHandler),
    ('/login', loginPage),
    ('/register', RegisterPage),
    ('/api/thesis', thesisAPI)
], debug=True)
