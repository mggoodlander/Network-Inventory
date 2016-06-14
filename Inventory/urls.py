from django.conf.urls import url
from . import views

app_name = 'Inventory'


urlpatterns = [
    # /Inventory/
    url(r'^$', views.index, name='index'),
    #/Inventory/sites/
    url(r'^sites/$', views.site, name='sites'),
    # /Inventory/71/
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # /Inventory/site/add
    url(r'^site/add/$', views.create_site, name='site-add'),
    # /Inventory/site/2
    url(r'^site/(?P<pk>[0-9]+)/$', views.SiteUpdate.as_view(), name='site-update'),
    # /Inventory/site/2/delete
    url(r'^SiteClosed/(?P<pk>[0-9]+)/$', views.closed, name='closed'),
    # /Inventory/site/addDetails/
    url(r'^(?P<pk>[0-9]+)/AddDetails/', views.create_detail, name='detail-create'),
    #
    url(r'^(?P<pk>[0-9]+)/updatedetails/', views.DetailUpdate.as_view(), name='detail-update'),
    #
    url(r'^devices/$', views.device, name='devices'),
    #
    url(r'^devices/add/$', views.create_device, name='devices_add'),
    #
    url(r'^devices/(?P<pk>[0-9]+)/$', views.DeviceUpdate.as_view(), name='device_update'),
    #
    url(r'^devices/(?P<pk>[0-9]+)/delete/$', views.DeviceDelete.as_view(), name='device-delete'),
]

