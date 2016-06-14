from django.contrib import admin
from .models import Site,Config,Device

admin.site.register(Site)
admin.site.register(Config)
admin.site.register(Device)
