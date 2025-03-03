import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# import chat_app.routing 

import DriveProject.chat_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DriveProject.DriveProject.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(DriveProject.chat_app.routing.websocket_urlpatterns)  
    ),
})


