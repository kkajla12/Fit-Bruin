from django.conf.urls import patterns, include, url
from Menu.views import Cafe1919, DiningHalls, Breakfast


urlpatterns = patterns('',
    url(r'^Cafe1919/$', Cafe1919),
    url(r'^DiningHalls/$', DiningHalls),
    url(r'^DiningHalls/Breakfast/$', Breakfast)
)
