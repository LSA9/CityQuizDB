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
        render_template(self,'login.html',{})


class createAccountPage(webapp2.RequestHandler):
    def get(self):
        render_template(self, 'createAccount.html',{})

class checkLoginValid(webapp2.RequestHandler):
    def post(self):
        desiredUsername = self.request.get('username')
        desiredPassword = self.request.get('password')
        userList = Use.all()
        userList.filter('username =', desiredUsername)
        userList.filter('password =', desiredPassword)
        possibleUser = userList.get()
        if possibleUser != None:
            render_template(self, 'index.html', {})
        else:
            render_template(self, 'login.html', {
                'error' : 'Invalid account!'
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
        userList = Use.all()
        passw = self.request.get('password')
        name = self.request.get('username')
        userList.filter("username =", name)

        if userList.count()==1:
            invalidUsername = "Username already in use!"
            render_template(self,'createAccount.html',{
                'error' : invalidUsername
            })
        else:
            use = Use()
            use.username = name
            use.password = passw
            use.highScore = 0
            use.quizTaken = 0
            use.put()
            render_template(self,'login.html',{})

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
        currentUser = userList.get()
        if currentUser != None:
            obj = {
                "Value" : "false"
            }
        else:
            obj = {
                "Value" : "true"
            }
        self.response.out.write(json.dumps(obj))


####################################################################################
# front-end back-end ping test class
####################################################################################
class ping(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = {
            'Value':'ping'
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
                {"Username":userList[3].username, "highScore":userList[3].highScore},
                {"Username":userList[4].username, "highScore":userList[4].highScore},
            ]
        }
        self.response.out.write(json.dumps(obj, sort_keys=True))

####################################################################################
# Posts a new user to the database
####################################################################################
class sendCredentials(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        parsedUrl = url.split('?')
        newUser = Use()
        newUser.username = parsedUrl[1]
        newUser.password = parsedUrl[2]
        newUser.highScore = 0
        newUser.quizTaken = 0
        newUser.put()
        obj = {
            "Value" : "true"
        }
        self.response.out.write(json.dumps(obj))

####################################################################################
# Updates a users highscore
####################################################################################
class sendPoints(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        parsedUrl = url.split('?')
        userList = Use.all()
        userList.filter('username =', parsedUrl[1])
        currentUser = Use()
        currentUser = userList.get()
        currentUser.highScore = int(parsedUrl[2])
        currentUser.put()
        obj = {
            "Value" : "true"
        }
        self.response.out.write(json.dumps(obj))

####################################################################################
# Sets user's quizTaken field to taken
####################################################################################
class sendQuizTaken(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        parsedUrl = url.split('?')
        userList = Use.all()
        userList.filter('username =', parsedUrl[1])
        currentUser = Use()
        currentUser = userList.get()
        currentUser.quizTaken = 1
        currentUser.put()
        obj = {
            "Value" : "true"
        }
        self.response.out.write(json.dumps(obj))

####################################################################################
# check user login for if password is correct
####################################################################################
class receiveSignInValid(webapp2.RequestHandler):
    def get(self):
        url = self.request.url
        parsedUrl = url.split('?')
        userList = Use.all()
        userList.filter('username =', parsedUrl[1])
        currentUser = userList.get()
        if currentUser!=None:
            if (currentUser.password == parsedUrl[2]):
                obj = {
                    "Value" : "true",
                    "Points" : currentUser.highScore,
                    "QuizTaken" : currentUser.quizTaken
                }
            else:
                obj = {
                    "Value" : "false"
                }
        else:
            obj = {
                "Value" : "false"
            }
        self.response.out.write(json.dumps(obj))

class setQuizTakenZero(webapp2.RequestHandler):
    def get(self):
        userList = Use.all()
        for user in userList:
            user.highScore = 0
            user.put()



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
    username = db.StringProperty()
    password = db.StringProperty()
    highScore = db.IntegerProperty()
    quizTaken = db.IntegerProperty()


####################################################################################
# Request handler
####################################################################################
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/savePost', savePost),
    ('/saveLogin', saveLogin),
    ('/createAccountPage', createAccountPage),
    ('/checkLoginValid', checkLoginValid),
    ('/receiveDailyQuestions', sendJsonQuestions),
    ('/receiveUsernameValid', receiveUsernameValid),
    ('/receiveLeaderBoard', receiveLeaderBoard),
    ('/sendPoints', sendPoints),
    ('/sendCredentials', sendCredentials),
    ('/sendQuizTaken', sendQuizTaken),
    ('/receiveSignInValid', receiveSignInValid),
    ('/ping', ping),
    ('/setQuizTakenZero', setQuizTakenZero)
], debug=True)
