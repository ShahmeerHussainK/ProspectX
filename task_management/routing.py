from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream
from django.urls import path

urlpatterns = [
   # url(r'^events/', AuthMiddlewareStack(
    #    URLRouter(django_eventstream.routing.urlpatterns)
#    ), {'channels': ['test']}),
    path('events/<prospectx>/<user_id>', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'format-channels': ['{prospectx}', '{prospectx}' + '{user_id}']}),

    url(r'', AsgiHandler),
]
