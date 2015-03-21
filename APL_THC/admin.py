from django.contrib import admin
from APL_THC.models import Trunk, RoutePattern

class TrunkAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'cluster')

    def get_route_pattern(self, obj):
        return "\n".join([p.pattern for p in obj.route_pattern.all()])

class RoutePatternAdmin(admin.ModelAdmin):
    list_display = ('trunk', 'pattern')


admin.site.register(Trunk, TrunkAdmin)
admin.site.register(RoutePattern, RoutePatternAdmin)

