import endpoints

__author__ = 'Aronson1'

package='TriviaGame'

import os
import datetime
import webapp2
import string
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import logging
import json


def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__),'templates/'+templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            userList = Use.all()
            userInQuestion = userList.filter("email =", user.email())
            result = userList.get()
            if result:
                render_template(self,'index.html',{})
            else:
                render_template(self,'login.html',{})
        else:
            url = users.create_login_url()
            render_template(self, 'getGmailLogin.html',{
                'url': url
            })

class savePost(webapp2.RequestHandler):
    def post(self):
        question = Question()
        question.questionText = self.request.get('questionbox')
        question.timeSubmitted = datetime.datetime.now()
        question.answer1 = self.request.get('answer1')
        question.answer2 = self.request.get('answer2')
        question.answer3 = self.request.get('answer3')
        question.answer4 = self.request.get('answer4')
        question.put()
        render_template(self, 'index.html', {})

class saveLogin(webapp2.RequestHandler):
    def post(self):
        mail = users.get_current_user().email()
        name = self.request.get('username')
        passw = self.request.get('password')
        if (mail == ''):
            errorString = 'Please use a valid username and password!'
            render_template(self,'login.html',{
                'error' : errorString
            })
        else:
            use = Use()
            logging.debug(users.get_current_user().email())
            use.email = mail
            use.username = name
            use.password = passw
            use.put()
            render_template(self,'index.html',{})




class Question(db.Model):
    questionText = db.StringProperty(multiline = True)
    answer1 = db.StringProperty(multiline=True)
    answer2 = db.StringProperty(multiline=True)
    answer3 = db.StringProperty(multiline=True)
    answer4 = db.StringProperty(multiline=True)
    timeSubmitted = db.DateTimeProperty()

class Use(db.Model):
    email = db.StringProperty()
    username = db.StringProperty()
    password = db.StringProperty()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/savePost', savePost),
    ('/saveLogin', saveLogin)
], debug=True)
