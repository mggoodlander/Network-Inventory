from django.conf.urls import url
from . import views
#TODO add examples for all urls
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
    url(r'^(?P<pk>[0-9]+)/AddDetails/', views.CreateDetail.as_view(), name='detail-create'),
    #
    url(r'^(?P<pk>[0-9]+)/updatedetails/', views.DetailUpdate.as_view(), name='detail-update'),
    #
    url(r'^devices/$', views.device, name='devices'),
    #
    url(r'^devices/add/$', views.create_device, name='devices_add'),
    #
    url(r'^devices/(?P<pk>[0-9]+)/$', views.DeviceToSite.as_view(), name='device_update'),
    #
    url(r'^devices/(?P<pk>[0-9]+)/delete/$', views.DeviceDelete.as_view(), name='device-delete'),
    #
    url(r'^sites/(?P<device_id>[0-9]+)/', views.remove_device, name='device_remove'),
    #
    url(r'^phones/add/$', views.CreatePhone.as_view(), name='phone_add'),
    #
    url(r'^phones/$', views.phone, name='phones'),
    #
    url(r'^sites/phone/(?P<phone_id>[0-9]+)/$', views.remove_phone, name='phone_remove'),
    #
    url(r'^phone/(?P<pk>[0-9]+)', views.PhoneToSite.as_view(), name='phonetosite'),
    #
    url(r'^phone/add/(?P<pk>[0-9]+)', views.UpdatePhone.as_view(), name='update-phone'),
    #
    url(r'^phone/delete/(?P<pk>[0-9]+)', views.DeletePhone.as_view(), name='delete-phone')
]

