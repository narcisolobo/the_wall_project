from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^wall$', views.wall),
    url(r'^process_message$', views.process_message),
    url(r'^process_comment$', views.process_comment),
]