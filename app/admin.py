from django.contrib import admin
from .models import City, Station, Fuel, Feature, Comment, StationFuel

admin.site.register(City)
admin.site.register(Station)
admin.site.register(Fuel)
admin.site.register(Feature)
admin.site.register(Comment)
admin.site.register(StationFuel)
