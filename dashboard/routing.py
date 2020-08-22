from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import path, re_path
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from .consumers import UniversalConsumer, UserConsumer

application = ProtocolTypeRouter({
   'websocket': AllowedHostsOriginValidator(
       AuthMiddlewareStack(
           URLRouter(
               [
                   path('example/', UniversalConsumer),
                   re_path(r'register/(?<room_name>)\w+/$',UserConsumer)
               ]
           )
       )
   )
})