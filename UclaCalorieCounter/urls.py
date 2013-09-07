from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from Menu import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UclaCalorieCounter.views.home', name='home'),
    # url(r'^UclaCalorieCounter/', include('UclaCalorieCounter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Menu/', include('Menu.urls')),
    url(r'^$', views.home),
    url(r'^newuser/$', views.newuser),
    url(r'^profile/$', views.profile),
    url(r'^foodlog/$', views.foodlog),
    url(r'^additem/$', views.additem),
    url(r'^toptens/$', views.toptens),
    url(r'^about/$', views.about),
    url(r'^addbreakfast/$', views.addbreakfast),
    url(r'^addlunch/$', views.addlunch),
    url(r'^adddinner/$', views.adddinner),
    url(r'^addsnacks/$', views.addsnacks),
    url(r'^feastlunch/$', views.addfeastlunch),
    url(r'^feastdinner/$', views.addfeastdinner),
    url(r'^addcafe1919/$', views.addcafe1919),
    url(r'^addbruincafe/$', views.addbruincafe),
    url(r'^addrendezvous/$', views.addrendezvous),
    url(r'^addlatenight/$', views.addlatenight),
    url(r'^delete/(?P<foodlogid>\d+)/$', views.deletefoodlog, name='foodlog-delete'),
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
)
