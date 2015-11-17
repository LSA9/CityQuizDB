__author__ = 'Aronson1'

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from code import Use
from code import Question

package = 'backend'

@endpoints.api(name='helloworld', version='v1')
class HelloWorldApi(remote.Service):

    #Request field for getUser
    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
        username = messages.StringField,
        password = messages.StringField
    )

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, bool,
                      path='awesomePath', http_method='GETUSER',
                      name='use.getUser')
    def getUser(self, request):
        users=Use.all()
        userInQuestion = users.filter('username =',request.username)
        correctPassword = userInQuestion.filter('password =', request.password)
        if correctPassword:
            return True
        else:
            return False

APPLICATION = endpoints.api_server([HelloWorldApi])