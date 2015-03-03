from django.contrib import admin
from APL_THC.models import Trunk

class TrunkAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'cluster', 'device_pool', 'sip_profile', 'security_profile', 'trp')

admin.site.register(Trunk, TrunkAdmin)
