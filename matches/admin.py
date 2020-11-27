from django.contrib import admin

# Register your models here.
from .models import AppUser, IPLSeason, Matches

# Register your models here.
admin.site.register(AppUser)
admin.site.register(IPLSeason)
admin.site.register(Matches)