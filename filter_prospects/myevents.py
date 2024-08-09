from django_eventstream import send_event
from rest_framework.response import Response
from rest_framework.views import APIView


class my_send_event(APIView):
    def post(self, request):
        print(""""id""")
        # print(request.user.id)
        # send_event('prospectx' + str(request.user.id), 'message', 'Task')
        event_to = "prospectx{}".format(1)
        send_event(event_to, 'message', "Task")
        return Response({"hello"})
