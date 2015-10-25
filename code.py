__author__ = 'Aronson1'

import os
import datetime
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db

def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__),'templates/'+templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)

class MainPage(webapp2.RequestHandler):
    def get(self):
        render_template(self, 'index.html', {})

class savePost(webapp2.RequestHandler):
    def post(self):
        question = Question()
        question.questionText = self.request.get('questionbox')
        question.timeSubmitted = datetime.datetime.now()
        question.put()
        render_template(self, 'index.html', {})



class Question(db.Model):
    questionText = db.StringProperty(multiline = True)
    timeSubmitted = db.DateTimeProperty()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/savePost', savePost)
], debug=True)