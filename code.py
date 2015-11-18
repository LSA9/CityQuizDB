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
import random


def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__),'templates/'+templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)

####################################################################################
# Creates the main page and checks for user authentication
####################################################################################
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

####################################################################################
# Takes a submitted question from the website and stores it in the database
####################################################################################
class savePost(webapp2.RequestHandler):
    def post(self):
        QT = self.request.get('questionbox')
        A1 = self.request.get('answer1')
        A2 = self.request.get('answer2')
        A3 = self.request.get('answer3')
        A4 = self.request.get('answer4')
        if (QT=='' or A1==''  or A2=='' or A3=='' or A4==''):
            render_template(self, 'index.html', {})
        else:
            question = Question()
            question.questionText = QT
            question.timeSubmitted = datetime.datetime.now()
            question.answer1 = A1
            question.answer2 = A2
            question.answer3 = A3
            question.answer4 = A4
            question.catagory = self.request.get('catagories')
            question.put()
            render_template(self, 'index.html', {})

####################################################################################
# Takes a created username and password from the website and stores it in the database
####################################################################################
class saveLogin(webapp2.RequestHandler):
    def post(self):
        mail = users.get_current_user().email()
        name = self.request.get('username')
        userList = Use.all()
        userList.filter("username =", name)
        passw = self.request.get('password')
        if userList.count()==1:
            invalidUsername = "Username already in use!"
            render_template(self,'login.html',{
                'error' : invalidUsername
            })
        else:
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
                use.highScore = 0
                use.put()
                render_template(self,'index.html',{})

####################################################################################
# Creates a json string of 5 random questions of the day
####################################################################################
class sendJsonQuestions(webapp2.RequestHandler):
    def get(self):
        questionList = Question.all()
        questionList.order("-timeSubmitted")
        randomList = random.sample(xrange(questionList.count()),5)

        obj = {
            "Questions":[
                {"questionText":questionList[randomList[0]].questionText, "answer1":questionList[randomList[0]].answer1, "answer2":questionList[randomList[0]].answer2, "answer3":questionList[randomList[0]].answer3, "answer4":questionList[randomList[0]].answer4},
                {"questionText":questionList[randomList[1]].questionText, "answer1":questionList[randomList[1]].answer1, "answer2":questionList[randomList[1]].answer2, "answer3":questionList[randomList[1]].answer3, "answer4":questionList[randomList[1]].answer4},
                {"questionText":questionList[randomList[2]].questionText, "answer1":questionList[randomList[2]].answer1, "answer2":questionList[randomList[2]].answer2, "answer3":questionList[randomList[2]].answer3, "answer4":questionList[randomList[2]].answer4},
                {"questionText":questionList[randomList[3]].questionText, "answer1":questionList[randomList[3]].answer1, "answer2":questionList[randomList[3]].answer2, "answer3":questionList[randomList[3]].answer3, "answer4":questionList[randomList[3]].answer4},
                {"questionText":questionList[randomList[4]].questionText, "answer1":questionList[randomList[4]].answer1, "answer2":questionList[randomList[4]].answer2, "answer3":questionList[randomList[4]].answer3, "answer4":questionList[randomList[4]].answer4},
            ]
        }
        self.response.out.write(json.dumps(obj, sort_keys=True))

####################################################################################
# Determines if a username and password exists in the database
####################################################################################
class receiveUsernameValid (webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        parsedUrl = url.split('?')
        userList = Use.all()
        userList.filter('username =', parsedUrl[1])
        userList.filter('password =', parsedUrl[2])
        userList.fetch(1)
        if userList.count()==1:
            self.response.out.write(True)
        else:
            self.response.out.write(False)


####################################################################################
# front-end back-end ping test class
####################################################################################
class ping(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = {
            'String':'ping'
        }
        self.response.out.write(json.dumps(obj))

####################################################################################
# Gets the users with the top 5 high scores for the leaderboard
####################################################################################
class receiveLeaderBoard(webapp2.RequestHandler):
    def get(self):
        userList = Use.all()
        userList.order("-highScore")
        userList.fetch(5)
        obj = {
            'Users': [
                {"Username":userList[0].username, "highScore":userList[0].highScore},
                {"Username":userList[1].username, "highScore":userList[1].highScore},
                {"Username":userList[2].username, "highScore":userList[2].highScore},
                {"Username":userList[2].username, "highScore":userList[2].highScore},
                {"Username":userList[2].username, "highScore":userList[2].highScore},
            ]
        }
        self.response.out.write(json.dumps(obj, sort_keys=True))



####################################################################################
# Database objects
####################################################################################
class Question(db.Model):
    questionText = db.StringProperty(multiline = True)
    answer1 = db.StringProperty(multiline=True)
    answer2 = db.StringProperty(multiline=True)
    answer3 = db.StringProperty(multiline=True)
    answer4 = db.StringProperty(multiline=True)
    catagory = db.StringProperty(multiline=True)
    timeSubmitted = db.DateTimeProperty()

class Use(db.Model):
    email = db.StringProperty()
    username = db.StringProperty()
    password = db.StringProperty()
    highScore = db.IntegerProperty()


####################################################################################
# Request handler
####################################################################################
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/savePost', savePost),
    ('/saveLogin', saveLogin),
    ('/receiveDailyQuestions', sendJsonQuestions),
    ('/receiveUsernameValid', receiveUsernameValid),
    ('/receiveLeaderBoard', receiveLeaderBoard),
    ('/ping', ping)
], debug=True)
