from channels.routing import ProtocolTypeRouter, URLRouter
import task_management.routing

application = ProtocolTypeRouter({
    'http': URLRouter(task_management.routing.urlpatterns),
})